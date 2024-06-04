DROP TABLE IF EXISTS StarsIn;
DROP TABLE IF EXISTS Directs;

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
    originCountries varchar(1024),
    PRIMARY KEY (id)
);
COPY Movies(id,year,primaryTitle,originalTitle,runtimeMinutes,genres,averageRating,posterURL,originCountries)
    FROM '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/imdb_movie_list.csv'
    delimiter ','
    CSV HEADER;


DROP TABLE IF EXISTS Directors;
CREATE TABLE Directors(
    did varchar(10),
    primaryName varchar(255),
    PRIMARY KEY (did)
);
COPY Directors(did, primaryName)
    FROM '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/directors.csv'
    delimiter ','
    CSV HEADER;


DROP TABLE IF EXISTS Actors;
CREATE TABLE Actors(
    aid varchar(10),
    primaryName varchar(255),
    PRIMARY KEY (aid)
);
COPY Actors(aid, primaryName)
    FROM '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/actors.csv'
    delimiter ','
    CSV HEADER;

DROP TABLE IF EXISTS Genres;
CREATE TABLE Genres(
    genre varchar(11),
    PRIMARY KEY (genre));
INSERT INTO Genres VALUES
    ('Action'),
    ('Adventure'),
    ('Comedy'),
    ('Crime'),
    ('Drama'),
    ('Documentary'),
    ('Horror'),
    ('Musical'),
    ('Mystery'),
    ('News'),
    ('Romance'),
    ('Sci-Fi'),
    ('Thriller'),
    ('Animation'),
    ('Biography'),
    ('History'),
    ('Family'),
    ('Film-Noir'),
    ('Fantasy'),
    ('Music'),
    ('War'),
    ('Western'),
    ('Sport');