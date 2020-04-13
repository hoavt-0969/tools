import time
from http.server import HTTPServer
from server import Server
from portopen import PortOpen
import config
from threading import Thread
def start_port_open():
    portopen = PortOpen(host,ports_list,log_filepath)
    portopen.run()

def start_web_server():
    httpd = HTTPServer((config.HOST_NAME,config.PORT_WEB),Server)
    print(time.asctime(), "Start Server - %s:%s"%(config.HOST_NAME,config.PORT_WEB))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(),'Server down - %s:%s' %(config.HOST_NAME,config.PORT_WEB))
if __name__ == "__main__":
    host = config.HOST_NAME
    ports_list = config.PORTS_OPEN.split(", ")
    log_filepath = config.log_filepath
    t1 = Thread(target=start_port_open)
    t1.start()
    t2 = Thread(target=start_web_server)
    t2.start()