from sys import argv
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
from Render import *
from os import system
import time

def write_hr(hr="0"):
    write(int(hr))

def read_hr():
    return HeartRate[0]

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class HeartBeatHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path == "/hr":
            self._set_response(200)
            self.wfile.write(str(read_hr()).encode('utf-8'))
        elif self.path == "/obs":
            self._set_response(200)
            self.wfile.write(open("./obs.html", "r").read().encode('utf-8'))
        elif self.path.startswith("/js/") or self.path.startswith("/css/"):
            self._set_response(200)
            self.wfile.write(open(".{}".format(self.path), "r").read().encode('utf-8'))
        else:
            self._set_response(404)
            self.wfile.write("NOT FOUND".encode('utf-8'))



    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self._set_response(200)
        self.wfile.write("OK".encode('utf-8'))
        data = post_data.decode('utf-8').split("=")
        print("Received BPM = {}".format(data[1]))
        write_hr(data[1])

def keep_running():
    return running[0]

def run(port):
    server_class=HTTPServer
    handler_class=HeartBeatHandler
    server_address = ("", port)

    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("""
###########################
#     STOPPING SERVER     #
###########################        
        """)
        pass
    httpd.server_close()


if __name__ == '__main__':
    port_arg = 6547
    if len(argv) == 2:
        port_arg = argv[1]

    #print("This is your IP : {}" .format(get_ip()))
    #print("Port is {}" .format(port_arg))
    print("WebServer online")
    start()
    thr = None
    if len(argv) == 2:
        thr=Thread(target=run,args=(int(port_arg),))
    else:
        thr=Thread(target=run,args=(port_arg,))
    thr.start()
    while keep_running():
        time.sleep(0.1)
    system('taskkill /f /im "pythonw.exe"')
