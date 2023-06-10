import pandas as pd

def filtrer_offres_emploi(titre_offre, date_offre, filename):
    data = pd.read_excel(filename)
    
    # Convertir les entrées en minuscules pour une recherche insensible à la casse
    titre_offre = titre_offre.lower()
    date_offre = date_offre.lower()
    
    # Filter les données en utilisant str.lower() et str.contains()
    filtered_data = data[(data['Titre de l\'offre'].str.lower().str.contains(titre_offre)) &
                         (data['Date de l\'offre'].str.lower().str.contains(date_offre))]
    
    if not filtered_data.empty:
        filtered_data.to_excel('offre_alwadifa_filtre.xlsx', index=False)
        print("Les offres filtrées ont été enregistrées dans le fichier 'offre_alwadifa_filtre.xlsx'.")
    else:
        print("Aucune offre ne correspond aux critères de filtrage.")

# Exemple d'utilisation
titre_offre = input("Entrez le titre de l'offre : ")
date_offre = input("Entrez la date de l'offre : ")
filename = input("Entrez le nom du fichier Excel contenant les données : ")
filtrer_offres_emploi(titre_offre, date_offre, filename)
