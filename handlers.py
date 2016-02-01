from flask import Flask
from flask import Request
from flask import  Response



import crawler

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/crawl_me_some_pages')
def crawl():
    crawler.crawlThem()

    return 'good!'

@app.route('/get_me_some_links')
def getLinks():

    newsPosts = crawler.takeNewsPosts()

    str = '\n'.join([np.title for np in newsPosts])

    return Response(str, mimetype='text/plain')









