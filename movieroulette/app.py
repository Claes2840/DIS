from flask import Flask, render_template, redirect, url_for, session, request, Response
from flask_caching import Cache
import psycopg2
import os

app = Flask(__name__ , static_url_path='/static')
db = "dbname='MovieRoulette' user='postgres' host='localhost' password='dis'"
conn = psycopg2.connect(db)

config = {
    "DEBUG": True,          
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 600 # 10 minutes.
}
app.config.from_mapping(config)
cache = Cache(app)

def filter_genre(genres: list[str]) -> str:
    if not genres:
        return ""
    genre_conditions = f'''\n    id IN (SELECT mid
           FROM MovieGenreAssociations M
           JOIN Genres G
           ON M.genre = G.genre AND ('''
    for genre in genres:
        genre_conditions += f"G.genre = '{genre}' OR "
    return genre_conditions[:-4] + "))\n    AND "

def filter_director(director_name: str) -> str:
    if not director_name:
        return ""
    subquery = f'''(SELECT mid 
           FROM DirectedBy
           JOIN Directors
           ON DirectedBy.did = Directors.did AND primaryName ~* '\y{director_name}\y')'''
    return f'''\n    id IN {subquery}\n    AND '''

def filter_actor(actor_name: str) -> str:
    if not actor_name:
        return ""
    subquery = f'''(SELECT mid 
           FROM StarsIn S
           JOIN Actors A
           ON S.aid = A.aid AND primaryName ~* '\y{actor_name}\y')'''
    return f'''\n    id IN {subquery}\n    AND '''

def filter_keyword(keyword: str) -> str:
    if not keyword:
        return ""
    # Using (case-insensitive) regexes to find titles.
    return f"(primaryTitle ~* '\y{keyword}\y' OR originalTitle ~* '\y{keyword}\y') \n    AND "

def filter_rating(rating_range: tuple[float, float]) -> str:
    min_rating, max_rating = rating_range
    return f"(averageRating >= {min_rating} AND averageRating <= {max_rating}) \n    AND "

def filter_releaseyear(year_range: tuple[int, int]) -> str:
    min_year, max_year = year_range
    return f"(releaseYear >= {min_year} AND releaseYear <= {max_year})\n"

def filter_runtime(runtime_range: int) -> str:
    min_runtime, max_runtime = runtime_range
    return f"(runtimeMinutes >= {min_runtime} AND runtimeMinutes <= {max_runtime}) \n    AND "
            
def filter_character(character: str) -> str:
    if not character:
        return ""
    return f'''\n    id in (SELECT mid 
           FROM StarsIn
           WHERE charactername ~* '\y{character}')\n    AND '''

def pick_random_movies(criteria: tuple) -> Response:
    if criteria:
        genres, keyword, rating_range, year_range, director, actor, character, runtime_range = criteria
        query = ("SELECT *\nFROM Movies\nWHERE " +
                filter_genre(genres) +
                filter_keyword(keyword) +
                filter_director(director) +
                filter_actor(actor) +
                filter_character(character) +
                filter_runtime(runtime_range) +
                filter_rating(rating_range) +
                filter_releaseyear(year_range) +
                "ORDER BY random();")
    else:
        query = "SELECT *\nFROM Movies\nORDER BY random();"
    cur = conn.cursor()
    cur.execute(query)
    picks = cur.fetchall()
    if not picks:
        return redirect(url_for('bad_criteria'))
    cache.set('picked_movies', picks)
    
    return redirect(url_for('picked_movie', movie_id=picks[0][0]))

def get_genres(movie_id: str) -> str:
    query = f"SELECT genre\nFROM MovieGenreAssociations\nWHERE mid = '{movie_id}'"
    cur = conn.cursor()
    cur.execute(query)    
    genres = ', '.join(map(lambda elm: elm[0], cur.fetchall()))
    return genres

def get_origin_countries(movie_id: str) -> str:
    query = f"SELECT country\nFROM OriginCountries\nWHERE mid = '{movie_id}'"
    cur = conn.cursor()
    cur.execute(query)
    countries = ', '.join(map(lambda elm: elm[0], cur.fetchall()))
    return countries

@app.route("/", methods=['GET', 'POST'])
def home() -> Response | str:
    reset_criteria = request.args.get('reset_criteria', True)
    if not reset_criteria == 'False':
        # Resetting criteria.
        session['criteria'] = []
    criteria = session.get('criteria')
    
    # Clearing data that might've been saved earlier.
    session['pick'] = None
    session['i'] = 0
    cache.set('picked_movies', [])
    
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
    movies = cur.fetchall()
    
    genres = ['' for _ in range(len(movies))]
    countries = ['' for _ in range(len(movies))]
    for i, movie in enumerate(movies):
        genres[i] = get_genres(movie[0])
        countries[i] = get_origin_countries(movie[0])

    if request.method == 'POST':
        # User has clicked 'Pick' so pick random movie.
        criteria = get_criteria()
        
        # Saving the user-specified criteria.
        session['criteria'] = criteria
        
        return pick_random_movies(criteria)
    return render_template('index.html', criteria=criteria, content=movies, genres=genres)

def get_criteria() -> tuple:
    genres = request.form.getlist('genres')
    keyword = request.form.get('keyword', type=str)
    rating_range = (request.form.get('min_rating', 0.0, type=float),
                    request.form.get('max_rating', 10.0, type=float))
    year_range = (request.form.get('min_year', 1920, type=int), 
                  request.form.get('max_year', 2024, type=int))
    director = request.form.get('director', type=str)
    actor = request.form.get('actor', type=str)
    character = request.form.get('character', type=str)
    runtime_range = (request.form.get('min_runtime', 0, type=int),
                     request.form.get('max_runtime', 467, type=int))
    
    return genres, keyword, rating_range, year_range, director, actor, character, runtime_range

@app.route("/contact")
def contact() -> str:
    return render_template('contact.html')

@app.route("/bad_criteria", methods=['GET','POST'])
def bad_criteria() -> Response | str:
    if request.method == 'POST':
        return redirect(url_for('home', reset_criteria=False))
    return render_template('bad_criteria.html')

@app.route("/movie/<movie_id>", methods=['GET','POST'])
def picked_movie(movie_id: str) -> Response | str:    
    if request.method == 'POST':
        pressed = request.form
        movies = cache.get('picked_movies')
        
        # Checking if user has clicked 'Pick another' and if there are
        # more movies to choose from given the specified criteria.
        if 'new_pick' in pressed and movies:
            # User has clicked 'Pick another' and there  
            # are other movies to pick based on criteria.
            i = session.get('i', 0)
            i = (i + 1) % len(movies)
            session['i'] = i
            return redirect(url_for('picked_movie', movie_id=movies[i][0]))
        elif 'new_criteria' in pressed:
            # User wants to update their criteria.
            return redirect(url_for('home', reset_criteria=False))
    
    cur = conn.cursor()
    movie_query = f'''
        SELECT *
        FROM Movies
        WHERE id = '{movie_id}'
    '''
    cur.execute(movie_query)    
    pick = cur.fetchone()
    genres = get_genres(movie_id)
    countries = get_origin_countries(movie_id)
    
    return render_template(
        'pickedmovie.html', content=pick, genres=genres, countries=countries)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=5000)