from pdb import set_trace as st

import re
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import cgi

import bleach

import db_iface

PORT = 8080

class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = """
                <html><body>hiya
                <form method='POST' enctype='multipart/form-data'
                action='/hello'><h2>What to say?</h2>
                <input name='message' type='text'>
                <input type='submit' value='Submit'>
                </body></html>"""
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/nihao'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = """
                <html><body>nihao
                <a href="/hello">back to hello</a>
                </body></html>
                """
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_div = """
                <div>
                <h2>{name}<h2>
                <a href="/restaurants/{id}/edit">edit</a>
                <a href="/restaurants/{id}/delete">delete</a>
                </div>
                """
                output = """
                <html><body>
                %s
                <a href="/restaurants/new">Create restaurant"</a>
                </body></html>
                """ % '\n'.join(
                    [restaurant_div.format(
                        name=restaurant.name,
                        id=restaurant.id)
                     for restaurant in db_iface.get_restaurants()]
                )
                self.wfile.write(output)
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = """
                <html><body>
                <form method='POST' enctype='multipart/form-data'
                 action='/restaurants/new'><h2>Restaurant name?</h2>
                <input name='restaurant-name' type='text'>
                <input type='submit' value='Submit'>
                </form>
                </html></body>
                """
                self.wfile.write(output)
                return

            mo = re.match(r'^/restaurants/(\d+)/edit$', self.path)
            if mo is not None:
                restaurant_id = mo.group(1)
                restaurant = db_iface.get_restaurant(restaurant_id)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output_template = """
                <html><body>
                <form method="POST" enctype="multipart/form-data"
                 action="/restaurants/{id}/edit">
                <h2>{name}</h2>
                <input name="restaurant-name" type="text"
                placeholder="{name}">
                <input type="submit" value="Submit">
                </form>
                </html></body>
                """
                output = output_template.format(
                    name=bleach.clean(restaurant.name
                                  ).replace('"', '\"'),
                    id=restaurant.id)
                self.wfile.write(output)
                return


            mo = re.match(r'^/restaurants/(\d+)/delete$', self.path)
            if mo is not None:
                restaurant_id = mo.group(1)
                restaurant = db_iface.get_restaurant(restaurant_id)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output_template = """
                <html><body>
                <form method="POST" enctype="multipart/form-data"
                 action="/restaurants/{id}/delete">
                <h2>Are you sure you want to deleted {name}?</h2>
                <input type="submit" value="Confirm">
                </form>
                </html></body>
                """
                output = output_template.format(
                    name=bleach.clean(restaurant.name),
                    id=restaurant.id)
                self.wfile.write(output)
                return


        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(301)
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = """
                <html><body>
                <h2>post content:</h2>
                <h1> %s </h1>
                <form method='POST' enctype='multipart/form-data'
                 action='/hello'><h2>What to say?</h2>
                <input name='message' type='text'>
                <input type='submit' value='Submit'>
                </form>
                </html></body>
                """ % messagecontent[0]
                self.wfile.write(output)

            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant-name')[0]
                restaurant_name = bleach.clean(restaurant_name)
                db_iface.new_restaurant(restaurant_name)
                # redirect consists of ...
                # response code beginning with 3
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                # 'Location' header
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ####
                # manual redirect
                # output = """
                # <html><body>
                # <p>created new restaurant %s</p>
                # <a href="/restaurants">back to list</a>
                # </html></body>
                # """ % restaurant_name
                # self.wfile.write(output)
                return

            mo = re.match(r'^/restaurants/(\d+)/edit$', self.path)
            if mo is not None:
                restaurant_id = mo.group(1)
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant-name')[0]
                restaurant_name = bleach.clean(restaurant_name)
                db_iface.rename_restaurant(restaurant_id,
                                           restaurant_name)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            mo = re.match(r'^/restaurants/(\d+)/delete$', self.path)
            if mo is not None:
                restaurant_id = mo.group(1)
                db_iface.delete_restaurant(restaurant_id)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return


        except IOError:
            self.send_error(404, "File not found %s" % self.path)


def main():
    try:
        server = HTTPServer(('', PORT), WebserverHandler)
        print "web server running on port ", PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print "interrupt, stopping server..."
        server.socket.close()


if __name__ == '__main__':
    main()
