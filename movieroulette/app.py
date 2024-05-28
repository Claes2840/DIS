from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
import requests
from bs4 import BeautifulSoup
import psycopg2
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__ , static_url_path='/static')
db = "dbname='MovieRoulette' user='jacobsiegumfeldt' host='localhost' password='dis'"
conn = psycopg2.connect(db)
cursor = conn.cursor()

@app.route("/", methods=['GET', 'POST'])
def home():
    cur = conn.cursor()
    #Getting 10 random rows from Movies
    twelve_rand = '''SELECT * FROM Movies ORDER BY random() LIMIT 12;'''
    cur.execute(twelve_rand)
    movies = list(cur.fetchall())
    length = len(movies)    
    genres = []
    if request.method == 'POST':
        genres = request.form.getlist('genres')
        print(genres)
        
    return render_template('index.html', selected_options=genres, content=movies, length=length)

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/pickedmovie/<movieid>")
def picked_movie(movieid):
    cur = conn.cursor()
    pick_movie = f'''SELECT * FROM Movies WHERE id=\'{movieid}\''''
    cur.execute(pick_movie)    
    pick = cur.fetchone()
    print(pick)
    return render_template('pickedmovie.html', content=pick)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=5002)