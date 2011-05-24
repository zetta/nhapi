
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson

import utils

from models import User, Post, Comment, Notification, Ticket

class FetchHandler(webapp.RequestHandler):
  def get(self):
  
     #usuarios_twitter = utils.getJson("http://www.noticiashacker.com/api/usuarios/twitter");
  
    #print "hola"
  
    for n in range(1, 11): 
      json_url = 'http://www.noticiashacker.com/nuevo.json?pagina=%d'
      noticias = utils.getJson(json_url % n)    
   
      for noticia in noticias['posts']:
         user = utils.put_user(noticia['user'])
         post = utils.put_post(noticia,user)

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write( 'finish' )


def main():
  application = webapp.WSGIApplication([
      ('/tasks/fetch', FetchHandler)
  ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
