


import urllib
import urllib2



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

 
