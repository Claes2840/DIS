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
    FROM 'path/to/tmp/stars_in.csv'
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
    FROM 'path/to/tmp/directs.csv'
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
    FROM 'path/to/tmp/movie_genre_associations.csv'
    delimiter ','
    CSV HEADER;

DROP TABLE IF EXISTS OriginCountries;
CREATE TABLE OriginCountries(
    mid varchar(10),
    country varchar(32),
    PRIMARY KEY (mid, country),
    FOREIGN KEY (mid) REFERENCES Movies,
    FOREIGN KEY (country) REFERENCES Countries
);
COPY OriginCountries(mid, country)
    FROM 'path/to/tmp/origin_countries.csv'
    delimiter ','
    CSV HEADER;