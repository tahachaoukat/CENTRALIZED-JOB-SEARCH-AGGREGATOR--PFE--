import pandas as pd

def filtrer_offres_emploi(titre_offre, titre_entreprise, date_offre, localisation, filename):
    data = pd.read_excel(filename)
    
    # Convert inputs to lowercase
    titre_offre = titre_offre.lower()
    titre_entreprise = titre_entreprise.lower()
    date_offre = date_offre.lower()
    localisation = localisation.lower()
    
    # Filter the data based on the provided criteria
    filtered_data = data[(data['Titre de l\'offre'].str.lower().str.contains(titre_offre)) &
                         (data['Titre de l\'entreprise'].str.lower().str.contains(titre_entreprise)) &
                         (data['Date de l\'offre'].str.lower().str.contains(date_offre)) &
                         (data['Localisation'].str.lower().str.contains(localisation))]
    
    if not filtered_data.empty:
        filtered_data.to_excel('offres_Emploi_filtres.xlsx', index=False)
        print("Les offres filtrées ont été enregistrées dans le fichier 'offres_Emploi_filtres.xlsx'.")
    else:
        print("Aucune offre ne correspond aux critères de filtrage.")

# Example usage
titre_offre = input("Entrez le titre de l'offre : ")
titre_entreprise = input("Entrez le titre de l'entreprise : ")
date_offre = input("Entrez la date de l'offre : ")
localisation = input("Entrez la localisation : ")
filename = input("Entrez le nom du fichier Excel contenant les données : ")
filtrer_offres_emploi(titre_offre, titre_entreprise, date_offre, localisation, filename)
