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
    return render_template('dashbord.html')
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
                 session["admin_logged"]=True
                 session["admin_name"]=result[0][4]
                 current_datetime = datetime.now()
                 formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                 session["logged_time"]=formatted_datetime
                 
                 return render_template("dashbord.html")
            
            
          else:
              return "<h1>your are not admin</h1>" 
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
                 session["user_id"]=result[0][0]
                 return render_template("user.html")
                 
            
            
          else:
              return "<h1>your are not admin</h1>" 
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
    if request.method=="POST":
        nom=request.form["nom"]
        email=request.form["email"]
        password= request.form["pswd"]
        profession=request.form["prof"]
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO users(username,email,pass,profession) VALUES(%s,%s,%s,%s)",(nom,email,password,profession))
        mysql.connection.commit()
        cursor.close()
       
    
               
    return render_template('page_login.html')


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

# Scrapping Routes 

@app.route('/download/<path:filename>')
def download_file(filename):
    directory = 'Files'  # Name of the folder
    return send_from_directory(directory, filename, as_attachment=True)

@app.route("/wadifashow")
def wshow():
    return render_template("wadifa.html")
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

          
    
# @app.route('/<path:filename>')
# def download_file(filename):
#     # Provide the path to the directory where the file is located
#     directory = '/path/to/file/directory'
#     return send_from_directory(directory, filename, as_attachment=True)             
           
         





     
     
    

if __name__ == "__main__":
    app.run(debug=True)






