
from os import listdir, getcwd
from os.path import isfile, join
from itertools import repeat
import json
import hashlib
import subprocess

import psycopg2
import psycopg2.extras
import exifread

img_path = './geophoto/static/img/geocoded'
img_in_path = './geophoto/static/img/geocoded_in'
web_path = '/static/img/geocoded/'

conn = psycopg2.connect("dbname='geophoto'")
conn.autocommit = True

def dms_to_decimal(value, hemi):
    value = str(value).replace('[','').replace(']','').replace(' ','')
    dms = value.split(',')
    secs = dms[2].split('/')
    try:
        secs = float(secs[0]) / float(secs[1])
    except IndexError:
        secs = float(dms[2])
    retval = float(dms[0]) + float(dms[1])/60 + secs/3600
    hemi = str(hemi)
    if hemi == 'W' or hemi == 'S':
        retval *= -1.0
    return retval

def process_photos():

    in_files = set(
        f for f in listdir(img_in_path) if isfile(join(img_in_path, f))
    )
    files = in_files - set(
        f for f in listdir(img_path) if isfile(join(img_path, f))
    )

    for f in files:
        subprocess.call(
            "mogrify -path ./geophoto/static/img/geocoded -auto-orient './geophoto/static/img/geocoded_in/{}'".format(f),
            shell=True
        )

    results = []
    for i, fn in enumerate(files):
        if i % 100 == 0:
            print "Processing %i row" % i
        tags = exifread.process_file(open(join(img_path,fn)), 'rb')
        try:
            results.append({
                "src": web_path + fn,
                "lat": dms_to_decimal(tags['GPS GPSLatitude'], tags['GPS GPSLatitudeRef']),
                "lng": dms_to_decimal(tags['GPS GPSLongitude'], tags['GPS GPSLongitudeRef']),
                "id": md5(fn)
            })
        except KeyError:
            pass
    rows = (
        x for x in results
            if isinstance(x['lat'],float)
            and isinstance(x['lng'],float)
    )
    with conn.cursor() as cur:
        for i, row in enumerate(rows):
            if i % 100 == 0:
                print "Processing %i row" % i
            try:
                cur.execute("""
                    insert into photos(id, lat, lng, src)
                    VALUES (%(id)s, %(lat)s, %(lng)s, %(src)s)
                """, row)
            except psycopg2.IntegrityError:
                print row
    return results

def md5(fname):
    hf = hashlib.md5()
    with open(join(img_path,fname), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hf.update(chunk)
    return hf.hexdigest()


def photos():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            select id, lat, lng, src from photos
        """)
        return {"results": [dict(x) for x in cur] }

def tags(id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            select tag from tags
            where id = %s
        """, (id,))
        return {"results": [dict(x) for x in cur] }

def add_tags(id, tags):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.executemany("""
                insert into tags VALUES (%s, %s)
            """, zip(repeat(id), tags))
        except psycopg2.IntegrityError:
            raise ValueError("Tag already exists for this photo.")

        cur.execute("""
            select tag from tags
            where id = %s
        """, (id,))
        return {"results": [dict(x) for x in cur] }

if __name__ == '__main__':
    process_photos()
