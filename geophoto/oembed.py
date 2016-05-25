
from json import loads
from urlparse import urlparse

from flask import current_app as app

def oembed(url):
    path = '/' + urlparse(url).fragment + '/'
    with app.test_client() as c:
        rv = c.get(path)
        try:
            article = loads(rv.data)
        except ValueError:
            print url
            print path
            raise
    return {
        "success": True,
        "type": "rich",
        "version": "1.0",
        "provider_name": "Venturelog",
        "provider_url": "http://www.venturelog.io",
        "title": article['headline'],
        "author_name": "Brad Smith",
        "author_url": "http://www.venturelog.io",
        "height": "300",
        "width": "800",
        "thumbnail_width": "384",
        "thumbnail_height": "225",
        "thumbnail_url": "",
        "html": '<div><p>' + article['headline'] + '</p><p>' + article['leader'] + '</p></div>'
    }
