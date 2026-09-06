import pandas as  pd

# Lire le fichier Excel
df = pd.read_excel("Gestion_Tickets_IT.xlsx")

# Demander l'ID
id_recherche = input("Entrez l'ID du ticket : ")

# Rechercher le tickect
resultat = df[df["ID"].astype(str) == id_recherche]

# Afficher le résultat
if resultat.empty:
    print(" Ticket introuvable.")
else:
    print("\n Ticket trouvé ")
    print(resultat)
