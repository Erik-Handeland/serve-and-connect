import jinja2
import webapp2
import os
import json
import urllib
import urllib2
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + "/templates"))

# ----------------------------------------------------------------------------------

def find_or_create_user():
     user = users.get_current_user()
     if user:
         key = ndb.Key('JUser', user.user_id())
         juser = key.get()
         if not juser:
             juser = JUser(key=key,
                            nickname=user.nickname(),
                           email=user.email()
                           )
         juser.put()
         return juser;
     return None

def get_log_inout_url(user):
     if user:
         return users.create_logout_url('/')
     else:
         return users.create_login_url('/')

class JUser(ndb.Model):
    nickname =  ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    bio = ndb.StringProperty(required=False)

class LoginPage(webapp2.RequestHandler):
    def get(self):

        user = find_or_create_user()
        log_url = get_log_inout_url(user)

        variables = {"user": user,
                    "log_url": log_url}


        template = jinja_env.get_template("login.html")
        self.response.write(template.render(variables))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = find_or_create_user()
        variables = {"user": user}
        template = jinja_env.get_template("profile2.html")
        self.response.write(template.render(variables))


    def post(self):
        user = find_or_create_user()
        bio = self.request.get("bio")
        user.bio = bio
        user.put()

        variables = {"user": user}
        template = jinja_env.get_template("profile2.html")
        self.response.write(template.render(variables))

# ----------------------------------------------------------------------------------

class HomePage(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('home.html')
        self.response.write(home_template.render())

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
    ('/login2', ProfileHandler),
    ('/home', CommunityPage),
    ('/community', CommunityPage),
    ('/friends', FriendsPage),
    ('/profile', ProfilePage),
    ('/', HomePage),
], debug=True)
