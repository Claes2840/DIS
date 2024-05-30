from flask import Flask, render_template, redirect, url_for, session, request
import psycopg2
import os

app = Flask(__name__ , static_url_path='/static')
db = "dbname='MovieRoulette' user='postgres' host='localhost' password='Lykkehvid123'"
conn = psycopg2.connect(db)
cursor = conn.cursor()

def genre_filter(genres):
    sql = '''('''
    for genre in genres:
        sql += f'''genres ~ '{genre}' OR '''
    return sql[:-3] + ''')'''

def keyword_filter(keyword):
    # Using (case-insensitive) regexes to find titles.
    return f'''
        (primarytitle ~* '{keyword}' OR originaltitle ~* '{keyword}') AND 
    '''

def releaseyear_filter(year):
    return f'''(year = {year}) '''


def pick_random_movie(genres, keyword, releaseyear):
    sqlcode = '''SELECT id FROM MOVIES WHERE '''
    cond = False
    if not (genres == []):
        cond = True
        sqlcode += genre_filter(genres) + ''' AND '''
    if not (keyword == ''):
        cond = True
        sqlcode += keyword_filter(keyword) + ''' AND '''
    if not (releaseyear == None):
        cond = True
        sqlcode += releaseyear_filter(releaseyear) + ''' AND '''
    
    if (cond):
        sqlcode = sqlcode[:-4]
    else:
        sqlcode = sqlcode[:-6]
    sqlcode += ''' ORDER BY random() LIMIT 1;'''
    print(sqlcode)
    curr = conn.cursor()
    curr.execute(sqlcode)
    movieid = (curr.fetchone())
    if (movieid == None):
        #PRINT TIL BRUGEREN AT DER IKKE FINDES EN FILM
        return redirect(url_for('home'))
    
    return redirect(url_for('picked_movie', movieid=movieid[0]))


@app.route("/", methods=['GET', 'POST'])
def home():
    curr = conn.cursor()
    # Getting 10 random rows from Movies
    twelve_rand = '''
        SELECT * FROM Movies WHERE averageRating >= 8.0 ORDER BY random() LIMIT 12;
    '''
    curr.execute(twelve_rand)
    movies = list(curr.fetchall())
    length = len(movies)    

    if request.method == 'POST':
        genres_picked = request.form.getlist('genres')
        keyword = request.form.get('keyword', type=str)
        releaseyear = request.form.get('releaseyear', type=int)
        
        # Saving which genres the user picked.
        session['genres_picked'] = genres_picked
        
        return pick_random_movie(genres_picked, keyword, releaseyear)

    genres_picked = session.get('genres_picked', [])
    return render_template('index.html', genres_picked=genres_picked, content=movies, length=length)

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/pickedmovie/<movieid>")
def picked_movie(movieid):
    #Tilføj en ekstra knap 'generate' som generere en ny film ud fra de samme kritier
    cur = conn.cursor()
    pick_movie = f'''SELECT * FROM Movies WHERE id= '{movieid}' '''
    cur.execute(pick_movie)    
    pick = cur.fetchone()
    
    # Resetting the previously selected options.
    session['genres_picked'] = []
    
    return render_template('pickedmovie.html', content=pick)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=5003)