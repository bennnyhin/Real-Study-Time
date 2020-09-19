import sys
import sqlite3 as lite
from flask_login import LoginManager, UserMixin
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

#example how to access database
# con = lite.connect("information.db")
# cur = con.cursor()
# cur.execute("SELECT * FROM information WHERE username='%s'" % username)
# information = cur.fetchall()


@app.route("/")
def index():
    return render_template("index.html", message="hello")

if __name__ == "__main__":
    app.run()
