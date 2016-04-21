DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS items;
DROP TYPE IF EXISTS itemtypes;

CREATE TYPE itemtypes AS ENUM ('photo','article');

CREATE TABLE items (
    id varchar(32) PRIMARY KEY,
    itemtype itemtypes,
    lat double precision,
    lng double precision,
    src text,
    body text
);

CREATE TABLE tags (
    id varchar(32) REFERENCES items (id),
    tag text 
);

CREATE UNIQUE INDEX name ON tags (id, tag);
