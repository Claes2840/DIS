DROP TABLE IF EXISTS StarsIn;
DROP TABLE IF EXISTS Directs;
DROP TABLE IF EXISTS MovieGenreAssociations;
DROP TABLE IF EXISTS OriginCountries;

DROP TABLE IF EXISTS Movies;
CREATE TABLE Movies(
    id varchar(10),
    releaseYear int,
    primaryTitle varchar(255),
    originalTitle varchar(255),
    runtimeMinutes int, 
    averageRating float,
    posterURL varchar(255),
    PRIMARY KEY (id)
);
COPY Movies(id,releaseYear,primaryTitle,originalTitle,runtimeMinutes,averageRating,posterURL)
    FROM 'path/to/tmp/movies.csv'
    delimiter ','
    CSV HEADER;


DROP TABLE IF EXISTS Directors;
CREATE TABLE Directors(
    did varchar(10),
    primaryName varchar(255),
    PRIMARY KEY (did)
);
COPY Directors(did, primaryName)
    FROM 'path/to/tmp/directors.csv'
    delimiter ','
    CSV HEADER;


DROP TABLE IF EXISTS Actors;
CREATE TABLE Actors(
    aid varchar(10),
    primaryName varchar(255),
    PRIMARY KEY (aid)
);
COPY Actors(aid, primaryName)
    FROM 'path/to/tmp/actors.csv'
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
    ('Horror'),
    ('Musical'),
    ('Mystery'),
    ('Romance'),
    ('Sci-Fi'),
    ('Thriller'),
    ('Animation'),
    ('Biography'),
    ('History'),
    ('Family'),
    ('Fantasy'),
    ('War'),
    ('Western'),
    ('Sport'),
    ('Music'),
    ('News'),
    ('Documentary'),
    ('Film-Noir');

DROP TABLE IF EXISTS Countries;
CREATE TABLE Countries(
    country varchar(32),
    PRIMARY KEY (country));
INSERT INTO Countries VALUES
    ('Gambia'),
    ('Philippines'),
    ('Tunisia'),
    ('Australia'),
    ('United Kingdom'),
    ('France'),
    ('Luxembourg'),
    ('Sweden'),
    ('Pakistan'),
    ('Liechtenstein'),
    ('China'),
    ('Netherlands Antilles'),
    ('Nepal'),
    ('Ghana'),
    ('Colombia'),
    ('Cuba'),
    ('Kazakhstan'),
    ('Austria'),
    ('Iran'),
    ('Switzerland'),
    ('Yugoslavia'),
    ('Morocco'),
    ('Jordan'),
    ('Bahrain'),
    ('North Macedonia'),
    ('Mauritania'),
    ('Brazil'),
    ('Ukraine'),
    ('Aruba'),
    ('Canada'),
    ('United Arab Emirates'),
    ('The Democratic Republic of Congo'),
    ('Federal Republic of Yugoslavia'),
    ('Romania'),
    ('Ireland'),
    ('Spain'),
    ('Uruguay'),
    ('Indonesia'),
    ('Turkey'),
    ('Croatia'),
    ('Botswana'),
    ('Hong Kong'),
    ('Russia'),
    ('Soviet Union'),
    ('Netherlands'),
    ('Puerto Rico'),
    ('Iceland'),
    ('Hungary'),
    ('Malaysia'),
    ('South Korea'),
    ('Kenya'),
    ('Lithuania'),
    ('Germany'),
    ('Chile'),
    ('Venezuela'),
    ('Zimbabwe'),
    ('Saudi Arabia'),
    ('Estonia'),
    ('Bosnia and Herzegovina'),
    ('Guatemala'),
    ('Finland'),
    ('New Zealand'),
    ('Paraguay'),
    ('Zambia'),
    ('Lebanon'),
    ('Czech Republic'),
    ('Monaco'),
    ('Slovenia'),
    ('Taiwan'),
    ('Bangladesh'),
    ('North Korea'),
    ('Serbia and Montenegro'),
    ('Algeria'),
    ('Japan'),
    ('Thailand'),
    ('Occupied Palestinian Territory'),
    ('Bulgaria'),
    ('Malawi'),
    ('Iraq'),
    ('Italy'),
    ('Isle of Man'),
    ('Kuwait'),
    ('Czechoslovakia'),
    ('Israel'),
    ('Panama'),
    ('United States'),
    ('Georgia'),
    ('South Africa'),
    ('Belarus'),
    ('Malta'),
    ('Cambodia'),
    ('Latvia'),
    ('Libya'),
    ('Serbia'),
    ('Slovakia'),
    ('Macao'),
    ('Singapore'),
    ('Denmark'),
    ('Mexico'),
    ('Ecuador'),
    ('Greece'),
    ('Qatar'),
    ('Cyprus'),
    ('Poland'),
    ('Peru'),
    ('India'),
    ('Bahamas'),
    ('Belgium'),
    ('West Germany'),
    ('Argentina'),
    ('Portugal'),
    ('Norway'),
    ('Egypt'),
    ('Vietnam');    