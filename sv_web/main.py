import time
from http.server import HTTPServer
from server import Server
from portopen import PortOpen
import config
if __name__ == "__main__":
    host = config.HOST_NAME
    ports_list = config.PORTS_OPEN.split(", ")
    log_filepath = config.log_filepath
    # Server.config_server(Server,protocol_ver="HTTP/1.1")
    # httpd = HTTPServer((config.HOST_NAME,config.PORT),Server)
    # print(time.asctime(), "Start Server - %s:%s"%(config.HOST_NAME,config.PORT))
    # try:
    #     httpd.serve_forever()
    # except KeyboardInterrupt:
    #     pass
    # httpd.server_close()
    # print(time.asctime(),'Server down - %s:%s' %(config.HOST_NAME,config.PORT))
    portopen = PortOpen(host,ports_list,log_filepath)
    portopen.run()