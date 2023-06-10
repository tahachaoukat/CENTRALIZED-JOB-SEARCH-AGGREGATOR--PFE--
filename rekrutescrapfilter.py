import pandas as pd

def filtrer_offres_emploi(entres, secteurs, filename):
    data = pd.read_excel(filename)
    
    # Convertir les entrées en minuscules pour une recherche insensible à la casse
    entres = entres.lower()
    secteurs = secteurs.lower()
    
    # Filter les données en utilisant str.lower() et str.contains()
    filtered_data = data[(data['entreprise'].str.lower().str.contains(entres)) &
                         (data['secteur'].str.lower().str.contains(secteurs))]
    
    if not filtered_data.empty:
        filtered_data.to_excel('offres_reKrute_filtres.xlsx', index=False)
        print("Les offres filtrées ont été enregistrées dans le fichier 'offres_reKrute_filtres.xlsx'.")
    else:
        print("Aucune offre ne correspond aux critères de filtrage.")

# Example usage
nom_entreprise = input("Entrez le nom de l'entreprise : ")
secteur = input("Entrez le secteur : ")
filename = input("Entrez le nom du fichier Excel contenant les données : ")
filtrer_offres_emploi(nom_entreprise, secteur, filename)
