from google.appengine.ext import ndb
import main


class JUser(ndb.Model):
    nickname =  ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    bio = ndb.StringProperty(required=False)

class UserPost(ndb.Model):
    post_name = ndb.StringProperty(required = True)
    post_location = ndb.StringProperty(required = True)
    post_event = ndb.StringProperty(required = True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    image = ndb.BlobProperty()
