import jinja2
import webapp2
import os
import json
import urllib
import urllib2
import base64
from google.appengine.ext import ndb
from google.appengine.api import users
from models import UserPost
from models import JUser

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + "/templates"))

# ----------------------------------------------------------------------------------
# creates and adds users to database

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

class HomePage(webapp2.RequestHandler):
    def get(self):

        user = find_or_create_user()
        log_url = get_log_inout_url(user)
        if user:
            log_message='Sign Out'

        else:
            log_message = "Sign In"


        variables = {"user": user,
                    "log_url": log_url,
                    "log_message": log_message}


        home_template = jinja_env.get_template('home.html')
        self.response.write(home_template.render(variables))

# ----------------------------------------------------------------------------------
# create post and profile page

class PostPage(webapp2.RequestHandler):
    def get(self):
        post_template = jinja_env.get_template('post.html')
        self.response.write(post_template.render())
    def post(self):
        user = users.get_current_user()
        post_user = ndb.Key('JUser', user.email())
        post_name = self.request.get("post_name")
        post_location = self.request.get("post_location")
        post_event = self.request.get("post_event")


        JUserPost = UserPost(post_user = post_user,
                            post_name = post_name,
                            post_location = post_location,
                            post_event = post_event,
                            post_user_id = user.email())
        JUserPost.put()
        self.redirect('/profile')

class ProfilePage(webapp2.RequestHandler):

    def get(self):

        juser = find_or_create_user()
        post_date = UserPost.query().order(UserPost.created_at).fetch(limit=10)
        user = find_or_create_user()
        variables = {"user": user,}

        person = find_or_create_user()
        email = person.email
        post_date = UserPost.query().filter(UserPost.post_user_id== email).order(UserPost.created_at).fetch(limit=10)
        variables = {"user": person,

                    "post_date": post_date}
        template = jinja_env.get_template("profile.html")


        if juser.profile_pic:
            variables['profilepic'] = base64.b64encode(juser.profile_pic)

        self.response.write(template.render(variables))
    def post(self):
        juser = find_or_create_user()
        if juser:
            profilepic = self.request.get("profilepic")
            juser.profile_pic = profilepic
            juser.put()
        self.redirect('/profile')

# ----------------------------------------------------------------------------------
# classes for each webpage

class CommunityPage(webapp2.RequestHandler):
    def get(self):
        community_template = jinja_env.get_template('community.html')
        self.response.write(community_template.render())

class FriendsPage(webapp2.RequestHandler):
    def get(self):
        friends_template = jinja_env.get_template('friends.html')
        self.response.write(friends_template.render())


app = webapp2.WSGIApplication([
    ('/home', HomePage),
    ('/', HomePage),
    ('/login', HomePage),
    ('/community', CommunityPage),
    ('/friends', FriendsPage),
    ('/profile', ProfilePage),
    ('/post', PostPage),
], debug=True)
