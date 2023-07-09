from flask import Flask , render_template, request , redirect ,session,jsonify,url_for,send_from_directory
from datetime import datetime
import secrets
from flask_mysqldb import MySQL
# Scrapping dependencies
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import os
import time as t
import pymysql
import json
import shutil
import uuid

app = Flask(__name__)
secret_key=secrets.token_hex(16)
app.secret_key=secret_key
# Connect app with mysql
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="flask"
mysql=MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/dash')
def dashb():

    cursor=mysql.connection.cursor()
    query=cursor.execute("SELECT profession, COUNT(*) AS count FROM users GROUP BY profession")
    if query :
     result=cursor.fetchall()
     #chart graphe pour les villes 
     cursor3=mysql.connection.cursor()
     query3=cursor3.execute("SELECT ville, COUNT(*) AS count FROM users GROUP BY ville")
    if query3 :
     result3=cursor3.fetchall()
    
     return render_template('dashbord.html',data=result,data3=result3) 
    


     # Informations de connexion à la base de données
    # serveur = "localhost"
    # nomUtilisateur = "root"
    # nomBaseDeDonnees = "flask"

    # try:
        # Connexion à la base de données
        # connexion = pymysql.connect(host=serveur, user=nomUtilisateur, database=nomBaseDeDonnees)

        # Requête pour récupérer les données des professions
        # requete = "SELECT profession, COUNT(*) AS count FROM users GROUP BY profession"
        # with connexion.cursor() as cursor:
        #     cursor.execute(requete)
        #     resultat = cursor.fetchall()

    #     # Conversion des données en tableaux utilisables par Chart.js
    #     labels = []
    #     data = []

    #     for row in resultat:
    #       labels.append(row[0])  # Accès à l'élément avec l'indice 0 (profession)
    #       data.append(row[1])  # Accès à l'élément avec l'indice 1 (count)

    #     # Fermeture de la connexion à la base de données
    #     connexion.close()
    # except pymysql.Error as e:
    #     # Gestion des erreurs de connexion à la base de données
    #     return "Erreur de connexion à la base de données : " + str(e)
    # return render_template('dashbord.html')
@app.route("/profil")
def Profile():
    return render_template("profile.html")    
@app.route("/check_admin",methods=["POST","GET"])
def check_admin():
    if request.method=="POST":
        
          username=request.form["username"]
          passw=request.form["pass"]
         
           
          cursor=mysql.connection.cursor()
          query=cursor.execute("SELECT * FROM admin WHERE userame=%s AND pass=%s",(username,passw))
          if query:   
            
            result=cursor.fetchall()
             
            if result:
                 cursor2=mysql.connection.cursor()
                 query2=cursor2.execute("SELECT profession, COUNT(*) AS count FROM users GROUP BY profession")
                 result2=cursor2.fetchall()
                 cursor3=mysql.connection.cursor()
                 query3=cursor3.execute("SELECT ville, COUNT(*) AS count FROM users GROUP BY ville")
                 result3=cursor3.fetchall()
                 session["admin_logged"]=True
                 session["admin_name"]=result[0][4]
                 current_datetime = datetime.now()
                 formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                 session["logged_time"]=formatted_datetime
                 
                 return render_template("dashbord.html",data=result2,data3=result3)
            
            
          else:
              return render_template("page_login_admin.html") 
    if request.method=="GET":
        return redirect("/dash",code=302)              

@app.route('/check',methods=["POST","GET"])
def check():
      
      if "user_logged" in session and session["user_logged"]:
          return redirect("/dash-user")
      if request.method=="POST":
          username=request.form["username"]
          passw=request.form["pass"]
          cursor=mysql.connection.cursor()
          qwery=cursor.execute("SELECT * FROM users WHERE email=%s AND pass=%s",(username,passw))
          if qwery:   
            
             result=cursor.fetchall()
             if result:
                 session["user_logged"]=True
                 session["user_name"]=result[0][1]
                 session["user_email"]=result[0][2]
                 session["ville"]=result[0][5]
                 session["profession"]=result[0][4]
                 session["image"]=result[0][6]
                 session["user_id"]=result[0][0]
                 return render_template("user.html")
                 
            
            
          else:
              return render_template("page_login.html")
@app.route("/register")
def register():
    return render_template("page_register.html")
@app.route("/admin")
def admin():
    if "admin_logged" in session and session["admin_logged"]:
        return redirect("/dash")
    return render_template("page_login_admin.html")
            
@app.route("/login",methods=["POST","GET"])
def login():
    
    if "user_logged" in session and session["user_logged"]:
        return redirect("/dash-user")
    
    if request.method == "POST":

       nom=request.form["nom"]
       file=request.files["file"]
       email = request.form["email"]
       password = request.form["pswd"]
       profession = request.form["prof"]
       ville = request.form["Ville"]
       if file :
           file_name=file.filename
           destination = os.path.join(app.root_path, 'static', 'Profils', file_name)
           file.save(destination)
    
    # Définir le répertoire de stockage
    #    storage_directory = "/static/Profils"
    
    #    if not os.path.exists(storage_directory):
        # os.makedirs(storage_directory)
    
    # Générer un nom unique pour le fichier
    #    unique_filename = str(uuid.uuid4()) + "_" + file.filename
    
    # Construire le chemin complet du fichier
    #    file_path = os.path.join(storage_directory, unique_filename)
    
    # Enregistrer le fichier dans le répertoire de stockage
    #    with open(file_path, "wb") as f:
        # shutil.copyfileobj(file, f)
    
    # Définir les permissions appropriées sur le fichier
    #    os.chmod(file_path, 0o777)
    
    # Utiliser le nom du fichier enregistré dans la suite de votre code si nécessaire
    #    file_name = unique_filename
    
       cursor = mysql.connection.cursor()
       cursor.execute("INSERT INTO users(username,email,pass,profession,ville,image) VALUES(%s,%s,%s,%s,%s,%s)", (nom, email, password, profession, ville, file_name))
       mysql.connection.commit()
       cursor.close()
       
    
               
    return render_template('page_login.html')
    # return jsonify(file.filename)
    
   


@app.route("/dash-user")
def user_dash():
    return render_template("user.html")
@app.route("/deconnexion")
def logout():
    session.pop("admin_logged")
    return redirect("/")
@app.route("/deconn_user")
def logout_user():
    session.pop("user_logged")
    return redirect("/")
@app.route('/dashbaord.html')
def dash():
    return '<html><body><h1>Ma page</h1></body></html>'
@app.route("/about")
def about():
    return render_template("about.html")





# start Scrapping Function wadifa sans filter
def alwadifa_scraping(keyword,named_file):
    base_url = f"http://www.alwadifa-maroc.com/search?query={keyword}"
    jobs = []

    url = base_url
    # print(f"Scraping: {url}")

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
       

      
    
        # filepath = f"/Files/{named_file}.xlsx"
        # df.to_excel(f"{filepath}", index=True)
        
        directory = 'Files'
        if not os.path.exists(directory):
           os.makedirs(directory)
        filepath = os.path.join(directory, f"{named_file}.xlsx")
        df.to_excel(filepath, index=True)
       
        
    else:
        return "auncun"
# end Scrapping Function wadifa sans filter

#scrapping rekrute
def recrute_scraping(keyword, number,filename):
    number = str(number)
    keyword = urllib.parse.quote(keyword)  # Encode le mot-clé pour l'utiliser dans l'URL
    new_url = f"https://www.rekrute.com/offres.html?p={number}&s=1&o=1&query={keyword}&keyword={keyword}&st=d"
    
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
    
    liste_of_datas = []

    for i in range(1, 5):
    
     liste_of_datas.append(data)

    data_frame = pd.concat(liste_of_datas, axis=0).reset_index(drop=True)
      # Set the fixed file name
    directory = 'Files'
    
    filepath = os.path.join(directory, f"{filename}.xlsx")
    data_frame.to_excel(filepath, index=True)
    
    return jsonify("siii")
   
# Scrapping Routes 

@app.route('/download/<path:filename>')
def download_file(filename):
    directory = 'Files'  # Name of the folder
    return send_from_directory(directory, filename, as_attachment=True)

@app.route("/wadifashow")
def wshow():
    return render_template("wadifa.html")
@app.route("/rekrute")
def Rshow():
    return render_template("rekrute.html")
@app.route("/emploi")
def Eshow():
    return render_template("emploi.html")
@app.route("/wadifapost",methods=["POST","GET"])
def wpost():
    if request.method=="POST":
     current_datetime = datetime.now()
     formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
     nom_offre=request.form["sans_offrenom"]
     nom_fichier=request.form["nomfile"]
     
     
     
     if alwadifa_scraping(nom_offre,nom_fichier) != "aucun":
          alwadifa_scraping(nom_offre,nom_fichier)
          
          session["success_wadifa"]=True
          session["named_file"]=nom_fichier
          cursor=mysql.connection.cursor()
          cursor.execute("INSERT INTO files(name,user_id) VALUES(%s,%s)",(nom_offre,session["user_id"]))
          mysql.connection.commit()
          cursor.close()
          return render_template("wadifa.html",href=session["named_file"])
        
     else : 
         return jsonify("unsucess")
    #  Recrute calling function
@app.route("/rekrutepost",methods=["POST","GET"])
def postrecrute():
    if request.method=="POST":
        filename=session["user_name"]+"recrute"
        my_keyword=request.form["keyword"]
        my_number=request.form["nombre"]
        if recrute_scraping(my_keyword,my_number,filename):
            session["success_rekrute"]=True
            session["named_file"]=filename
           
            return render_template("rekrute.html",href=session["named_file"])
             
        else:
            return jsonify("unsuccess recrute")    
    

          
    
# @app.route('/<path:filename>')
# def download_file(filename):
#     # Provide the path to the directory where the file is located
#     directory = '/path/to/file/directory'
#     return send_from_directory(directory, filename, as_attachment=True)             
           
         





     
     
    

if __name__ == "__main__":
    app.run(debug=True)






