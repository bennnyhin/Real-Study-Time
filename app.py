import sys
import sqlite3 as lite
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
# import headers.average, headers.timeConversions, headers.timer
from ml import *
import pandas as pd

expected_time = None
task_name = None
username_global = None

app = Flask(__name__)
app.secret_key = "asfdjklasdjflasdkf"

#example how to access database
# con = lite.connect("information.db")
# cur = con.cursor()
# cur.execute("SELECT * FROM information WHERE username='%s'" % username)
# information = cur.fetchall()

@app.route("/")
def index():
    if "user" in session and username_global is not None:
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
            username = username_global
            cur.execute("SELECT * FROM history WHERE username='%s';" % username)
            information = cur.fetchall()

            #create list of different attributes
            task_name_list = []
            expected_time_list = []
            real_time_list = []
            difference_time_list = []

            difference = []

            for info in information:
                task_name_list.append(info[1])
                expected_time_list.append(info[2])
                real_time_list.append(info[4])
                # for (x,y) in zip(info[3], info[4]):
                #     if (x == None or y == None):
                #         difference.append(None)
                #     else:
                #         difference.append(x - y)
                if (info[4] == None or info[3] == None):
                    difference_time_list.append(None)
                else:
                    difference_time_list.append(info[4] - info[3])

                # difference_time_list.append(difference)

            dictionary = {}
            dictionary["task_name"] = task_name_list
            dictionary["expected_time"] = expected_time_list
            dictionary["real_time"] = real_time_list
            dictionary["difference_time"] = difference_time_list
            return render_template("landing.html", dictionary=dictionary, user=username_global, numElements=len(dictionary["task_name"])) #TODO change this back to username_global
        else:
            return redirect("/")
    else:
        #for getting the timer
        global expected_time, task_name
        task_name = request.form.get("task_name")
        expected_time = request.form.get("expected_time")

        #error checking
        if int(expected_time) < 1:
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
    return render_template("task.html", emailAddress=username_global, timeExpected=expected_time, timer=session["timer"])


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
Add model download that redirects to static/{id}.pkl
'''

@app.route("/stats", methods=["GET", "POST"])
def stats():
    if request.method == "GET":
        if "user" in session:
            return render_template("stats.html", user_image = None)
        else:
            return redirect("/")
    else:
        percentage = request.form.get("percentagee")
        percentage = True if percentage=='on' else False
        model = request.form.get("modell")
        model = True if model=='on' else False
        stat = request.form.get("stats")
        con = lite.connect("all.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM history WHERE username='%s';" % username_global)
        information = cur.fetchall()

        predicted_time_list = []
        actual_time_list = []

        for info in information:
            predicted_time_list.append(info[3])
            actual_time_list.append(info[4])
        times = np.column_stack([np.asarray(predicted_time_list), np.asarray(actual_time_list)])
        
        # COMMENT THE FOLLOWING LINE OUT IF LEGIT DATA
        # times = generate_noisy_data()
        times = pd.DataFrame(times, columns=["Expected time", "Actual time"])
        times = times.dropna()
        times = times.values.astype(np.float32)
        plotmodel(times, username_global, percentage=percentage, model=model) # please see ml.py for what this does, there is detailed documentation there
        if stat:
            stati = statistics(times)
            print(stati)
        else: 
            stati=None
        return render_template("stats.html", user = username_global, statistics=stati)

@app.route("/complete")
def complete():
    time_difference = request.args.get('difference')
    print(time_difference)
    time_total = int(expected_time) + int(time_difference)

    con = lite.connect("all.db")
    cur = con.cursor()
    cur.execute("INSERT INTO history (username, task_name, expected_time, real_time, difference_time) VALUES (?, ?, ?, ?,?);", (username_global, task_name, expected_time, time_total, time_difference))
    con.commit()
    con.close()
    return redirect("/")
    

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

