import logging
import hashlib
#import keys

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
#from gaesessions import get_current_session
from urlparse import urlparse
from datetime import datetime





class User(db.Model):
  lowercase_nickname  = db.StringProperty(required=True)
  nickname            = db.StringProperty(required=True)
  password            = db.StringProperty(required=True)
  created             = db.DateTimeProperty(auto_now_add=True)
  last_modified       = db.DateTimeProperty(auto_now=True)
  about               = db.TextProperty(required=False)
  hnuser              = db.StringProperty(required=False, default="")
  github              = db.StringProperty(required=False, default="")
  location            = db.StringProperty(required=False, default="")
  twitter             = db.StringProperty(required=False, default="")
  email               = db.EmailProperty(required=False)
  url                 = db.LinkProperty(required=False)
  admin               = db.BooleanProperty(default=False)
  karma               = db.IntegerProperty(required=False)
  avatar              = db.StringProperty(required=False)
  
class Post(db.Model):
  oid           = db.StringProperty(required=True)
  title         = db.StringProperty(required=True)
  url           = db.LinkProperty(required=False)
  message       = db.TextProperty()
  user          = db.ReferenceProperty(User, collection_name='posts')
  created       = db.DateTimeProperty(auto_now_add=True)
  karma         = db.FloatProperty()
  edited        = db.BooleanProperty(default=False)
  twittered     = db.BooleanProperty(default=False)
  votes         = db.IntegerProperty(required=False)
  comment_count = db.IntegerProperty(required=False)
   
class Comment(db.Model):
  message = db.TextProperty()
  user    = db.ReferenceProperty(User, collection_name='comments')
  post    = db.ReferenceProperty(Post, collection_name='comments')
  father  = db.SelfReferenceProperty(collection_name='childs')
  created = db.DateTimeProperty(auto_now_add=True)
  karma   = db.FloatProperty()
  edited  = db.BooleanProperty(default=False)


#class Vote(db.Model):
#  user        = db.ReferenceProperty(User, collection_name='votes')
#  target_user = db.ReferenceProperty(User, collection_name='received_votes')
#  post        = db.ReferenceProperty(Post, collection_name='votes')
#  comment     = db.ReferenceProperty(Comment, collection_name='votes')
#  created     = db.DateTimeProperty(auto_now_add=True)

class Notification(db.Model):
  target_user = db.ReferenceProperty(User, collection_name='notifications')
  sender_user = db.ReferenceProperty(User, collection_name='send_notifications')
  post        = db.ReferenceProperty(Post)
  comment     = db.ReferenceProperty(Comment)
  created     = db.DateTimeProperty(auto_now_add=True)
  read        = db.BooleanProperty(default=False)
  
  
class Ticket(db.Model):
  user        = db.ReferenceProperty(User, collection_name='tickets')
  is_active   = db.BooleanProperty(default=True)
  code        = db.StringProperty(required=True)
  created     = db.DateTimeProperty(auto_now_add=True)
  










