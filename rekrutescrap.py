from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import urllib.parse

def recrute_scraping(keyword, number):
    number = str(number)
    keyword = urllib.parse.quote(keyword)  # Encode le mot-clé pour l'utiliser dans l'URL
    new_url = f"https://www.rekrute.com/offres.html?p={number}&s=1&o=1&query={keyword}&keyword={keyword}&st=d"
    print(new_url)
    webpage = urllib.request.urlopen(new_url)
    soup = BeautifulSoup(webpage, "html.parser")
    results = soup.find_all("div", {"class": "col-sm-10 col-xs-12"})
   
    titles = []
    descs = []
    entres = []
    objecs = []
    publis = []
    secteurs = []
    job_links = []  # Nouvelle liste pour stocker les liens de l'offre

    for result in results:
        title = result.find("a").text
        titles.append(title)

        try:
            description_du_poste = result.find("span", {"style": "color: #5b5b5b; font-style : italic;"}).text
        except:
            description_du_poste = result.find("span", {"style": "color: #5b5b5b;margin-top: 5px;"}).text
        descs.append(description_du_poste)

        entreprise = result.find("span", {"style": "color: #5b5b5b;"}).text
        entres.append(entreprise)

        objectif = result.find("span", {"style": "color: #5b5b5b;margin-top: 5px;"}).text
        objecs.append(objectif)

        publication = result.find("em", {"class": "date"}).text
        publis.append(publication)

        secteur = result.find("li").text.replace(' \n', '')
        secteurs.append(secteur)

        # Extraction du lien de l'offre
        job_link = result.find("a")["href"]
        base_url = "https://www.rekrute.com"
        job_link_full = urllib.parse.urljoin(base_url, job_link)
        job_links.append(job_link_full)

    jobs = {
        "Titre de l'offre": titles,
        "Description de poste": descs,
        "Entreprise": entres,
        "Objectif": objecs,
        "Publication": publis,
        "Secteur": secteurs,
        "Lien de l'offre": job_links  # Ajout du lien de l'offre
    }

    data = pd.DataFrame(jobs)
    return data


keyword = input("Entrez le mot-clé du poste : ")
liste_of_datas = []

for i in range(1, 5):
    data = recrute_scraping(keyword, i)
    liste_of_datas.append(data)

data_frame = pd.concat(liste_of_datas, axis=0).reset_index(drop=True)
file_name = "offres_rekrute"  # Set the fixed file name
data_frame.to_excel(file_name + '.xlsx', index=False)
