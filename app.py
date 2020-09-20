import sys
import sqlite3 as lite
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
# import headers.average, headers.timeConversions, headers.timer
# from ml import *

app = Flask(__name__)
app.secret_key = "asfdjklasdjflasdkf"

#example how to access database
# con = lite.connect("information.db")
# cur = con.cursor()
# cur.execute("SELECT * FROM information WHERE username='%s'" % username)
# information = cur.fetchall()

@app.route("/")
def index():
    if "user" in session:
        return redirect("/landing")
    else:
        return redirect("/login")

@app.route("/landing", methods=["GET", "POST"])
def landing():
    if request.method == "GET":
        if "user" in session:
            #for displaying the history
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
        else:
            return redirect("/")

    else:
        #for getting the timer
        global expected_time
        expected_time = request.form.get("expected_time")
        subject = request.form.get("subject")
        task_name = request.form.get("task_name")
        
        #error checking
        if expected_time < 1:
            return redirect("/apology")
        if not subject:
            return redirect("/apology")
        if not task_name:
            return redirect("/apology")

        session["timer"] = expected_time
        return redirect("/task")

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
    return render_template("task.html", emailAddress=username_global, timeExpected=expected_time, timeDifference="44:39", timer=session["timer"])


@app.route("/apology")
def apology():
    return render_template("apology.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return redirect("/apology")
        if not password:
            return redirect("/apology")
        
        con = lite.connect("all.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username='%s';" % username)
        information = cur.fetchall()

        for info in information:
            hash_pass = info[2]
        
        if check_password_hash(hash_pass, password):
            global username_global
            username_global = username
            session["user"] = username
            return redirect("/")
            
        return redirect("/apology")


'''
todo: 
html according to this link: https://docs.google.com/drawings/d/1mPRTqE2jXMfDL8ZYX_1ulpt7_qXSAaNUh-PLpcZjDkI/edit?usp=sharing
add times (iterable, with this format:)  ((predicted_time1, actual_time1), (predicted_time2, actual_time2), (predicted_timen, actual_timen))
Add model download that redirects to static/{id}.pkl
what format does cur.fetchall() output?
'''

@app.route("/stats", methods=["GET", "POST"])
def stats():
    # if "user" in session:
    #     if request.method == "GET":
    #         return render_template("stats.html", user_image = None)
    #     else:
    #         percentage = request.form.get("percentage")
    #         model = request.form.get("percentage")
    #         if not username:
    #             return redirect("/apology")
    #         if not password:
    #             return redirect("/apology")
            
    #         plotmodel(times, username_global, percentage, model) # please see ml.py for what this does, there is detailed documentation there

            return render_template("stats.html", user = "1")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

    
    # con = lite.connect("all.db")
    # cur = con.cursor()
    # cur.execute("SELECT * FROM history WHERE username='%s';" % username_global)
    # information = cur.fetchall()

    # predicted_time_list = []
    # actual_time_list = []

    # for info in information:
    #     predicted_time_list.append(info[3])
    #     actual_time_list.append(info[4])

    # times = np.column_stack(np.asarray(predicted_time_list), np.asarray(actual_time_list))
    # return render_template("stats.html")


    # if request.method == "GET":
    #     return render_template("stats.html", user_image = None)
    # else:
    #     percentage = request.form.get("percentage")
    #     model = request.form.get("percentage")
    #     if not username:
    #         return redirect("/apology")
    #     if not password:
    #         return redirect("/apology")
        
    #     plotmodel(times, username_global, percentage, model) # please see ml.py for what this does, there is detailed documentation there

    #     return render_template("stats.html", user_image = f"/static/{id}.png")



if __name__ == "__main__":
    app.run()

