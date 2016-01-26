
from os import listdir, getcwd
from os.path import isfile, join
import json
import hashlib

import psycopg2
import exifread

img_path = './geophoto/static/img/geocoded'
web_path = '/static/img/geocoded/'

conn = psycopg2.connect("dbname='geophoto'")
conn.autocommit = True

def dms_to_decimal(value):
    value = str(value).replace('[','').replace(']','').replace(' ','')
    dms = value.split(',')
    secs = dms[2].split('/')
    try:
        secs = float(secs[0]) / float(secs[1])
    except IndexError:
        secs = float(dms[2])
    return float(dms[0]) + float(dms[1])/60 + secs/3600

def process_photos():
    files = (
        f for f in listdir(img_path) if isfile(join(img_path, f))
    )
    results = []
    for fn in files:
        tags = exifread.process_file(open(join(img_path,fn)), 'rb')
        for tag in tags:
            try:
                results.append({
                    "src": web_path + fn,
                    "lat": dms_to_decimal(tags['GPS GPSLatitude']),
                    "lng": dms_to_decimal(tags['GPS GPSLongitude']),
                    "id": md5(fn)
                })
            except KeyError:
                pass
    rows = [
        {
            'id': x['id'],
            'lat': x['lat'],
            'lng': x['lng'],
            'doc': json.dumps(x)
        } for x in results
        if isinstance(x['lat'],float)
        and isinstance(x['lng'],float)
    ]
    with conn.cursor() as cur:
        for row in rows:
            try:
                cur.execute("""
                    insert into photos(id, lat, lng, doc)
                    VALUES (%(id)s, %(lat)s, %(lng)s, %(doc)s)
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
    #return {"results": process_photos()}
    with conn.cursor() as cur:
        cur.execute("""
            select doc from photos
        """)
        return {"results": [dict(x[0]) for x in cur] }

if __name__ == '__main__':
    process_photos()