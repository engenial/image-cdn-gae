import webapp2
import json
import jinja2
import os

from google.appengine.ext import db
from webapp2_extras.appengine.users import admin_required
from google.appengine.api import memcache

class Category(db.Model):
    name = db.CategoryProperty(required=True)

class ImageFile(db.Model):
    blob = db.BlobProperty(required=True)
    description = db.StringProperty()
    category = db.ReferenceProperty(Category, collection_name="images")
    date = db.DateTimeProperty(auto_now_add=True)

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
        autoescape = True)

class IndexHandler(webapp2.RequestHandler):
    @admin_required
    def get(self):
        template = jinja_env.get_template('index.html')
        self.response.out.write(template.render({'cats': Category.all()}))

class UploadHandler(webapp2.RequestHandler):
    def post(self):
        blobfile = db.Blob(self.request.get('file'))  # 'file' is file upload field in the form
        category_name = self.request.POST.get('category')
        category = Category.get_or_insert(category_name, name=category_name)
        description = self.request.POST.get('description')
        f = ImageFile(
            blob=blobfile,
            description=description,
            category=category)
        f.put()
        self.redirect('/%s' % str(category.key()))

class ServeHandler(webapp2.RequestHandler):
    @admin_required
    def get(self, c):
        category = db.get(c)
        if category:
            context = {'category': category}
            template = jinja_env.get_template('list.html')
            self.response.out.write(template.render(context))
        else:
            self.redirect('/')

class ServeImageHandler(webapp2.RequestHandler):
    def get(self, key):
        # image = db.get(key)
        # im = image.blob

        im = self.get_img(key)
        if im:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(im)
        else:
            self.response.out.write("No image")

    def get_img(self, key):
        im = memcache.get(key)
        if not im:
            im = db.get(key)
            if im:
                memcache.add(str(im.key()), im.blob, 3600*24)
                return im.blob
            else:
                return None
        else:
            return im

_wsgi = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/upload', UploadHandler),
    (r'/([^/]+)', ServeHandler),
    (r'/i/([^/]+)', ServeImageHandler)
    ])