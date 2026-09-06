from flask import Flask, render_template, request, redirect, session
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


app = Flask(__name__)

# =========================
# CONFIGURATION
# =========================

app.secret_key = "yazaki_secret_key"


# =========================
# VERIFICATION CONNEXION
# =========================

def verifier_connexion():

    if not session.get("logged_in"):
        return redirect("/login")

    return None


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # =========================
        # ADMIN
        # =========================

        if username == "admin" and password == "1234":

            session["logged_in"] = True
            session["role"] = "admin"
            session["username"] = username

            return redirect("/")


        # =========================
        # EMPLOYE
        # =========================

        elif username == "employe" and password == "1234":

            session["logged_in"] = True
            session["role"] = "employe"
            session["username"] = username

            return redirect("/employe")


        # =========================
        # TECHNICIEN IT
        # =========================

        elif username == "technicien" and password == "1234":

            session["logged_in"] = True
            session["role"] = "technicien"
            session["username"] = username

            return redirect("/technicien")


        # =========================
        # IDENTIFIANTS INCORRECTS
        # =========================

        else:

            message = "Nom d'utilisateur ou mot de passe incorrect."


    return render_template(
        "login.html",
        message=message
    )


# =========================
# DECONNEXION
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# DASHBOARD ADMIN
# =========================

@app.route("/")
def accueil():

    acces = verifier_connexion()

    if acces:
        return acces

    # Employé
    if session.get("role") == "employe":
        return redirect("/employe")

    # Technicien
    if session.get("role") == "technicien":
        return redirect("/technicien")

    # Admin
    if session.get("role") == "admin":
        return render_template("index.html")

    return redirect("/login")


# =========================
# ESPACE EMPLOYE
# =========================

@app.route("/employe")
def espace_employe():

    acces = verifier_connexion()

    if acces:
        return acces

    if session.get("role") != "employe":

        return redirect("/")

    return render_template("employe.html")


# =========================
# ESPACE TECHNICIEN
# =========================

@app.route("/technicien")
def espace_technicien():

    acces = verifier_connexion()

    if acces:
        return acces

    if session.get("role") != "technicien":

        return redirect("/")

    return render_template("technicien.html")


# =========================
# AJOUTER UN TICKET
# =========================

@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():

    acces = verifier_connexion()

    if acces:
        return acces

    if request.method == "POST":

        df = pd.read_excel(
            "Gestion_Tickets_IT.xlsx"
        )

        # =========================
        # ID AUTOMATIQUE
        # =========================

        if df.empty:

            id_ticket = 1

        else:

            id_ticket = int(df["ID"].max()) + 1


        # =========================
        # DATE AUTOMATIQUE
        # =========================

        date = pd.Timestamp.now().strftime(
            "%Y-%m-%d"
        )


        # =========================
        # UTILISATEUR
        # =========================

        utilisateur = session.get("username")


        # =========================
        # VALEURS SELON LE ROLE
        # =========================

        if session.get("role") == "employe":

            technicien = ""
            solution = ""
            statut = "En attente"

        else:

            technicien = request.form.get(
                "technicien",
                ""
            )

            solution = request.form.get(
                "solution",
                ""
            )

            statut = request.form.get(
                "statut",
                "En attente"
            )


        # =========================
        # NOUVEAU TICKET
        # =========================

        nouveau_ticket = {

            "ID": id_ticket,

            "Date": date,

            "Utilisateur": utilisateur,

            "Département": request.form[
                "departement"
            ],

            "Catégorie": request.form[
                "categorie"
            ],

            "Description": request.form[
                "description"
            ],

            "Technicien IT": technicien,

            "Solution": solution,

            "Statut": statut

        }


        # =========================
        # AJOUT DANS DATAFRAME
        # =========================

        df.loc[len(df)] = nouveau_ticket


        # =========================
        # SAUVEGARDE EXCEL
        # =========================

        df.to_excel(
            "Gestion_Tickets_IT.xlsx",
            index=False
        )


        # =========================
        # REDIRECTION
        # =========================

        if session.get("role") == "employe":

            return redirect("/mes-tickets")

        return redirect("/tickets")


    return render_template(
        "ajouter.html"
    )


# =========================
# AFFICHER TOUS LES TICKETS
# =========================

@app.route("/tickets")
def afficher_tickets():

    acces = verifier_connexion()

    if acces:
        return acces

    # Seulement Admin et Technicien
    if session.get("role") not in [
        "admin",
        "technicien"
    ]:

        return redirect("/employe")


    df = pd.read_excel(
        "Gestion_Tickets_IT.xlsx"
    )


    tickets = df.to_dict(
        orient="records"
    )


    return render_template(
        "tickets.html",
        tickets=tickets
    )


# =========================
# MES TICKETS
# =========================

@app.route("/mes-tickets")
def mes_tickets():

    acces = verifier_connexion()

    if acces:
        return acces


    # Seulement Employé
    if session.get("role") != "employe":

        return redirect("/")


    df = pd.read_excel(
        "Gestion_Tickets_IT.xlsx"
    )


    utilisateur = session.get(
        "username"
    )


    # Tickets de l'utilisateur connecté
    tickets = df[
        df["Utilisateur"]
        .astype(str)
        .str.lower()
        ==
        utilisateur.lower()
    ]


    tickets = tickets.to_dict(
        orient="records"
    )


    return render_template(
        "tickets.html",
        tickets=tickets
    )


# =========================
# RECHERCHER UN TICKET
# =========================

@app.route("/rechercher", methods=["GET", "POST"])
def rechercher():

    acces = verifier_connexion()

    if acces:
        return acces


    ticket = None
    message = None


    if request.method == "POST":

        df = pd.read_excel(
            "Gestion_Tickets_IT.xlsx"
        )


        id_recherche = request.form[
            "id"
        ]


        resultat = df[
            df["ID"]
            .astype(str)
            ==
            id_recherche
        ]


        if resultat.empty:

            message = "Ticket introuvable."


        else:

            ticket = resultat.iloc[
                0
            ].to_dict()


    return render_template(
        "rechercher.html",
        ticket=ticket,
        message=message
    )


# =========================
# MODIFIER UN TICKET
# =========================

@app.route("/modifier", methods=["GET", "POST"])
def modifier():

    acces = verifier_connexion()

    if acces:
        return acces


    # Seulement Admin et Technicien
    if session.get("role") not in [
        "admin",
        "technicien"
    ]:

        return redirect("/employe")


    message = None


    if request.method == "POST":

        df = pd.read_excel(
            "Gestion_Tickets_IT.xlsx"
        )


        id_modification = request.form[
            "id"
        ]


        resultat = df[
            df["ID"]
            .astype(str)
            ==
            id_modification
        ]


        if resultat.empty:

            message = "Ticket introuvable."


        else:

            index = resultat.index[0]


            df.loc[
                index,
                "Technicien IT"
            ] = request.form[
                "technicien"
            ]


            df.loc[
                index,
                "Solution"
            ] = request.form[
                "solution"
            ]


            df.loc[
                index,
                "Statut"
            ] = request.form[
                "statut"
            ]


            df.to_excel(
                "Gestion_Tickets_IT.xlsx",
                index=False
            )


            return redirect(
                "/tickets"
            )


    return render_template(
        "modifier.html",
        message=message
    )


# =========================
# SUPPRIMER UN TICKET
# =========================

@app.route("/supprimer", methods=["GET", "POST"])
def supprimer():

    acces = verifier_connexion()

    if acces:
        return acces


    # Suppression réservée à l'Admin
    if session.get("role") != "admin":

        return redirect("/")


    message = None


    if request.method == "POST":

        df = pd.read_excel(
            "Gestion_Tickets_IT.xlsx"
        )


        id_suppression = request.form[
            "id"
        ]


        if id_suppression in (
            df["ID"]
            .astype(str)
            .values
        ):


            df = df[
                df["ID"]
                .astype(str)
                != id_suppression
            ]


            df.reset_index(
                drop=True,
                inplace=True
            )


            df.to_excel(
                "Gestion_Tickets_IT.xlsx",
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


# =========================
# STATISTIQUES
# =========================

@app.route("/statistiques")
def statistiques():

    acces = verifier_connexion()

    if acces:
        return acces


    # Admin et Technicien seulement
    if session.get("role") not in [
        "admin",
        "technicien"
    ]:

        return redirect("/employe")


    df = pd.read_excel(
        "Gestion_Tickets_IT.xlsx"
    )


    statistiques = df[
        "Statut"
    ].value_counts()


    plt.figure(
        figsize=(8, 5)
    )


    statistiques.plot(
        kind="bar"
    )


    plt.title(
        "Nombre de tickets par statut"
    )


    plt.xlabel(
        "Statut"
    )


    plt.ylabel(
        "Nombre de tickets"
    )


    plt.tight_layout()


    plt.savefig(
        "static/statistiques.png"
    )


    plt.close()


    return render_template(
        "statistiques.html"
    )


# =========================
# LANCER L'APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )