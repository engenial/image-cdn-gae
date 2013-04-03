import webapp2
import json
import jinja2
import os
import urllib

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers
    
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
        autoescape = True)


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        context = {'upload_url': upload_url}
        template = jinja_env.get_template('index.html')
        self.response.out.write(template.render(context))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

_wsgi = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/upload', UploadHandler),
    (r'/serve/([^/]+)?', ServeHandler)
    ])

