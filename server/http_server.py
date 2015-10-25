#!/usr/bin/python
# encoding -*- utf-8 -*-

# server.py
import sys
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import urlparse
import MySQLdb
import random
import time

def rand_str(cnt):
    strs = "abcdefghijklmnopqrstuvwxyz0123456789"
    STRS_SET_COUNT = len(strs)
    if cnt > STRS_SET_COUNT:
        cnt = STRS_SET_COUNT
    if cnt < 0:
        return ""
    res = ""
    while (cnt > 0):
        cnt -= 1
        res += strs[random.randint(0, STRS_SET_COUNT - 1)]
    return res

class SqlHandler:
    db = None
    cursor = None
    def __init__(self, dbhost, user, pwd, dbname):
        self.db = MySQLdb.connect(dbhost, user, pwd, dbname)
        if self.db == None:
            raise "Failed to connect to dbname %s" % dbname
        self.cursor = self.db.cursor()
    def execute(self, sql):
        if self.cursor == None:
            print "[ERROR] Invalid sql connection!"
            return -1
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, err:
            print "[ERROR] %s" % err
            self.db.rollback()
            return -1
        return 0

class HttpHandler(BaseHTTPRequestHandler):
    sql_handler = None

    def do_GET(self):
        print "GET request arrived!"
        parsed_path = urlparse.urlparse(self.path)
        # Get request type
        if self.path == "" or self.path == "/":
            print "Invalid request path!"
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Please input the right url path!\n");
        else:
            self.send_response(200)
            self.end_headers()
            self.handle_request(self.path)
        
    def handle_request(self, request):
        if self.sql_handler == None:
            try:
                self.sql_handler = SqlHandler("127.0.0.1", "root", "gwj239", "test")
            except Exception, err:
                print "[ERROR] %s" % err
                sef.wfile.write("Failed to coonect to database!\r\n")
                return -1

        resstr = ""
        if request == "":
            self.wfile.write("Please input invalid url!\r\n")
            return -1
        elif request == "/insert":
            # Insert one line to database
            namestr = rand_str(10);
            id = int(time.time())
            sql = "insert into tb1 values(%d, '%s')" % (id, namestr)
            if self.sql_handler.execute(sql) == 0:
                self.wfile.write("Insert one line to tb1 (%s, %s)\r\n" % (id, namestr))
                return 0
            else:
                self.wfile.write("Faile to insert to tb1 (%s, %s)\r\n" % (id, namestr))
                return -1
        elif request == "/hello":
            self.wfile.write("Hello world!\r\n")
        else:
            # TODO
            return 0


    def __url_check(self):
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
        'CLIENT VALUES:',
        'client_address=%s (%s)' % (self.client_address,
                self.address_string()),
        'command=%s' % self.command,
        'path=%s' % self.path,
        'real path=%s' % parsed_path.path,
        'params=%s' % parsed_path.params,
        'query=%s' % parsed_path.query,
#'fragment' % parsed_path.fragment,
        'request_version=%s' % self.request_version,
        '',
        'SERVER VALUES:',
        'server_version=%s' % self.server_version,
        'sys_version=%s' % self.sys_version,
        'protocol_version=%s' % self.protocol_version,
        '',
        'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
            message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)

def main():
    HandlerClass = HttpHandler
    ServerClass  = HTTPServer
    Protocol     = "HTTP/1.0"
    
    if sys.argv[1:]:
    	port = int(sys.argv[1])
    else:
    	port = 8000
    server_address = ('0.0.0.0', port)
    
    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)
    
    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()

def unit_test():
    print rand_str(10)

if __name__ == "__main__":
    main()
    #unit_test()
