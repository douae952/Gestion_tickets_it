from flask import Flask, render_template, request, redirect, session
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# APPLICATION FLASK

app = Flask(__name__)

app.secret_key = "yazaki_secret_key"



# NOM DU FICHIER EXCEL

FICHIER_EXCEL = "Gestion_Tickets_IT.xlsx"


# VÉRIFICATION DE CONNEXION

def verifier_connexion():

    if not session.get("logged_in"):

        return redirect("/login")

    return None


# CONNEXION

@app.route("/login", methods=["GET", "POST"])
def login():

    message = None

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        password = request.form.get("password", "")


        # ADMIN

        if username == "admin" and password == "1234":

            session["logged_in"] = True

            session["role"] = "admin"

            session["username"] = username

            return redirect("/")


        # EMPLOYÉ

        elif username == "employe" and password == "1234":

            session["logged_in"] = True

            session["role"] = "employe"

            session["username"] = username

            return redirect("/employe")


        # TECHNICIEN IT

        elif username == "technicien" and password == "1234":

            session["logged_in"] = True

            session["role"] = "technicien"

            session["username"] = username

            return redirect("/technicien")


        # IDENTIFIANTS INCORRECTS

        else:

            message = "Nom d'utilisateur ou mot de passe incorrect."


    return render_template(
        "login.html",
        message=message
    )


# DÉCONNEXION

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# PAGE D'ACCUEIL

@app.route("/")
def accueil():

    acces = verifier_connexion()

    if acces:

        return acces


    # EMPLOYÉ

    if session.get("role") == "employe":

        return redirect("/employe")


    # TECHNICIEN

    if session.get("role") == "technicien":

        return redirect("/technicien")


    # ADMIN

    if session.get("role") == "admin":

        return render_template("index.html")


    return redirect("/login")


# ESPACE EMPLOYÉ

@app.route("/employe")
def espace_employe():

    acces = verifier_connexion()

    if acces:

        return acces


    # Seul l'employé peut accéder à cet espace

    if session.get("role") != "employe":

        return redirect("/")


    return render_template(
        "employe.html"
    )


# ESPACE TECHNICIEN

@app.route("/technicien")
def espace_technicien():

    acces = verifier_connexion()

    if acces:

        return acces


    # Seul le technicien peut accéder à cet espace

    if session.get("role") != "technicien":

        return redirect("/")


    return render_template(
        "technicien.html"
    )


# AJOUTER UN TICKET

@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():

    acces = verifier_connexion()

    if acces:

        return acces


    # FORMULAIRE ENVOYÉ

    if request.method == "POST":

        # LIRE LE FICHIER EXCEL

        df = pd.read_excel(
            FICHIER_EXCEL
        )


        # GÉNÉRER UN NOUVEL ID

        if df.empty:

            id_ticket = 1

        else:

            id_ticket = int(
                df["ID"].max()
            ) + 1


        # DATE

        date = pd.Timestamp.now().strftime(
            "%Y-%m-%d"
        )


        # UTILISATEUR CONNECTÉ

        utilisateur = session.get(
            "username",
            ""
        )


        # DONNÉES DU FORMULAIRE

        departement = request.form.get(
            "departement",
            ""
        ).strip()


        categorie = request.form.get(
            "categorie",
            ""
        ).strip()


        description = request.form.get(
            "description",
            ""
        ).strip()


        # SI EMPLOYÉ
        # Le ticket arrive sans technicien.
        # Le technicien sera choisi plus tard lorsqu'il
        # décidera de traiter le ticket.

        if session.get("role") == "employe":

            technicien = ""

            solution = ""

            statut = "En attente"


        # SI ADMIN OU TECHNICIEN

        else:

            technicien = request.form.get(
                "technicien",
                ""
            ).strip()


            solution = request.form.get(
                "solution",
                ""
            ).strip()


            statut = request.form.get(
                "statut",
                "En attente"
            ).strip()


        # CRÉER LE NOUVEAU TICKET

        nouveau_ticket = {

            "ID": id_ticket,

            "Date": date,

            "Utilisateur": utilisateur,

            "Département": departement,

            "Catégorie": categorie,

            "Description": description,

            "Technicien IT": technicien,

            "Solution": solution,

            "Statut": statut

        }


        # AJOUTER LE TICKET AU DATAFRAME

        df.loc[len(df)] = nouveau_ticket


        # ENREGISTRER DANS EXCEL

        df.to_excel(
            FICHIER_EXCEL,
            index=False
        )


        # REDIRECTION

        if session.get("role") == "employe":

            return redirect(
                "/mes-tickets"
            )


        return redirect(
            "/tickets"
        )


    # AFFICHER LA PAGE

    return render_template(
        "ajouter.html"
    )


# AFFICHER TOUS LES TICKETS

@app.route("/tickets")
def afficher_tickets():

    acces = verifier_connexion()

    if acces:

        return acces


    # ADMIN ET TECHNICIEN SEULEMENT

    if session.get("role") not in [
        "admin",
        "technicien"
    ]:

        return redirect("/employe")


    # LIRE EXCEL

    df = pd.read_excel(
        FICHIER_EXCEL
    )


    # TRANSFORMER EN LISTE

    tickets = df.to_dict(
        orient="records"
    )


    return render_template(
        "tickets.html",
        tickets=tickets
    )


# MES TICKETS - EMPLOYÉ

@app.route("/mes-tickets")
def mes_tickets():

    acces = verifier_connexion()

    if acces:

        return acces


    # EMPLOYÉ SEULEMENT

    if session.get("role") != "employe":

        return redirect("/")


    # LIRE EXCEL

    df = pd.read_excel(
        FICHIER_EXCEL
    )


    # UTILISATEUR CONNECTÉ

    utilisateur = str(
        session.get(
            "username",
            ""
        )
    ).strip().lower()


    # FILTRER SES PROPRES TICKETS

    tickets = df[
        df["Utilisateur"]
        .astype(str)
        .str.strip()
        .str.lower()
        == utilisateur
    ]


    # TRANSFORMER EN LISTE

    tickets = tickets.to_dict(
        orient="records"
    )


    return render_template(
        "tickets.html",
        tickets=tickets
    )


# RECHERCHER UN TICKET

@app.route("/rechercher", methods=["GET", "POST"])
def rechercher():

    acces = verifier_connexion()

    if acces:

        return acces


    ticket = None

    message = None


    # RECHERCHE

    if request.method == "POST":

        # LIRE EXCEL

        df = pd.read_excel(
            FICHIER_EXCEL
        )


        # RÉCUPÉRER L'ID

        id_recherche = request.form.get(
            "id",
            ""
        ).strip()


        # RECHERCHER

        resultat = df[
            df["ID"].astype(str).str.strip()
            == id_recherche
        ]


        # TICKET INTROUVABLE

        if resultat.empty:

            message = "Ticket introuvable."


        # TICKET TROUVÉ

        else:

            ticket = resultat.iloc[
                0
            ].to_dict()


    return render_template(
        "rechercher.html",
        ticket=ticket,
        message=message
    )


# TRAITER / MODIFIER UN TICKET

@app.route("/modifier", methods=["GET", "POST"])
def modifier():

    acces = verifier_connexion()

    if acces:

        return acces


    # ADMIN ET TECHNICIEN PEUVENT TRAITER

    if session.get("role") not in [
        "admin",
        "technicien"
    ]:

        return redirect("/employe")


    # MÉTHODE GET
    # Lorsqu'on clique sur "Traiter" dans tickets.html,
    # l'ID arrive automatiquement ici.
    # Exemple :
    # /modifier?id=5

    if request.method == "GET":

        id_ticket = request.args.get(
            "id",
            ""
        ).strip()


        # VÉRIFIER L'ID

        if not id_ticket:

            return render_template(
                "modifier.html",
                ticket=None,
                message="Aucun ticket sélectionné."
            )


        # LIRE EXCEL

        df = pd.read_excel(
            FICHIER_EXCEL
        )


        # RECHERCHER LE TICKET

        resultat = df[
            df["ID"].astype(str).str.strip()
            == id_ticket
        ]


        # TICKET INTROUVABLE

        if resultat.empty:

            return render_template(
                "modifier.html",
                ticket=None,
                message="Ticket introuvable."
            )


        # RÉCUPÉRER LE TICKET

        ticket = resultat.iloc[
            0
        ].to_dict()


        # AFFICHER LE FORMULAIRE

        return render_template(
            "modifier.html",
            ticket=ticket,
            message=None
        )


    # MÉTHODE POST
    # Le technicien a rempli :
    # - Technicien IT
    # - Solution
    # - Statut
    # On enregistre ces informations dans Excel.

    if request.method == "POST":

        # LIRE EXCEL

        df = pd.read_excel(
            FICHIER_EXCEL
        )


        # RÉCUPÉRER L'ID

        id_ticket = request.form.get(
            "id",
            ""
        ).strip()


        # VÉRIFIER L'ID

        if not id_ticket:

            return render_template(
                "modifier.html",
                ticket=None,
                message="ID du ticket manquant."
            )


        # RECHERCHER LE TICKET

        resultat = df[
            df["ID"].astype(str).str.strip()
            == id_ticket
        ]


        # TICKET INTROUVABLE

        if resultat.empty:

            return render_template(
                "modifier.html",
                ticket=None,
                message="Ticket introuvable."
            )


        # RÉCUPÉRER L'INDEX

        index = resultat.index[
            0
        ]


        # RÉCUPÉRER LES INFORMATIONS

        technicien = request.form.get(
            "technicien",
            ""
        ).strip()


        solution = request.form.get(
            "solution",
            ""
        ).strip()


        statut = request.form.get(
            "statut",
            "En attente"
        ).strip()


        # VÉRIFIER LE TECHNICIEN

        if not technicien:

            ticket = resultat.iloc[
                0
            ].to_dict()


            return render_template(
                "modifier.html",
                ticket=ticket,
                message="Veuillez saisir le nom du technicien."
            )


        # MODIFIER LE TECHNICIEN

        df.loc[
            index,
            "Technicien IT"
        ] = technicien


        # MODIFIER LA SOLUTION

        df.loc[
            index,
            "Solution"
        ] = solution


        # MODIFIER LE STATUT

        df.loc[
            index,
            "Statut"
        ] = statut


        # ENREGISTRER DANS EXCEL

        df.to_excel(
            FICHIER_EXCEL,
            index=False
        )


        # RETOUR À LA LISTE DES TICKETS

        return redirect(
            "/tickets"
        )


# SUPPRIMER UN TICKET

@app.route("/supprimer", methods=["GET", "POST"])
def supprimer():

    acces = verifier_connexion()

    if acces:

        return acces


    # ADMIN UNIQUEMENT

    if session.get("role") != "admin":

        return redirect("/")


    message = None


    # SUPPRESSION

    if request.method == "POST":

        # LIRE EXCEL

        df = pd.read_excel(
            FICHIER_EXCEL
        )


        # ID À SUPPRIMER

        id_suppression = request.form.get(
            "id",
            ""
        ).strip()


        # VÉRIFIER SI LE TICKET EXISTE

        if id_suppression in df[
            "ID"
        ].astype(str).str.strip().values:


            # SUPPRIMER

            df = df[
                df["ID"].astype(str).str.strip()
                != id_suppression
            ]


            # RÉINITIALISER LES INDEX

            df.reset_index(
                drop=True,
                inplace=True
            )


            # ENREGISTRER

            df.to_excel(
                FICHIER_EXCEL,
                index=False
            )


            return redirect(
                "/tickets"
            )


        else:

            message = "Ticket introuvable."


    return render_template(
        "supprimer.html",
        message=message
    )


# STATISTIQUES

@app.route("/statistiques")
def statistiques():

    acces = verifier_connexion()

    if acces:

        return acces


    # ADMIN ET TECHNICIEN

    if session.get("role") not in [
        "admin",
        "technicien"
    ]:

        return redirect("/employe")


    # LIRE EXCEL

    df = pd.read_excel(
        FICHIER_EXCEL
    )


    # COMPTER LES TICKETS PAR STATUT

    statistiques = df[
        "Statut"
    ].value_counts()


    # CRÉER LE GRAPHIQUE

    plt.figure(
        figsize=(8, 5)
    )


    statistiques.plot(
        kind="bar"
    )


    # TITRE

    plt.title(
        "Nombre de tickets par statut"
    )


    # AXE X

    plt.xlabel(
        "Statut"
    )


    # AXE Y

    plt.ylabel(
        "Nombre de tickets"
    )


    # AJUSTER

    plt.tight_layout()


    # SAUVEGARDER LE GRAPHIQUE

    plt.savefig(
        "static/statistiques.png"
    )


    # FERMER LE GRAPHIQUE

    plt.close()


    # AFFICHER LA PAGE

    return render_template(
        "statistiques.html"
    )


# LANCEMENT DE L'APPLICATION

if __name__ == "__main__":

    app.run(
        debug=True
    )