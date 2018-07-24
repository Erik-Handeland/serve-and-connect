import jinja2
import webapp2
import os
import json
import urllib
import urllib2
from google.appengine.api import users

from google.appengine.ext import ndb
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + "/templates"))
        
@ndb.transactional
def find_or_create_user():
    user = users.get_current_user()
    if user:
        key = ndb.Key('UserInfo', user.user_id())
        stuser = key.get()
        if not stuser:
            stuser = UserInfo(key=key, nickname=user.nickname())
        stuser.put()
        return stuser;
    return None
def get_log_inout_url(user):
    if user:
        return users.create_logout_url('/')
    else:
        return users.create_login_url('/')


class IndexPage(webapp2.RequestHandler):
    def get(self):
        index_template = jinja_env.get_template('index.html')
        self.response.write(index_template.render())

class PersonPage(ndb.Model):
        print("hello world")
        name = ndb.StringProperty(required=True)
        email = ndb.StringProperty(required=True)
        user_id = ndb.IntegerProperty(required=False)


class LoginPage(webapp2.RequestHandler):
    def get(self):
        login_template = jinja_env.get_template('login.html')
        zipcode = self.request.get("zipcode")
        self.response.write(login_template.render())

    def post(self):
        community_template = jinja_env.get_template('community.html')
        self.response.write(community_template.render())

class CommunityPage(webapp2.RequestHandler):
    def get(self):
        community_template = jinja_env.get_template('community.html')
        self.response.write(community_template.render())

class FriendsPage(webapp2.RequestHandler):
    def get(self):
        friends_template = jinja_env.get_template('friends.html')
        self.response.write(friends_template.render())

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('profile.html')
        self.response.write(profile_template.render())


app = webapp2.WSGIApplication([
    ('/login', LoginPage),
    ('/home', CommunityPage),
    ('/community', CommunityPage),
    ('/friends', FriendsPage),
    ('/profile', ProfilePage),
    ('/index', IndexPage),
], debug=True)
