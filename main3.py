import pandas as pd

# Lire le fichier Excel
df = pd.read_excel("Gestion_Tickets_IT.xlsx")

# Demander l'ID du ticket
id_modification = input("Entrez l'ID du ticket à modifier : ")

# Rechercher le ticket
index = df[df["ID"].astype(str) == id_modification].index

if len(index) == 0:
    print(" Ticket introuvable.")
else:
    # Saisir les nouvelles informations
    technicien = input("Nouveau technicien IT : ")
    solution = input("Nouvelle solution : ")
    statut = input("Nouveau statut : ")

    # Modifier les données
    df.loc[index, "Technicien IT"] = technicien
    df.loc[index, "Solution"] = solution
    df.loc[index, "Statut"] = statut

    # Enregistrer
    df.to_excel("Gestion_Tickets_IT.xlsx", index=False)

    print(" Ticket modifié avec succès !")