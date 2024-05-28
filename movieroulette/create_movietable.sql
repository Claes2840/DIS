DROP TABLE IF EXISTS Movies;

CREATE TABLE Movies(id varchar(10),
year int,
primaryTitle char(200),
originalTitle char(200),
runtimeMinutes int, 
genres char(60),
averageRating float,
CONSTRAINT mv PRIMARY KEY (id));

copy Movies(id,year,primaryTitle,originalTitle,runtimeMinutes,genres,averageRating)
            from '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/imdb_movie_list_scraped.csv'
            delimiter ','
            CSV HEADER;
