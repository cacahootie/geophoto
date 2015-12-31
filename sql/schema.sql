DROP TABLE IF EXISTS PHOTOS;

CREATE TABLE photos (
    id varchar(32) PRIMARY KEY,
    lat double precision,
    lng double precision,
    doc JSONB
);
