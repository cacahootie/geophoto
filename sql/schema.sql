DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS photos;

CREATE TABLE photos (
    id varchar(32) PRIMARY KEY,
    lat double precision,
    lng double precision,
    src text
);

CREATE TABLE tags (
    id varchar(32) REFERENCES photos (id),
    tag text
);
