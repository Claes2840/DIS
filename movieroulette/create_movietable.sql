DROP TABLE IF EXISTS Movies;

CREATE TABLE Movies(
    id varchar(10),
    year int,
    primaryTitle varchar(255),
    originalTitle varchar(255),
    runtimeMinutes int, 
    genres varchar(60),
    averageRating float,
    posterURL varchar(255),
    PRIMARY KEY (id)
);

COPY Movies(id,year,primaryTitle,originalTitle,runtimeMinutes,genres,averageRating,posterURL)
    FROM '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/imdb_movie_list.csv'
    delimiter ','
    CSV HEADER;
