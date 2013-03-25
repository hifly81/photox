'''
Created on Feb 23, 2013

@author: hifly
'''

import urllib
import simplejson
import logging
import logging.config

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger('photoOrganizer')

#constants
TWEET_RESULTS = "results"
TWEET_ENTITIES = "entities"
TWEET_MEDIA = "media"
TWEET_FROMUSER = "from_user"
TWEET_TEXT = "text"
TWEET_CREATEDAT = "created_at"
TWEET_MEDIAURLHTTPS = "media_url_https"
TWITTER_SEARCH_QUERY = "http://search.twitter.com/search.json?q="

#wrapper for twitter search results
class TwitterSearchResult:    
  def __init__(self):
    self.query = None
    self.entries = []

#twitter entry derived from a search
class TwitterEntry:
  def __init__(self):
    #attributes extracted from twitter result
    self.author = None
    self.text = None 
    self.url = None
    self.creationDate = None

def searchMediaTweets(query,numberOfTweets):
    #urlencoding
    queryEncoded = urllib.quote(query)
    try:
        #search with rpp attribute
        search = urllib.urlopen(TWITTER_SEARCH_QUERY+queryEncoded+"&rpp="+str(numberOfTweets)+"&include_entities=true")
    except Exception as inst:
       x, y = inst.args
       logger.error("Error in search %s %s",x,y)
       raise Exception("Can't contact twitter url. Check your internet connection!")
    dict = simplejson.loads(search.read())
    twitterSearchResult = TwitterSearchResult()
    for result in dict[TWEET_RESULTS]: 
        for entities in result[TWEET_ENTITIES]:
            if(entities==TWEET_MEDIA):
                for subEntities in result[TWEET_ENTITIES][entities]:   
                    twitterEntry =  TwitterEntry()
                    twitterEntry.author = result[TWEET_FROMUSER]
                    twitterEntry.text = result[TWEET_TEXT]
                    twitterEntry.creationDate = result[TWEET_CREATEDAT]
                    twitterEntry.url = subEntities[TWEET_MEDIAURLHTTPS]
                    twitterSearchResult.entries.append(twitterEntry)
    return twitterSearchResult 