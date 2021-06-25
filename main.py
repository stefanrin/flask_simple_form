from flask import Flask, render_template,request,redirect,flash, session
import random
import os.path
import json
import re
#RIN 8/19
app=Flask(__name__)
app.secret_key=str(random.randrange(0,1000))
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def hello_world():
    return render_template("form_login.html")
@app.route("/login", methods=["POST"])
def login():
    dict_logins={}
    form_data=request.form
    username=form_data["fuser"]
    password=form_data["fpass"]
    opcija=form_data["btn"]
    if (os.path.exists("logins.json")):
        f = open("logins.json")
        dict_logins = json.load(f)

    if opcija=="registracija":

        if not re.match("^[a-zA-Z0-9]{3,}$",username):
            flash("Korisnicko ime mora sadrzati najmanje 3 karaktera i ne sme sadrzati razmake")
            return redirect("/")

        if not re.match("\S{5,}",password):
            flash("Lozinka mora biti najmanje 5 karaktera")
            return redirect("/")

        if username in dict_logins.keys():
            flash("Korisnicko ime zauzeto")
            return redirect("/")
        else:
            dict_logins[username]=password
            with open("logins.json",'w') as f:
                json.dump(dict_logins,f)
            flash("Korisnik '" + username + "' uspeno registrovan.")
            return redirect("/")


    if opcija=="prijava":
        #flash("Uspesno ste se prijavili")
        if username in dict_logins.keys():
            if (dict_logins[username] == password):
                session['user']=username
                return redirect("/student")
    flash("Korisnicko ime ili lozinka netacni")
    return redirect("/")

@app.route("/student")
def profil():
    user=session.get('user', None)
    student_dict={}
    ime=""
    prezime=""
    adresa=""
    kontakt=""
    user_string="studenti/"+user+".json"
    if (os.path.exists(user_string)):
        f=open(user_string)
        student_dict=json.load(f)
        ime=student_dict["ime"]
        prezime=student_dict["prezime"]
        adresa=student_dict["adresa"]
        kontakt=student_dict["kontakt"]
    return render_template("form_profile.html",arg_username=user, arg_ime=ime, arg_prezime=prezime,arg_adresa=adresa,arg_kontakt=kontakt)

@app.route("/save",methods=["POST"])
def save():
    user = session.get('user', None)
    student_dict = {}
    form_data=request.form
    ime = ""
    prezime = ""
    adresa = ""
    kontakt = ""
    opcija = form_data["btn"]
    if (opcija=="odjava"):
        session.clear()
        return redirect("/")
    if (opcija=="sacuvaj"):
        if "name" in form_data.keys():
            ime=form_data["name"]
        if "surname" in form_data.keys():
            prezime = form_data["surname"]
        if "address" in form_data.keys():
            adresa=form_data["address"]
        if "contact" in form_data.keys():
            kontakt = form_data["contact"]
    student_dict["ime"]=ime
    student_dict["prezime"] = prezime
    student_dict["adresa"] = adresa
    student_dict["kontakt"] = str(kontakt)
    if not (os.path.exists("studenti")):
        #Add exception
        os.mkdir("studenti")
    with open("studenti/"+user+".json", 'w') as f:
        json.dump(student_dict, f)
    return redirect("/student")

if __name__=="__main__":
    app.run(debug=True)
