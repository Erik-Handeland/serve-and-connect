from google.appengine.ext import ndb

class UserPost(ndb.Model):
    post_event = ndb.StringProperty(required = True)
    post_location = ndb.StringProperty(required = True)
    picture_id = ndb.StringProperty(required = False)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
