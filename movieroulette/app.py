from flask import Flask, render_template, redirect, url_for, session, request
import psycopg2
import os

app = Flask(__name__ , static_url_path='/static')
db = "dbname='MovieRoulette' user='postgres' host='localhost' password='Lykkehvid123'"
conn = psycopg2.connect(db)
cursor = conn.cursor()

def genre_filter(genres):
    genre_condition = "("
    for genre in genres:
        genre_condition += f"genres ~* '{genre}' OR "
    return genre_condition[:-4] + ") AND "

def keyword_filter(keyword):
    # Using (case-insensitive) regexes to find titles.
    return f"(primaryTitle ~* '{keyword}' OR originalTitle ~* '{keyword}') AND "

def releaseyear_filter(year):
    return f"year = {year} AND "

def releaseyear_filter(year_range):
    min_year, max_year = year_range
    return f"(year >= {min_year} AND year <= {max_year}) "


def pick_random_movie(criteria):
    genres, keyword, rating_range, year_range, director, actor = criteria
    query = "SELECT * FROM Movies WHERE "
    min_one_criteria = False
    if not (genres == []):
        min_one_criteria = True
        query += genre_filter(genres)
    if not (keyword == ''):
        min_one_criteria = True
        query += keyword_filter(keyword)
    if not (release_year == None):
        min_one_criteria = True
        query += releaseyear_filter(release_year)
    
    if min_one_criteria:
        # Removing 'AND' from query text.
        query = query[:-4]
    else:
        # Removing 'WHERE' from query text.
        query = query[:-6]
    query += "ORDER BY random() LIMIT 1;"
    print(query)

    curr = conn.cursor()
    curr.execute(query)
    pick = curr.fetchone()
    if pick == None:
        # TODO: PRINT TIL BRUGEREN AT DER IKKE FINDES EN FILM.
        return redirect(url_for('home'))
    
    return redirect(url_for('picked_movie', movie_id=pick[0]))

@app.route("/", methods=['GET', 'POST'])
def home():
    
    # Getting 12 random movies with a rating of 8 or higher.
    twelve_rand_query = '''
        SELECT * 
        FROM Movies 
        WHERE averageRating >= 8.0
        ORDER BY random() 
        LIMIT 12;
    '''
    curr = conn.cursor()
    curr.execute(twelve_rand_query)
    movies = list(curr.fetchall())
    length = len(movies)    

    if request.method == 'POST':
        # User has clicked generate so generate random movie.
        criteria = get_criteria()
        
        # Saving which genres the user picked.
        session['genres_picked'] = criteria[0] 
        # TODO: Should save all criteria specified instead of just genres.
        
        return pick_random_movie(criteria)

    genres_picked = session.get('genres_picked', [])
    return render_template('index.html', genres_picked=genres_picked, content=movies, length=length)

def get_criteria():
    genres = request.form.getlist('genres')
    keyword = request.form.get('keyword', type=str)
    rating_range = (request.form.get('min_rating', 0.0, type=float),
                    request.form.get('max_rating', 10.0, type=float))
    year_range = (request.form.get('min_year', 1920, type=int), 
                  request.form.get('max_year', 2020, type=int))
    director = request.form.get('director', type=str)
    actor = request.form.get('actor', type=str)
    
    return genres, keyword, rating_range, year_range, director, actor

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/movie/<movie_id>")
def picked_movie(movie_id):
    # TODO: Tilføj en ekstra knap 'generate' som genererer en ny film ud fra de samme kritier
    cur = conn.cursor()
    movie_query = f'''
        SELECT *
        FROM Movies 
        WHERE id = '{movie_id}'
    '''
    cur.execute(movie_query)    
    pick = cur.fetchone()
    
    # Resetting the previously selected options.
    session['genres_picked'] = []
    
    return render_template('pickedmovie.html', content=pick)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=5000)