from flask import Flask, render_template, redirect, url_for, session, request
import psycopg2
import os

app = Flask(__name__ , static_url_path='/static')
db = "dbname='MovieRoulette' user='postgres' host='localhost' password='Lykkehvid123'"
conn = psycopg2.connect(db)

def filter_genre(genres):
    if not genres:
        return ""
    genre_conditions = f'''\n    id IN (SELECT mid
           FROM MovieGenreAssociations M
           JOIN Genres G
           ON M.genre = G.genre AND ('''
    for genre in genres:
        genre_conditions += f"G.genre = '{genre}' OR "
    return genre_conditions[:-4] + "))\n    AND "

def filter_director(director_name):
    if director_name == "":
        return ""
    subquery = f'''(SELECT mid 
           FROM Directs
           JOIN Directors
           ON Directs.did = Directors.did AND primaryName ~* '\y{director_name}\y')'''
    return f'''\n    id IN {subquery}\n    AND '''

def filter_actor(actor_name):
    if actor_name == "":
        return ""
    subquery = f'''(SELECT mid 
           FROM StarsIn S
           JOIN Actors A
           ON S.aid = A.aid AND primaryName ~* '\y{actor_name}\y')'''
    return f'''\n    id IN {subquery}\n    AND '''

def filter_keyword(keyword):
    if keyword == "":
        return ""
    # Using (case-insensitive) regexes to find titles.
    return f"(primaryTitle ~* '\y{keyword}\y' OR originalTitle ~* '\y{keyword}\y') \n    AND "

def filter_rating(rating_range):
    min_rating, max_rating = rating_range
    return f"(averageRating >= {min_rating} AND averageRating <= {max_rating}) \n    AND "

def filter_releaseyear(year_range):
    min_year, max_year = year_range
    return f"(year >= {min_year} AND year <= {max_year})\n"

def pick_random_movie(criteria):
    genres, keyword, rating_range, year_range, director, actor = criteria
    query = ("SELECT *\nFROM Movies\nWHERE " +
             filter_genre(genres) +
             filter_keyword(keyword) +
             filter_director(director) +
             filter_actor(actor) +
             filter_rating(rating_range) +
             filter_releaseyear(year_range) +
             "ORDER BY random()\nLIMIT 1;")
    print(query)

    cur = conn.cursor()
    cur.execute(query)
    pick = cur.fetchone()
    if pick == None:
        # TODO: PRINT TIL BRUGEREN AT DER IKKE FINDES EN FILM.
        return redirect(url_for('bad_criteria'))
    
    return redirect(url_for('picked_movie', movie_id=pick[0]))

@app.route("/", methods=['GET', 'POST'])
def home():
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
                  request.form.get('max_year', 2024, type=int))
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