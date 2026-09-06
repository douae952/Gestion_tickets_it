import pandas as pd
import matplotlib.pyplot as plt
def ajouter_ticket():
    
    df = pd.read_excel("Gestion_Tickets_IT.xlsx")

    id_ticket = input("ID : ")
    date = input("Date : ")
    utilisateur = input("Utilisateur : ")
    departement = input("Département : ")
    categorie = input("Catégorie : ")
    description = input("Description : ")
    technicien = input("Technicien IT : ")
    solution = input("Solution : ")
    statut = input("Statut : ")

    nouveau_ticket = {
        "ID": id_ticket,
        "Date": date,
        "Utilisateur": utilisateur,
        "Département": departement,
        "Catégorie": categorie,
        "Description": description,
        "Technicien IT": technicien,
        "Solution": solution,
        "Statut": statut,
    }

    df.loc[len(df)] = nouveau_ticket
    df.to_excel("Gestion_Tickets_IT.xlsx", index=False)

    print("Ticket ajouté avec succès !")
def afficher_tickets():
    
    df = pd.read_excel("Gestion_Tickets_IT.xlsx")
    print(df)
def rechercher_ticket():
    
    df = pd.read_excel("Gestion_Tickets_IT.xlsx")

    id_recherche = input("Entrez l'ID : ")

    resultat = df[df["ID"].astype(str) == id_recherche]

    if resultat.empty:
        print(" Ticket introuvable.")
    else:
        print(resultat)
def modifier_ticket():
    df = pd.read_excel("Gestion_Tickets_IT.xlsx")

    id_modification = input("Entrez l'ID du ticket : ")

    index = df[df["ID"].astype(str) == id_modification].index

    if len(index) == 0:
        print(" Ticket introuvable.")
    else:
        technicien = input("Nouveau Technicien IT : ")
        solution = input("Nouvelle Solution : ")
        statut = input("Nouveau Statut : ")

        df.loc[index, "Technicien IT"] = technicien
        df.loc[index, "Solution"] = solution
        df.loc[index, "Statut"] = statut

        df.to_excel("Gestion_Tickets_IT.xlsx", index=False)

        print(" Ticket modifié avec succès !")
def supprimer_ticket():
    df = pd.read_excel("Gestion_Tickets_IT.xlsx")

    id_suppression = input("Entrez l'ID du ticket : ")

    if id_suppression in df["ID"].astype(str).values:

        df = df[df["ID"].astype(str) != id_suppression]

        df.reset_index(drop=True, inplace=True)

        df.to_excel("Gestion_Tickets_IT.xlsx", index=False)

        print(" Ticket supprimé avec succès !")

    else:
        print(" Ticket introuvable.")
def statistiques():
    df = pd.read_excel("Gestion_Tickets_IT.xlsx")

    statistiques = df["Statut"].value_counts()

    statistiques.plot(kind="bar")

    plt.title("Nombre de tickets par statut")
    plt.xlabel("Statut")
    plt.ylabel("Nombre de tickets")

    plt.show()
while True:

    print("\n========== Gestion des Tickets IT ==========")
    print("1. Ajouter un ticket")
    print("2. Afficher les tickets")
    print("3. Rechercher un ticket")
    print("4. Modifier un ticket")
    print("5. Supprimer un ticket")
    print("6. Afficher les statistiques")
    print("7. Quitter")

    choix = input("Votre choix : ")

    if choix == "1":
        ajouter_ticket()

    elif choix == "2":
        afficher_tickets()

    elif choix == "3":
        rechercher_ticket()

    elif choix == "4":
        modifier_ticket()

    elif choix == "5":
        supprimer_ticket()

    elif choix == "6":
        statistiques()

    elif choix == "7":
        print("Merci d'avoir utilisé l'application.")
        break

    else:
        print("Choix invalide !")
