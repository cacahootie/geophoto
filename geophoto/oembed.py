
from json import loads
from urlparse import urlparse

from flask import current_app as app
from flask import request

def thumbUrl(thumb):
    return "https://venturelog.imgix.net/articles/" + thumb + \
        "?w=200&h=150&fit=crop&crop=entropy&auto=compress,format"

def html(article):
    return '<div><p>' + article['headline'] + '</p><p>' + article['leader'] + '</p></div>'

def oembed(url):
    path = urlparse(url).path + "?format=json"
    with app.test_client() as c:
        rv = c.get(path)
        try:
            article = loads(rv.data)
        except ValueError:
            print url
            print path
            raise
    if request.args.get("format") == "html":
        return html(article)
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
        "thumbnail_url": thumbUrl(article['thumbnail']),
        "html": html(article)
    }
