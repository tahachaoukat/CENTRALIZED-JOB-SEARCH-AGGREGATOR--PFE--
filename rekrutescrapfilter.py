import pandas as pd

def filtrer_offres_emploi(titre, secteur, filename):
    data = pd.read_excel(filename)
    
    # Convertir les titres et secteurs en minuscules pour une recherche insensible à la casse
    titre = titre.lower()
    secteur = secteur.lower()
    
    # Filter les données en utilisant str.lower() et str.contains()
    filtered_data = data[(data['Titre de l\'offre'].str.lower().str.contains(titre)) &
                         (data['Secteur'].str.lower().str.contains(secteur))]
    
    if not filtered_data.empty:
        filtered_data.to_excel('offres_rekrute_filtrees.xlsx', index=False)
        print("Les offres filtrées ont été enregistrées dans le fichier 'offres_rekrute_filtrees.xlsx'.")
    else:
        print("Aucune offre ne correspond aux critères de filtrage.")

# Example usage
titre_offre = input("Entrez le titre de l'offre : ")
secteur = input("Entrez le secteur : ")
filename = input("Entrez le nom du fichier Excel contenant les données : ")
filtrer_offres_emploi(titre_offre, secteur, filename)
