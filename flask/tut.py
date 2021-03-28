from flask import Flask, redirect,url_for, render_template,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.secret_key= "Hello"
app.config["SQLAlCHEMY_DATABASE_URI"]='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.permanent_session_lifetime=timedelta(days=5)

db=SQLAlchemy(app)

class users(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    name=db.Column("name",db.String(100))
    location=db.Column("location",db.String(100))


    def __init__(self,name,location):
        self.name=name
        self.location=location


@app.route("/")                        # this tells us the url to find our page
def home():
    return render_template("index.html")        #used to import/render the html files

@app.route("/view")
def view():
    return render_template("view.html",values=users.query.all())





#@app.route("/<name>/")                     # the / after the name will help redirect us to the previous pagge without an error
#def user(name):
    #return render_template("index.html")
    #return render_template("index.html",content=name,r=2)        #the content mentioned in the html file will replace the name

#@app.route("/admin/")
#def admin():
    #return redirect(url_for("home"))
    #return redirect(url_for("user",name='Admin '))       #this will redirect you to the user page

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        session.permanent=True
        user=request.form["nm"]                              #get and post information on a form
        session["user"]=user

        found_user=users.query.filter_by(name=user).first()
        #found_user=users.query.filter_by(name=user).delete()   to delete single database
        #for user in found_user:                                to delete multiple database
            #user.delete()
        if found_user:
            session["location"]=found_user.location
        else:
            usr=users(user,"")
            db.session.add(usr)
            db.session.commit()


        flash("Login Sucessful! ")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user",methods=["POST","GET"])
def user():
    location=None
    if "user" in session:
        user=session["user"]
        if request.method=="POST":
            location=request.form["location"]
            session["location"]=location
            found_user=users.query.filter_by(name=user).first()
            found_user.location=location
            db.session.commit()
            flash("location was saved!")
        else:
            if "location" in session:
                location=session["location"]

        #return render_template("user.html",user=user)
        return render_template("user.html",location=location)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have been logged out sucessfully","info")
    session.pop("user",None)
    session.pop("location",None)
    return redirect(url_for("login"))


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
