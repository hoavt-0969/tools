import os

from http.server import BaseHTTPRequestHandler

from routes.main import routes

from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

from config import config

class Server(BaseHTTPRequestHandler):

    def config_server(self):
        self.server_version = config['server_version']
        self.sys_version = config['sys_version']
        self.protocol_version = config['protocol_version']
    def do_GET(self):
        print(self.address_string())
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        print(request_extension)
        if request_extension == "":
            #print(self.path)
            #print(self.path[1:-5])
            #print(routes)
            if self.path in routes :
                #print("if")
                handler = TemplateHandler()
                #print(routes[self.path[:-5]])
                handler.find(routes[self.path])
            else:
                #print("else")
                handler = BadRequestHandler()
        elif request_extension == ".py":
            handler = BadRequestHandler()
        else:
            handler = StaticHandler()
            handler.find(self.path)
 
        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code == 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()
        #print(content)
        if isinstance(content, bytes):
            return content
        else:
            return bytes(content, 'UTF-8')
            
    def respond(self, opts):
        self.config_server()
        # print(self.log_request())
        response = self.handle_http(opts['handler'])
        # print(response)
        self.wfile.write(response)