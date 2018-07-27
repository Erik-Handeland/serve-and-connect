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
from models import CommunityPost
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
            community = "Community"
            friends = "Friends"
            profile= "Profile"
            about = "About"
        else:
            log_message = "Sign In"
            community = ""
            friends = ""
            profile = ""
            about = ""


        variables = {"user": user,
                    "log_url": log_url,
                    "log_message": log_message,
                    "community": community,
                    "friends":friends,
                    "profile": profile,
                    "about": about}


        home_template = jinja_env.get_template('home.html')
        self.response.write(home_template.render(variables))

# ----------------------------------------------------------------------------------
# create post and profile page

class ProfilePostPage(webapp2.RequestHandler):
    def get(self):
        post_template = jinja_env.get_template('profile-post.html')
        self.response.write(post_template.render())

    def post(self):
        user = users.get_current_user()
        post_user = ndb.Key('JUser', user.email())
        post_name = self.request.get("post_name")
        post_location = self.request.get("post_location")
        post_event = self.request.get("post_event")
        image = self.request.get("image")
        post_date = self.request.get("post_date")


        JUserPost = UserPost(post_user = post_user,
                            post_date = post_date,
                            post_name = post_name,
                            post_location = post_location,
                            post_event = post_event,
                            post_user_id = user.email(),
                            image = image)
        JUserPost.put()
        self.redirect('/profile')

class ProfilePage(webapp2.RequestHandler):

    def get(self):
        juser = find_or_create_user()
        post_list = UserPost.query().order(UserPost.created_at).fetch(limit=10)
        user = find_or_create_user()
        variables = {"user": user,}

        person = find_or_create_user()
        email = person.email
        post_list = UserPost.query().filter(UserPost.post_user_id== email).order(-UserPost.created_at).fetch(limit=10)
        # name = post_list.query().fetch()
        for post in post_list:
            post.image = base64.b64encode(post.image)

        variables = {"user": person,
                    "post_list": post_list
                    }
        template = jinja_env.get_template("profile.html")


        if juser.profile_pic:
            variables['profilepic'] =base64.b64encode(juser.profile_pic)

        self.response.write(template.render(variables))
    def post(self):
        juser = find_or_create_user()
        if juser:
            profilepic = self.request.get("profilepic")
            juser.profile_pic = profilepic
            juser.put()
        self.redirect('/profile')

        # image = self.request.get("image")
        # if image:
        #     userpost = UserPost()
        #     userpost.image = image
        #     userpost.put()
        # self.redirect('/profile')

# ----------------------------------------------------------------------------------
# classes for each webpage and post page

class CommunityPostPage(webapp2.RequestHandler):
    def get(self):
        post_template = jinja_env.get_template('community-post.html')
        self.response.write(post_template.render())

    def post(self):
        user = users.get_current_user()
        post_date = self.request.get("post_date")
        post_user = ndb.Key('JUser', user.email())
        post_name = self.request.get("post_name")
        post_location = self.request.get("post_location")
        post_event = self.request.get("post_event")
        image = self.request.get("image")


        JUserPost = CommunityPost(post_user = post_user,
                            post_name = post_name,
                            post_date = post_date,
                            post_location = post_location,
                            post_event = post_event,
                            post_user_id = user.email(),
                            image = image)
        JUserPost.put()
        self.redirect('/community')

class CommunityPage(webapp2.RequestHandler):
    def get(self):
        search_term = self.request.get("q")
        search = search_term.lower()
        community_template = jinja_env.get_template('community.html')

        if search:
            juser = find_or_create_user()
            post_list = CommunityPost.query().filter(CommunityPost.post_location== search).order(-CommunityPost.created_at).fetch(limit=10)
            user = find_or_create_user()
            variables = {"user": user,}
            person = find_or_create_user()
            email = person.email
            for post in post_list:
                post.image = base64.b64encode(post.image)

            variables = {"user": person,
                        "post_list": post_list,
                        "search_term": search_term
                        }
            self.response.write(community_template.render(variables))

        else:
            juser = find_or_create_user()
            post_list = CommunityPost.query().order(-CommunityPost.created_at).fetch(limit=10)
            user = find_or_create_user()
            variables = {"user": user,}

            person = find_or_create_user()
            email = person.email
            for post in post_list:
                post.image = base64.b64encode(post.image)

            variables = {"user": person,
                        "post_list": post_list
                        }
            self.response.write(community_template.render(variables))

# ----------------------------------------------------------------------------------
# classes for friends page


class FriendsPage(webapp2.RequestHandler):
    def get(self):
        user = JUser.query().fetch()
        post_list = UserPost.query().order(-UserPost.created_at).fetch(limit=20)
        name = find_or_create_user()

        user_lookup = {}
        for name in user:
            user_lookup[name.email] = name

        for post in post_list:
            id = user_lookup.get(post.post_user_id)
            if id:
                post.post_nickname = id.nickname
                if id.profile_pic:
                    post.post_user_image = base64.b64encode(id.profile_pic)
                else:
                    post.post_user_image = default_user_pic
            else:
                post.post_nickname = "User"
                post.post_user_image = default_user_pic
            post.image = base64.b64encode(post.image)
        variables = {"post_list": post_list,
                    }
        friends_template = jinja_env.get_template('friends.html')
        self.response.write(friends_template.render(variables))

# ----------------------------------------------------------------------------------
# classes for each webpage

class AboutPage(webapp2.RequestHandler):
    def get(self):
        post_template = jinja_env.get_template('about.html')
        self.response.write(post_template.render())



app = webapp2.WSGIApplication([
    ('/home', HomePage),
    ('/', HomePage),
    ('/login', HomePage),
    ('/community', CommunityPage),
    ('/friends', FriendsPage),
    ('/profile', ProfilePage),
    ('/profile-post', ProfilePostPage),
    ('/community-post', CommunityPostPage),
    ('/about', AboutPage),

], debug=True)

default_user_pic = "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"
