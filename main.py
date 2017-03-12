from flask import Flask, render_template, request
import json
import random
import sqlite3
from datetime import datetime

TIME_FMT = "%m-%d %H:%M:%S"

def currentTime():
    return datetime.now().strftime(TIME_FMT)


with open("problemset.json", "r", encoding="utf-8") as fp:
    problemset = json.load(fp)

conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

app = Flask("survey")


@app.route("/")
def home():
    which = random.randint(0, 5)
    return render_template("survey.html",
                           which=which, problems=problemset[which],
                           time=currentTime())


@app.route("/check", methods=["POST"])
def check():
    form = request.form
    which = int(form['which'])

    def score():
        sum = 0
        scores = ''
        for i in range(10):
            if int(form[str.format('choices{}', i)]) \
                 == ord(problemset[which]['choices'][i]['answer']) - ord('A'):
                sum += 8
                scores += '8'
            else:
                scores += '0'

        for i in range(5):
            if form[str.format('judges{}', i)] \
                 == str(problemset[which]['judges'][i]['answer']):
                sum += 4
                scores += '4'
            else:
                scores += '0'

        return (scores, sum)

    now = currentTime()
    elapsed = datetime.now() - datetime.strptime(form['starttime'], TIME_FMT)
    try:
        c.execute('INSERT INTO score VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (form['name'], form['number'], form['school'], form['class'],
                   form['which'], now, elapsed.seconds,
                   *(score()), form['phone'], request.remote_addr))
        conn.commit()
    except Exception as e:
        return "Please check whether all items are finished. \
                Repetead submission is now allowed."

    return "<div style=\"margin: auto;\"><h3>Thanks for your participation!</h3></div>"

app.run()
