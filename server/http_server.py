#!/usr/bin/python
# encoding -*- utf-8 -*-

# server.py
import sys
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import urlparse
import MySQLdb

class SqlHandler:
    db = None
    cursor = None
    def __init__(self, dbhost, user, pwd, dbname):
        self.db = MySQLdb.connect(dbhost, user, pwd, dbname)
        if db == None:
            raise "Failed to connect to dbname %s" % dbname
        self.cursor = db.cursor()
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
        if self.path != "/hello":
            print "Invalid request path!"
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Please input the right url path!\n");
        else:
            self.send_response(200)
            self.end_headers()
            self.handle_request(self.path)
        
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

    def handle_request(self, request):
        resstr = ""
        if request == "":
            self.wfile.write("Please input invalid url!\r\n")
            return -1
        else if request == "/insert":
            # Insert one line to database
            if self.sql_handler == None:
                try:
                    self.sql_handler = new SqlHandler("127.0.0.1", "root", "gwj239", "test")
                except Exception, err:
                    print "[ERROR] %s" % err
                    sef.wfile.write("Failed to coonect to database!\r\n")
                    return -1
                id = 
                sql = "insert into tb1"

    def __rand_str(self, len):
        strs = "abcdefghijklmnopqrstuvwxyz0123456789";
        STRS_SET_COUNT = len(strs)
        if len > STRS_SET_COUNT:
            len = STRS_SET_COUNT
        if len < 0:
            return ""
        res = ""
        while (len > 0):
            --len
            res .= strs[rand()%STRS_SET_COUNT]
        return res

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

if __name__ == "__main__":
    main()
