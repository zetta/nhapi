
from google.appengine.api import memcache

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
    print "user exists"
    if user.twitter != '' and user.avatar == None:
      print "updating avatar"
      twinfo = getJson("https://api.twitter.com/1/users/show/%s.json" % user.twitter)
      user.avatar = twinfo['profile_image_url']
      user.put()
  else:
    print "creating new user"
    info = getJson("http://www.noticiashacker.com/perfil/%s.json" % nickname);
    if  info['twitter'] != '':
      twinfo =  getJson("https://api.twitter.com/1/users/show/%s.json" % info['twitter'])
      avatar = twinfo['profile_image_url']
    else:
      avatar = None
    user =  User(
      nickname = nickname,
      lowercase_nickname = nickname,
      password = 'a',
      avatar = avatar,
      twitter = info['twitter'],
      hnuser = info['hn'],
      github = info['github'],
      karma = info['karma']
    ).put()
  
  return user
  
def put_post(noticia,user):
  p = Post.all().filter('oid = ',noticia['id']).fetch(1)
  if len(p) == 1:
    post = p[0]
    #if post.votes != noticia['votes']:
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
    

def post_to_json(post):
   return {
      'id':str(post.key()),
      'title':post.title,
      'message':post.message,
      'created':post.created.strftime("%s"),
      'user':post.user.nickname,
      'avatar': post.user.avatar,
      'comment_count':post.comment_count,
      'url':post.url,	  
      'votes':post.votes
   }

def get_new_posts(page):
    posts = memcache.get("new_%s" % page)
    if posts is not None:
        return posts
    else:
        perPage = 20
        page = int(page) if page else 1
        realPage = page - 1
        if realPage > 0:
          prevPage = realPage
        posts = Post.all().order('-created').fetch(perPage, realPage * perPage)
        memcache.add("new_%d" % page, posts, 250)
    return posts

def get_top_posts(page):
    posts = memcache.get("top_%s" % page)
    if posts is not None:
        return posts
    else:
        perPage = 20
        page = int(page) if page else 1
        realPage = page - 1
        if realPage > 0:
          prevPage = realPage
        posts = Post.all().order('-karma').fetch(perPage, realPage * perPage)
        memcache.add("new_%d" % page, posts, 250)
    return posts











