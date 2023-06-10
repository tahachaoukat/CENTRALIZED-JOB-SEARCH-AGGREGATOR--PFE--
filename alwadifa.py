from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

def alwadifa_scraping(keyword):
    base_url = f"http://www.alwadifa-maroc.com/search?query={keyword}"
    jobs = []

    url = base_url
    print(f"Scraping: {url}")

    webpage = urllib.request.urlopen(url)
    soup = BeautifulSoup(webpage, "html.parser")
    job_elements_ar_deux = soup.find_all("div", {"class": "bloc-content ar deux"})
    job_elements_fr_deux = soup.find_all("div", {"class": "bloc-content fr deux"})
    job_elements_fr_prem = soup.find_all("div", {"class": "bloc-content fr prem"})
    job_elements_ar_prem = soup.find_all("div", {"class": "bloc-content ar prem"})

    job_elements = job_elements_ar_deux + job_elements_fr_deux + job_elements_fr_prem + job_elements_ar_prem
    
    if len(job_elements) == 0:
        print("Aucune offre d'emploi correspondante n'a été trouvée.")
        return

    for job_element in job_elements:
        job_title = job_element.find("a").text.strip()
        job_company = job_element.find("img").get("alt")
        job_description = job_element.find("p").text.strip()
        job_date = job_element.find_all("li")[0].text.strip()

        job_link = "www.alwadifa-maroc.com" + job_element.find("a").get("href")

        jobs.append({
            "Titre de l'offre": job_title,
            "Titre de l'entreprise": job_company,
            "Description de l'offre": job_description,
            "Date de l'offre": job_date,
            "Lien de l'offre": job_link
        })

    if len(jobs) > 0:
        df = pd.DataFrame(jobs)
        filepath = "offres_wadifa.xlsx"
        df.to_excel(filepath, index=False)
        print(f"Les données ont été enregistrées dans le fichier '{filepath}'.")
    else:
        print("Aucune offre d'emploi n'a été trouvée.")

keyword = input("Entrez le mot-clé de recherche : ")
alwadifa_scraping(keyword)
