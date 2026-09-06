import pandas as pd
# Lire le fichier Excel
df = pd.read_excel("Gestion_Tickets_IT.xlsx")
# Afficher tous les tickets
print("\nListe des tickets :")
print(df)