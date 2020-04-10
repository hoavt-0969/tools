import time
from http.server import HTTPServer
from server import Server

import config
if __name__ == "__main__":
    # Server.config_server(Server,protocol_ver="HTTP/1.1")
    httpd = HTTPServer((config.HOST_NAME,config.PORT),Server)
    print(time.asctime(), "Start Server - %s:%s"%(config.HOST_NAME,config.PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(),'Server down - %s:%s' %(config.HOST_NAME,config.PORT))