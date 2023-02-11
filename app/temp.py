from urllib.parse import urlparse

o = urlparse("www.docs.python.org:80/3/library/urllib.parse.html?"
             "highlight=params#url-parsing")
print(o)
