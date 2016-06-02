DROP SCHEMA IF EXISTS geophoto CASCADE;

CREATE SCHEMA geophoto;

CREATE TYPE geophoto.itemtypes AS ENUM ('photo','article');

CREATE TABLE geophoto.items (
    id varchar(32) PRIMARY KEY,
    itemtype geophoto.itemtypes,
    lat double precision,
    lng double precision,
    src text,
    body text
);

CREATE TABLE geophoto.tags (
    id varchar(32) REFERENCES geophoto.items (id),
    tag text 
);

CREATE UNIQUE INDEX geophototagname ON geophoto.tags (id, tag);
