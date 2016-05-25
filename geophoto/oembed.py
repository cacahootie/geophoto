
from json import loads
from urlparse import urlparse

from flask import current_app as app

def oembed(url):
    path = urlparse(url).path + '' if \
        urlparse(url).path.endswith('/') else '/'
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
        "thumbnail_width": "200",
        "thumbnail_height": str(int(200 * float(3)/4)),
        "thumbnail_url": article['thumbnail'] + "?w=200&h=150&auto=compress,format",
        "html": '<div><p>' + article['headline'] + '</p><p>' + article['leader'] + '</p></div>'
    }
