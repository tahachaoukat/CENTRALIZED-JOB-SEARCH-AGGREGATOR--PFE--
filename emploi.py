from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

def emploi_ma_scraping(keyword, num_offres):
    base_url = f"https://www.emploi.ma/recherche-jobs-maroc/{keyword}?"
    jobs = []

    url = base_url
    print(f"Scraping: {url}")

    webpage = urllib.request.urlopen(url)
    soup = BeautifulSoup(webpage, "html.parser")
    job_elements = soup.find_all("div", {"class": "col-lg-5 col-md-5 col-sm-5 col-xs-12 job-title"})
    
    if len(job_elements) == 0:
        print("Aucune offre d'emploi correspondante n'a été trouvée.")
        return

    for job_element in job_elements:
        job_title = job_element.find('h5').text.strip()
        company_title = job_element.find('a', class_='company-name').text.strip()
        job_date = job_element.find('p', class_='job-recruiter').text.strip().split('|')[0].strip()
        job_location = job_element.find('p', class_='job-recruiter').find_next_sibling('p').text.strip().split('Région de : ')[-1]
        job_link = "https://www.emploi.ma" + job_element.find('h5').find('a')['href']

        job = {
            'Titre de l\'offre': job_title,
            'Titre de l\'entreprise': company_title,
            'Date de l\'offre': job_date,
            'Localisation': job_location,
            'Lien de l\'offre': job_link
        }

        jobs.append(job)

        if len(jobs) >= num_offres:
            break

    if len(jobs) >= num_offres:
        df = pd.DataFrame(jobs[:num_offres])
        filepath = input("Entrez le nom du fichier Excel de sortie : ") + ".xlsx"
        df.to_excel(filepath, index=False)
        print(f"Les données ont été enregistrées dans le fichier '{filepath}'.")
    else:
        print("Le nombre d'offres demandé n'est pas disponible sur le site.")

keyword = input("Entrez le mot-clé de recherche : ")
num_offres = int(input("Entrez le nombre d'offres d'emploi à rechercher : "))
emploi_ma_scraping(keyword, num_offres)
