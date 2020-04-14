import logging
import threading
from socket import socket, timeout


class PortOpen(object):
    def __init__(self, bind_ip, ports, log_filepath):
        self.ports = ports
        self.log_filepath = log_filepath
        self.listener_threads = {}
        self.bind_ip = bind_ip
        if len(ports) < 1 :
            raise Exception("No ports provided.")
        self.log_port = logging.getLogger("portopen")
        self.file_log_port = logging.FileHandler("log.txt")
        self.format_log_port = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        self.log_port.setLevel(logging.DEBUG)
        self.log_port.addHandler(self.file_log_port)
        self.log_port.info("hello log port")
        # logging.basicConfig(level=logging.DEBUG, 
        #                     format= '%(asctime)s %(levelname)-8s %(message)s', 
        #                     datefmt='%Y-%m-%d %H:%M:%S', 
        #                     filename=self.log_filepath, 
        #                     filemode='w')
        # self.logger = logging.getLogger("portopen")
        # self.logger.info("Honeypot initializing...")
        # self.logger.info("Ports: %s" %self.ports)
        # self.logger.info("Log file path: %s" % self.log_filepath)
        # logging.info("Honeypot initializing...")
        # logging.info("Ports: %s" %self.ports)
        # logging.info("Log file path: %s" % self.log_filepath)
    
    def handle_connection(self, port, client_socket, ip, remote_port):
        data = client_socket.recv(64)
        # self.logger.info("Connection to port %s form %s:%d - %s"% (port,ip,remote_port,data[:-1].decode("utf8")))
        self.log_port.info("Connection to port %s form %s:%d - %s"% (port,ip,remote_port,data[:-1].decode("utf8")))
        client_socket.send("Access denied.\n".encode("utf8"))
        client_socket.close()
    
    def start_new_listener_thread(self, port):
        listener = socket()
        listener.bind((self.bind_ip,int(port)))
        listener.listen(5)
        while True:
            client, addr = listener.accept()
            print(addr)
            client_handler = threading.Thread(target=self.handle_connection, args=(port,client, addr[0], addr[1]))
            client_handler.start()
    def start_listening(self):
        for port in self.ports:
           self.listener_threads[port] = threading.Thread(target=self.start_new_listener_thread,args=(port,))
           self.listener_threads[port].start()
    def run(self):
        self.start_listening()
        while True:
            pass