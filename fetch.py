
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson

import utils

from models import User

class FetchHandler(webapp.RequestHandler):
  def get(self):
    json_url = 'http://www.noticiashacker.com/nuevo.json'
    js = utils.fetchUrl(json_url)
    js_object = simplejson.loads(js)
    print js_object 


def main():
  application = webapp.WSGIApplication([
      ('/tasks/fetch', FetchHandler)
  ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
