#!/usr/bin/env python3
# coding: utf-8
# Copyright 2019 Vlad Kravchenko, https://github.com/vvkravch
# Copyright 2016 Abram Hindle
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse


def help():
    print("httpclient.py [GET/POST] [URL]\n")
    
def parse(url):
    #different cases of url
    if ("http://" in url):
        parseddata = urllib.parse.urlparse(url) 
    elif ("https://" in url):
        parseddata = urllib.parse.urlparse(url)
    else:
        host="http://" + host
        parseddata = urllib.parse.urlparse(host)
    if not (parseddata.port):
        port=80
    else:
        port=parseddata.port
    if not (parseddata.path):
        path="/"
    else:
        path=parseddata.path
    
    #print(parseddata)   
    host= parseddata.hostname
    return(host,port,path)

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        splitdata=data.split()
        #print(splitdata)
        code=int(splitdata[1])
        #print ("THE CODE"+str(code)+"\n")
        return code

    def get_headers(self,data):
    
        return None

    def get_body(self, data):
        splitdata=data.split("\r\n\r\n")
        body=splitdata[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        host,port,path=parse(url)
        #print ("HOST!!="+host+str(port))
        self.connect(host,port)
        #print("Bla inside get")
        #Prepare the request
        requesttype="GET "+path+" HTTP/1.1\r\n"
        hostloc="Host: " + host+"\r\n"
        user_agent="User-Agent: "+"vvkravch_client "+"\r\n"
        accept="Accept: */*\r\n"
        acceptlang="Accept-Language:en-US,en;\r\n\r\n"
        tobesent=requesttype+hostloc+user_agent+accept+acceptlang
        self.sendall(tobesent)
        #print("data sent")
        
        self.socket.shutdown(socket.SHUT_WR)
        
        data=self.recvall(self.socket)
        self.close()
        #print("data received")
        print (data)
        print ("\n")
        code=self.get_code(data)
        body=self.get_body(data)
        print (body)
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host,port,path=parse(url)
        #print ("HOST!!="+host+str(port))
        self.connect(host,port)
        #print("Bla inside get")
        if args!=None:
            encodedarg=urllib.parse.urlencode(args)
            
           # print("THE ARGUMEEEENTS"+str(encodedarg))
           # prepare post request 
        request1="POST " + path +" HTTP/1.1\r\n"
        request3 ="Host: "+host+ " r\n"
        request4= "Accept: */* \r\n"
        request5 ="Content-Type: application/x-www-form-urlencoded\r\n"
        request0= request1 +request3+request4+request5
        if args!=None:
            request2="Content-Length: "+str(len(encodedarg))+" \r\n\r\n"
            request = request0+request2+encodedarg
            #print("AND THE LENGTH IS "+ str(len(encodedarg)))
        else:
            request = request0+ "Content-Length: 0 \r\n\r\n"
        self.sendall(request)
        #print("data sent")
        self.socket.shutdown(socket.SHUT_WR)
        
        data=self.recvall(self.socket)
        self.close()
        #print("data received!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #print (data)
        code=self.get_code(data)
        body=self.get_body(data)        
        #code = 500
        #body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            print("Bla get")
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        #host,port,path =parse(sys.argv[2])
        #print(parse(sys.argv[2]))
        #client.connect(host,port)
        print("bla")
        print(client.command( sys.argv[2], sys.argv[1] ))
        #client.close()
    else:
        print(client.command( sys.argv[1] ))
