import os
import logging
from http.server import BaseHTTPRequestHandler

from routes.main import routes

from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

from config import config_web_server
import config
class Server(BaseHTTPRequestHandler):

    def config_server(self):
        self.server_version = config_web_server['server_version']
        self.sys_version = config_web_server['sys_version']
        self.protocol_version = config_web_server['protocol_version']
    def do_GET(self):
        # logging.basicConfig(level=logging.DEBUG, 
        #                     format= '%(asctime)s %(levelname)-8s %(message)s', 
        #                     datefmt='%Y-%m-%d %H:%M:%S', 
        #                     filename=config.log_web_filepath, 
        #                     filemode='w')
        # logger_web_sv = logging.getLogger("server")
        # logger_web_sv.info("hello")
        self.log_web = logging.getLogger("server")
        self.file_log_web = logging.FileHandler("log_web.txt")
        self.format_log_web = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        self.file_log_web.setFormatter(self.format_log_web)
        self.log_web.setLevel(logging.DEBUG)
        self.log_web.addHandler(self.file_log_web)
        # log_web.info("hello log web")
        # print(self.address_string())
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        # print(request_extension)
        # print(self.client_address)
        # print(self.log_request())
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
        self.log_web.info("\nConnection from: %s:%s\nGET %s\n%s\n",str(self.client_address[0]),str(self.client_address[1]) , str(self.path), str(self.headers))
        # self.log_web.info("hello")
        # print(response)
        self.wfile.write(response)