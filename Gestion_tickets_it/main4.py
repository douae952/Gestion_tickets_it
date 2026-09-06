import pandas as pd

# Lire le fichier Excel
df = pd.read_excel("Gestion_Tickets_IT.xlsx")

# Demander l'ID du ticket
id_suppression = input("Entrez l'ID du ticket à supprimer : ")

# Vérifier si le ticket existe
if id_suppression in df["ID"].astype(str).values:

    # Supprimer le ticket
    df = df[df["ID"].astype(str) != id_suppression]

    # Réinitialiser les index
    df.reset_index(drop=True, inplace=True)

    # Enregistrer les modifications
    df.to_excel("Gestion_Tickets_IT.xlsx", index=False)

    print("Ticket supprimé avec succès !")

else:
    print(" Ticket introuvable.")