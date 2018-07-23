import jinja2
import webapp2
import os
import json
import urllib
import urllib2
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + "/templates"))

class LocationSearch(ndb.Model):
    city = ndb.StringProperty(required = True)
    state = ndb.StringProperty(required = True)

class LoginPage(webapp2.RequestHandler):
    def get(self):
        location_template = jinja_env.get_template('location.html')
        zipcode = self.request.get("zipcode")
        self.response.write(location_template.render(zipcode))
        
    def post(self):
        login_template = jinja_env.get_template('login.html')
        self.response.write(login_template.render())


    # def get(self):
    #     city = self.request.get("city")
    #     state = self.request.get("state")
    #     location_template = jinja_env.get_template('location.html')
    #     params = {"city": city,
    #             "state": state,
    #             }
    #     api_url = city + ", " + state
    #     api_url = "https://www.zipcodeapi.com/rest/"+ "RAU0IsJOFZxVEgTEAlllssd44GJm9euGb3gtYaAbNWxYv9f7bCFluUnLczMAA1OTr" + "/city-zips." + "json/" + city + "/" + state
    #     self.response.write(location_template.render())
    #     print api_url

app = webapp2.WSGIApplication([
    ('/login', LoginPage),
], debug=True)
