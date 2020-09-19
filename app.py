import sys
import sqlite3 as lite
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

#example how to access database
# con = lite.connect("information.db")
# cur = con.cursor()
# cur.execute("SELECT * FROM information WHERE username='%s'" % username)
# information = cur.fetchall()

#remember to set global variable of username after login

@app.route("/")
def index():
    return render_template("index.html", message="hello")

@app.route("/landing")
def landing():
    con = lite.connect("all.db")
    cur = con.cursor()
    username = "testing"
    cur.execute("SELECT * FROM history WHERE username='%s';" % username)
    information = cur.fetchall()

    #create list of different attributes
    subject_list = []
    expected_time_list = []
    real_time_list = []
    difference_time_list = []

    for info in information:
        subject_list.append(info[1])
        expected_time_list.append(info[2])
        real_time_list.append(info[3])
        difference_time_list.append(info[4])
    
    dictionary = {}
    dictionary["subject"] = subject_list
    dictionary["expected_time"] = expected_time_list
    dictionary["real_time"] = real_time_list
    dictionary["difference_time"] = difference_time_list

    return render_template("landing.html", dictionary=dictionary)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation_password = request.form.get("confirmation-password")

        #error checking
        if not username:
            return redirect("/apology")
        if not password:
            return redirect("/apology")
        if not confirmation_password:
            return redirect("/apology")
        if password != confirmation_password:
            return redirect("/apology")
        
        pass_hash = generate_password_hash(password)
        con = lite.connect("all.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?);", (username, pass_hash))
        con.commit()
        con.close()

        return redirect("/login")

@app.route("/task")
def task():
    return render_template("task.html", emailAddress="themicklepickle@gmail.com", timeElapsed="15:21", timeExpected="1:00:00", timeDifference="44:39")

@app.route("/apology")
def apology():
    return render_template("apology.html")


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run()

