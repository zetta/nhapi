from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils.html import escape
from django.utils import simplejson

import utils

from models import User, Post, Comment, Notification, Ticket

class MainHandler(webapp.RequestHandler):
  def get(self):
    page = escape(self.request.get('page'))
    posts = utils.get_top_posts(page)

    posts_json = [utils.post_to_json(p) for p in posts]
    if(self.request.get('callback')):
      self.response.headers['Content-Type'] = "application/javascript"
      self.response.out.write(self.request.get('callback')+'('+simplejson.dumps({'posts':posts_json})+');')
    else:
      self.response.headers['Content-Type'] = "application/json"
      self.response.out.write(simplejson.dumps({'posts':posts_json}))

class NewHandler(webapp.RequestHandler):
  def get(self):
    page = escape(self.request.get('page'))
    posts = utils.get_new_posts(perPage, realPage)
    
    posts_json = [utils.post_to_json(p) for p in posts]
    if(self.request.get('callback')):
      self.response.headers['Content-Type'] = "application/javascript"
      self.response.out.write(self.request.get('callback')+'('+simplejson.dumps({'posts':posts_json})+');')
    else:
      self.response.headers['Content-Type'] = "application/json"
      self.response.out.write(simplejson.dumps({'posts':posts_json}))


def main():
  application = webapp.WSGIApplication([
      ('/.json', MainHandler),
      ('/new.json', NewHandler)
  ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
