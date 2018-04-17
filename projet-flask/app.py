#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
from flask import Flask, redirect, url_for
from flask import request
from passlib.hash import argon2
from flask import render_template
import mysql.connector
from flask import g
from flask import Flask, session
from flask.ext.session import Session
SECRET_KEY = 'some random string w17h n|_|m83r5'

app = Flask(__name__, template_folder='template')

def connect_db () :
    g.mysql_connection = mysql.connector.connect(
        host = 'localhost',
        user = 'marlon',
        password = 'soleil13',
        database = 'flask'
    )

    g.mysql_cursor = g.mysql_connection.cursor()
    return g.mysql_cursor

def get_db () :
    if not hasattr(g, 'db') :
        g.db = connect_db()
    return g.db


@app.route('/')
def index () :
    return 'Hello World !'

@app.route('/lorem-ipsum/')
def lorem_ipsum () :
    page = """
        <!doctype html>
        <html lang="fr"><head>
        <meta charset="utf-8">
        <title>WEBSITES STATUS Martine Marlon</title>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="/">STATUS</a>
  </button>

  <div class="collapse navbar-collapse" id="navbarColor03">
    <ul class="navbar-nav mr-auto my-2 my-lg-0">
    </ul>
    <ul class="navbar-nav my-2 my-lg-0">

              <li class="nav-item">
                    <a class="nav-link" href="/login/">Connexion
              </li>
    </ul>
  </div>
</nav>
        <section class="container-fluid body-container">

    <h1 class="text-center">Liste des sites</h1>
    <div class="row websites-container text-center">


        <div class="card  bg-success  text-white mb-3 website-card">
            <div class="card-header website-card-title"><h4><a href="https://raspbian-france.fr">https://raspbian-france.fr</a></h4></div>
            <div class="card-body">
                <div>Actif</div>

                </div>
            </div>
            <div class="card-footer">
                <a href="show1/" class="btn btn-lg btn-white">Voir la fiche</a>
            </div>
        </div>

        <div class="card  bg-success  text-white mb-3 website-card">
            <div class="card-header website-card-title"><h4><a href="https://forum.raspbian-france.fr">https://forum.raspbian-france.fr</a></h4></div>
            <div class="card-body">
                <div>Actif</div>

                </div>
            </div>
            <div class="card-footer">
                <a href="show2/" class="btn btn-lg btn-white">Voir la fiche</a>
            </div>
        </div>


    </div>

        </section>
        <div id="flash-messages-container">

</div>

</body>
</html>
    """
    return page

@app.route('/lorem-ipsum-template/')
def lorem_ipsum_template () :
    return render_template('lorem-ipsum.html')

@app.route('/lorem-ipsum/show1/')
def lorem_ipsum_show1 () :
    return render_template('show1.php')

@app.route('/lorem-ipsum/show2/')
def lorem_ipsum_show2 () :
    return render_template('show2.html')

@app.route('/show-sentence-template/<sentence>/')
def show_sentence_template (sentence) :
    return render_template('show-sentence.html', sentence = sentence)

@app.route('/say/')
def say () :
    say = request.args.get('say')
    return render_template('say.html', say = say)

@app.route('/contact/', methods=['GET', 'POST'])
def contact () :
    email = request.form.get('email')
    message = request.form.get('message')
    return render_template('contact.html', email = email, message = message)

@app.route('/show-entries/')
def show_entries () :
    db = get_db()
    db.execute('SELECT name, value FROM entries')
    entries = db.fetchall()
    return render_template('show-entries.html', entries = entries)

@app.teardown_appcontext
def close_db (error) :
    if hasattr(g, 'db') :
        g.db.close()

@app.route('/login/', methods = ['GET', 'POST'])
def login () :
    email = str(request.form.get('email'))
    password = str(request.form.get('password'))

    db = get_db()
    db.execute('SELECT email, password, is_admin FROM user WHERE email = %(email)s', {'email' : email})
    users = db.fetchall()

    valid_user = False
    #for user in users :
        #if argon2.verify(password, user[1]) :
            #valid_user = user

    if valid_user :
        session['user'] = valid_user
        return redirect(url_for('admin'))

    return render_template('login.html')

@app.route('/admin/')
def admin () :
    if not session.get('user') or not session.get('user')[2] :
        return redirect(url_for('login'))

    return render_template('admin.html', user = session['user'])

@app.route('/admin/logout/')
def admin_logout () :
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True)
