from flask import Flask, render_template, redirect, url_for, session, request
import psycopg2
import os

app = Flask(__name__ , static_url_path='/static')
db = "dbname='MovieRoulette' user='postgres' host='localhost' password='dis'"
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
            
def filter_character(character):
    if character == "":
        return ""
    return f'''\n    id in (SELECT mid 
           FROM StarsIn
           WHERE charactername ~* '\y{character}')\n    AND '''

def pick_random_movie(criteria):
    if criteria:
        genres, keyword, rating_range, year_range, director, actor, character = criteria
        query = ("SELECT *\nFROM Movies\nWHERE " +
                filter_genre(genres) +
                filter_keyword(keyword) +
                filter_director(director) +
                filter_actor(actor) +
                filter_character(character) +
                filter_rating(rating_range) +
                filter_releaseyear(year_range) +
                "ORDER BY random()\nLIMIT 1;")
    else:
        query = "SELECT *\nFROM Movies\nORDER BY random()\nLIMIT 1;"
    print(query)
    cur = conn.cursor()
    cur.execute(query)
    pick = cur.fetchone()
    if pick == None:
        return redirect(url_for('bad_criteria'))
    return redirect(url_for('picked_movie', movie_id=pick[0]))
        

@app.route("/", methods=['GET', 'POST'])
def home():
    reset_criteria = request.args.get('reset_criteria', True)
    criteria = session.get('criteria')
    if reset_criteria:
        # Resetting criteria.
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
        
        # Saving the user-specified criteria.
        session['criteria'] = criteria
        
        return pick_random_movie(criteria)
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
    character = request.form.get('character', type=str)
    
    return genres, keyword, rating_range, year_range, director, actor, character

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/bad_criteria", methods=['GET','POST'])
def bad_criteria():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('bad_criteria.html')

@app.route("/movie/<movie_id>", methods=['GET','POST'])
def picked_movie(movie_id):
    if request.method == 'POST':
        pressed = request.form
        if 'new_pick' in pressed:
            return pick_random_movie(session.get('criteria'))
        elif 'new_criteria' in pressed:
            return redirect(url_for('home', reset_criteria=False))
    
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