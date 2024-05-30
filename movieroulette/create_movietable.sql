DROP TABLE IF EXISTS Movies;

CREATE TABLE Movies(id varchar(10),
year int,
primaryTitle varchar(200),
originalTitle varchar(200),
runtimeMinutes int, 
genres varchar(60),
averageRating float,
PRIMARY KEY (id));

copy Movies(id,year,primaryTitle,originalTitle,runtimeMinutes,genres,averageRating)
            from '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/imdb_movie_list_scraped.csv'
            delimiter ','
            CSV HEADER;
