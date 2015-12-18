
from os import listdir, getcwd
from os.path import isfile, join

import exifread

img_path = './geophoto/static/img/geocoded'
web_path = '/static/img/geocoded/'

def dms_to_decimal(value):
    value = str(value).replace('[','').replace(']','').replace(' ','')
    dms = value.split(',')
    print dms
    secs = dms[2].split('/')
    try:
        secs = float(secs[0]) / float(secs[1])
    except IndexError:
        secs = float(dms[2])
    retval = float(dms[0]) + float(dms[1])/60 + secs/3600
    print retval
    return retval

def photos():
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
                    "id": fn
                })
            except KeyError:
                pass
    return {"results":results}