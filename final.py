import webapp2
import jinja2
import re
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

global newurl

'''def render_str(self, template, **params):
        params['user'] = self.user
        t = jinja_env.get_template(template)
        return t.render(params)'''

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

'''class WikiHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		return render_str(template, **params)    

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))'''

class Wiki(db.Model):
	content = db.StringProperty(required = True)
	urlold = db.StringProperty(required = True)

class EditPage(webapp2.RequestHandler):
	#def render_form(self, error=""):
		#self.render("form.html", error = error)


	def get(self):
		self.render("edit.html")

	def post(self):
		global newurl
		content = self.request.get('content')
		editurl = self.request.path
		str1 = editurl.split('/')
		newurl= str1[1]

		if content:
			a = Wiki(content = content, urlold = newurl)
			a.put()
			self.redirect("/%s"%newurl)
		else:
			template_values = {
				'error':"Content is required, please!",
			}
			template = jinja_environment.get_template('edit.html')
			self.response.out.write(template.render(template_values))
			#error = "Content is required, please!"
			#self.render_form("edit.html", error=error)
		
class WikiPage(webapp2.RequestHandler):
	def get(self):
		ur = self.request.path

		if ur:
			ur1 = db.GqlQuery("SELECT * FROM Wiki WHERE urlold = ur")
			if ur1:
				template_values = {
					'ur1':ur1,
				}
				template = jinja_environment.get_template('wikipost.html')
				self.response.out.write(template.render(template_values))
				#self.render("wikipost.html", ur1 = ur1)
			else:
				self.redirect("/_edit/%s"%ur)

		
		

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Welcome to my wiki")

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/_edit' + PAGE_RE, EditPage),
                               (PAGE_RE, WikiPage),
                               ],
                              debug=True)