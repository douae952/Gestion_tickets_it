import pandas as pd
import os

FICHIER = "Gestion_Tickets_IT.xlsx"

def charger_donnees():
    if os.path.exists(FICHIER):
        return pd.read_excel(FICHIER)
    else:
        colonnes = ["ID", "Date", "Utilisateur", "Département", "Catégorie",
                    "Description", "Technicien IT", "Solution", "Statut"]
        return pd.DataFrame(columns=colonnes)

def sauvegarder(df):
    df.to_excel(FICHIER, index=False)

def ajouter_ticket(df):
    print("\n--- Nouveau ticket ---")
    id_ticket = input("ID : ")
    date = input("Date (JJ/MM/AAAA) : ")
    utilisateur = input("Utilisateur : ")
    departement = input("Département : ")
    categorie = input("Catégorie : ")
    description = input("Description : ")
    technicien = input("Technicien IT : ")
    solution = input("Solution : ")

    # Validation simple du statut
    statuts_valides = ["Ouvert", "En cours", "Résolu"]
    statut = input(f"Statut {statuts_valides} : ")
    while statut not in statuts_valides:
        print("Statut invalide, réessaie.")
        statut = input(f"Statut {statuts_valides} : ")

    nouveau_ticket = {
        "ID": id_ticket, "Date": date, "Utilisateur": utilisateur,
        "Département": departement, "Catégorie": categorie,
        "Description": description, "Technicien IT": technicien,
        "Solution": solution, "Statut": statut
    }
    df.loc[len(df)] = nouveau_ticket
    sauvegarder(df)
    print(" Ticket ajouté avec succès !")
    return df

def afficher_tickets(df):
    print("\n--- Liste des tickets ---")
    if df.empty:
        print("Aucun ticket enregistré.")
    else:
        print(df.to_string(index=False))

def rechercher_ticket(df):
    id_recherche = input("ID du ticket à rechercher : ")
    resultat = df[df["ID"].astype(str) == id_recherche]
    if resultat.empty:
        print("" \
        " Aucun ticket trouvé avec cet ID.")
    else:
        print(resultat.to_string(index=False))

def modifier_statut(df):
    id_ticket = input("ID du ticket à modifier : ")
    if id_ticket in df["ID"].astype(str).values:
        nouveau_statut = input("Nouveau statut (Ouvert / En cours / Résolu) : ")
        df.loc[df["ID"].astype(str) == id_ticket, "Statut"] = nouveau_statut
        sauvegarder(df)
        print(" Statut mis à jour !")
    else:
        print("Ticket introuvable.")
    return df

def menu():
    df = charger_donnees()
    while True:
        print("\n===== GESTION DES TICKETS IT =====")
        print("1. Ajouter un ticket")
        print("2. Afficher tous les tickets")
        print("3. Rechercher un ticket par ID")
        print("4. Modifier le statut d'un ticket")
        print("5. Quitter")
        choix = input("Choix : ")

        if choix == "1":
            df = ajouter_ticket(df)
        elif choix == "2":
            afficher_tickets(df)
        elif choix == "3":
            rechercher_ticket(df)
        elif choix == "4":
            df = modifier_statut(df)
        elif choix == "5":
            print(" À bientôt !")
            break
        else:
            print("Choix invalide, réessaie.")

if __name__ == "__main__":
    menu()

