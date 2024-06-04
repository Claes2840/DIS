from flask import Flask, render_template, redirect, url_for, session, request
import psycopg2
import os

app = Flask(__name__ , static_url_path='/static')
db = "dbname='MovieRoulette' user='postgres' host='localhost' password='Lykkehvid123'"
conn = psycopg2.connect(db)

def filter_genre(genres):
    if not genres:
        return ""
    genre_condition = "("
    for genre in genres:
        genre_condition += f"genres ~* '{genre}' OR "
    return genre_condition[:-4] + ") AND "

def filter_keyword(keyword):
    if keyword == "":
        return ""
    # Using (case-insensitive) regexes to find titles.
    return f"(primaryTitle ~* '\y{keyword}\y' OR originalTitle ~* '\y{keyword}\y') AND "

def filter_rating(rating_range):
    min_rating, max_rating = rating_range
    return f"(averageRating >= {min_rating} AND averageRating <= {max_rating}) AND "

def filter_releaseyear(year_range):
    min_year, max_year = year_range
    return f"(year >= {min_year} AND year <= {max_year}) "

def filter_director(director):
    if director == "":
        return ""
    return f'''(id in (
            SELECT DIRECTS.mid
            FROM DIRECTORS 
            JOIN DIRECTS
            ON DIRECTORS.primaryName ~* '\y{director}\y' 
            AND DIRECTS.did = DIRECTORS.did)) AND '''

def filter_actor(actor):
    if actor == "":
        return ""
    return f'''(id in (
            SELECT STARSIN.mid
            FROM ACTORS 
            JOIN STARSIN
            ON ACTORS.primaryName ~* '\y{actor}\y' 
            AND STARSIN.aid = ACTORS.aid)) AND '''

def pick_random_movie(criteria):
    genres, keyword, rating_range, year_range, director, actor = criteria
    query = ("SELECT *\nFROM Movies\nWHERE " +
             filter_genre(genres) +
             filter_keyword(keyword) +
             filter_director(director) +
             filter_actor(actor) +
             filter_rating(rating_range) +
             filter_releaseyear(year_range) +
             "\nORDER BY random()\nLIMIT 1;")
    print(query)

    cur = conn.cursor()
    cur.execute(query)
    pick = cur.fetchone()
    if pick == None:
        return redirect(url_for('badcritiera'))
    
    return redirect(url_for('picked_movie', movie_id=pick[0]))

@app.route("/", methods=['GET', 'POST'])
def home():
    # Resetting criteria
    session['criteria'] = []
    
    # Getting 12 random movies with a rating of 7 or higher.
    twelve_rand_query = '''
        SELECT * 
        FROM Movies 
        WHERE averageRating >= 7.0
        ORDER BY random() 
        LIMIT 12;
    '''
    cur = conn.cursor()
    cur.execute(twelve_rand_query)
    movies = list(cur.fetchall())
    length = len(movies)    

    if request.method == 'POST':
        # User has clicked generate so generate random movie.
        criteria = get_criteria()
        
        # Saving which genres the user picked.
        session['criteria'] = criteria
        
        # TODO: Should save all criteria specified instead of just genres.
        return pick_random_movie(criteria)

    criteria = session.get('criteria', [])
    return render_template('index.html', criteria=criteria, content=movies, length=length)

def get_criteria():
    genres = request.form.getlist('genres')
    keyword = request.form.get('keyword', type=str)
    rating_range = (request.form.get('min_rating', 0.0, type=float),
                    request.form.get('max_rating', 10.0, type=float))
    year_range = (request.form.get('min_year', 1920, type=int), 
                  request.form.get('max_year', 2024, type=int))
    director = request.form.get('director', type=str)
    actor = request.form.get('actor', type=str)
    
    return genres, keyword, rating_range, year_range, director, actor

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/badcritiera", methods=['GET','POST'])
def badcritiera():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('badcritiera.html')

@app.route("/movie/<movie_id>", methods=['GET','POST'])
def picked_movie(movie_id):
    if request.method == 'POST':
        return pick_random_movie(session.get('criteria', []))
    
    cur = conn.cursor()
    movie_query = f'''
        SELECT *
        FROM Movies 
        WHERE id = '{movie_id}'
    '''
    cur.execute(movie_query)    
    pick = cur.fetchone()
    
    return render_template('pickedmovie.html', content=pick)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=5000)