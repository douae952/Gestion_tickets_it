import pandas as pd
import matplotlib.pyplot as plt

# Lire le fichier Excel
df = pd.read_excel("Gestion_Tickets_IT.xlsx")

# Compter les tickets par statut
statistiques = df["Statut"].value_counts()

# Créer le graphique
plt.figure(figsize=(6,4))
statistiques.plot(kind="bar")

# Titre et axes
plt.title("Nombre de tickets par statut")
plt.xlabel("Statut")
plt.ylabel("Nombre de tickets")

# Afficher le graphique
plt.show()