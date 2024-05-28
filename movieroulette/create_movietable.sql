DROP TABLE IF EXISTS Movies;

CREATE TABLE Movies(id char(10),
titleType char(10),
year int,
primaryTitle char(200),
originalTitle char(200),
runtimeMinutes int, 
genres char(60),
averageRating float,
numVotes int,
CONSTRAINT mv PRIMARY KEY (id));

copy Movies(id,titleType,year,primaryTitle,originalTitle,runtimeMinutes,genres,averageRating,numVotes)
            from '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/imdb_movie_list.csv'
            delimiter ','
            CSV HEADER;
