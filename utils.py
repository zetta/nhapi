
from datetime import datetime
from django.utils import simplejson
import urllib
import urllib2

from models import User, Post, Comment, Notification, Ticket


def fetchUrl(url,
              post_data=None,
              parameters=None,
              no_cache=None,
              use_gzip_compression=None):
  '''Fetch a URL, 
  Returns:
    A string containing the body of the response.
  '''
  http_handler  = urllib2.HTTPHandler(debuglevel=0)
  https_handler = urllib2.HTTPSHandler(debuglevel=0)

  opener = urllib2.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url)
  raw_data = response.read()
  opener.close()
  return raw_data

 

def getJson(json_url):
  json = fetchUrl(json_url)
  return simplejson.loads(json)
 
 
def put_user(nickname):
  u = User.all().filter('nickname =',nickname).fetch(1)
  if len(u) == 1:
    user = u[0]
  else:
    info = getJson("http://www.noticiashacker.com/perfil/%s.json" % nickname);
    user =  User(
      nickname = nickname,
      lowercase_nickname = nickname,
      password = 'a',
      twitter = info['twitter'],
      hnuser = info['hn'],
      github = info['github'],
      karma = info['karma']
    ).put()
  
  #if user.twitter != '' and user.avatar = '':
    #twinfo =   
    
  return user
  
def put_post(noticia,user):
  p = Post.all().filter('oid = ',noticia['id']).fetch(1)
  if len(p) == 1:
    post = p[0]
    if post.votes != noticia['votes']:
      post.votes = noticia['votes']
      calculate_karma(post)
      post.put()
  else:
    post = Post(
      oid = noticia['id'],
      votes = noticia['votes'],
      created = datetime.fromtimestamp( float(noticia['created']) ),
      url = noticia['url'],
      title = noticia['title'],
      comment_count = noticia['comment_count'],
      user = user,
      message = noticia['message'],
    )
    calculate_karma(post)
    post.put()
  return post



def calculate_karma(post):
    delta = (datetime.now() - post.created)
    seconds = delta.seconds + delta.days*86400
    hours = seconds / 3600 + 1
    votes = post.votes
    gravity = 1.8
    karma = (votes - 1) / pow((hours + 2), gravity)
    post.karma = karma 
    














