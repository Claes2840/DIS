START TRANSACTION;

DROP TABLE IF EXISTS StarsIn;
CREATE TABLE StarsIn(
    mid varchar(10),
    aid varchar(10),
    characterName varchar(255),
    PRIMARY KEY (mid, aid, characterName),
    FOREIGN KEY (mid) REFERENCES Movies,
    FOREIGN KEY (aid) REFERENCES Actors
);
COPY StarsIn(mid, aid, characterName)
    FROM '/Users/claes/DIS/Afleveringer/DIS/movieroulette/tmp/stars_in.csv'
    delimiter ','
    CSV HEADER;

DROP TABLE IF EXISTS Directs;
CREATE TABLE Directs(
    mid varchar(10),
    did varchar(10),
    PRIMARY KEY (mid, did),
    FOREIGN KEY (mid) REFERENCES Movies,
    FOREIGN KEY (did) REFERENCES Directors    
);
COPY Directs(mid, did)
    FROM '/Users/claes/DIS/Afleveringer/DIS/movieroulette/tmp/directs.csv'
    delimiter ','
    CSV HEADER;

DROP TABLE IF EXISTS MovieGenreAssociations;
CREATE TABLE MovieGenreAssociations(
    mid varchar(10),
    genre varchar(11),
    PRIMARY KEY (mid, genre),
    FOREIGN KEY (mid) REFERENCES Movies,
    FOREIGN KEY (genre) REFERENCES Genres
);
COPY MovieGenreAssociations(mid, genre)
    FROM '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/movie_genre_associations.csv'
    delimiter ','
    CSV HEADER;

DROP TABLE IF EXISTS MovieCountryAssociations;
CREATE TABLE MovieCountryAssociations(
    mid varchar(10),
    country varchar(32),
    PRIMARY KEY (mid, country),
    FOREIGN KEY (mid) REFERENCES Movies,
    FOREIGN KEY (country) REFERENCES Countries
);
COPY MovieCountryAssociations(mid, country)
    FROM '/Users/jacobsiegumfeldt/Desktop/DIS/Project/movieroulette/tmp/movie_country_associations.csv'
    delimiter ','
    CSV HEADER;

COMMIT;