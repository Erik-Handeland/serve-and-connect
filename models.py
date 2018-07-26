from google.appengine.ext import ndb
import main


class JUser(ndb.Model):
    nickname =  ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    friends = ndb.StringProperty(required=False)
    profile_pic = ndb.BlobProperty()

class UserPost(ndb.Model):
    post_name = ndb.StringProperty(required = True)
    post_date = ndb.StringProperty(required = True)
    post_location = ndb.StringProperty(required = True)
    post_event = ndb.StringProperty(required = True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    image = ndb.BlobProperty(required = False)
    post_user = ndb.KeyProperty(kind=JUser)
    post_user_id = ndb.StringProperty(required = True)
    post_user_image = ndb.BlobProperty()
    post_nickname = ndb.StringProperty()

class CommunityPost(ndb.Model):
    post_name = ndb.StringProperty(required = True)
    post_date= ndb.StringProperty(required = True)
    post_location = ndb.StringProperty(required = True)
    post_event = ndb.StringProperty(required = True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    image = ndb.BlobProperty(required = False)
    post_user = ndb.KeyProperty(kind=JUser)
    post_user_id = ndb.StringProperty(required = True)
