
import os, sys
from socket import *
import select, codecs

from error import *



class CPSocket:


    def __init__(self,addr,port,blockink=0):
        self.address = addr
        self.port = port
        self.socket = ""
        self.connected = 0


        self.buffersize = 4096
        self.__blocking = blockink
        
    def connect(self):

        self.socket = socket(AF_INET,SOCK_STREAM)
        try:
            self.socket.connect((self.address, self.port))
        except:
            raise CPSocketError("Cannot connect to "+self.address)

        #set the socket to non-blockink 
        if not self.__blocking:
            self.socket.setblocking(0)


        self.connected = 1

    def close(self):
        self.socket.shutdown(2)
        self.socket.close()

    def send(self,string):
        if not self.connected:
            raise CPSocketError("You must open a connection first")
        try:
               self.socket.send(string.encode("utf-8"))
        except:
            raise CPSocketError("Cannot send data")



    def ready(self):
        if self.__blocking:
            return 1
            
        return select.select([self.socket],[self.socket],[self.socket], 0)
                   
        

    def readyToRead(self):
        read, write, error  = self.ready()
        if read.__contains__(self.socket):
            return 1
        else:
            return 0
    
    def readToWrite(self):
        read, write, error  = self.ready()
        if write.__contains__(self.socket):
            return 1
        else:
            return 0


    def receive(self):
    
        if not self.connected:
            raise CPSocketError("You must open a connection first")
        
        if not self.__blocking:
            if not self.readyToRead():
                raise CPSocketError("No data to receive")
    
        try:
            buffer = self.socket.recv(self.buffersize)
        except:
            raise CPSocketError("No data to receive")

        string = buffer.decode('utf-8')
        return string




class CPSocketContent:

    def __init__(self,stream,parser):
        self.stream = stream
        self.parser = parser

        self.doctype = ""
        self.system = ""
        self.inicialized = 0
        
        

    def update(self):

        data = u""
        
        try:
            data = self.stream.receive()
        except (CPSocketError):
            pass
    
        if data:
            self.parser.feed(data)


    def initCommunication(self):
        
        if not (self.doctype and self.system):
            raise CPXmlContentExcption("System or doctype not defined")

        self.stream.send("<?xml version=\"1.0\" encoding=\"utf-8\" ?>")
        self.stream.send("<!DOCTYPE "+self.doctype+" SYSTEM \""+self.system+"\">")


    def send(self,data):
        if not self.inicialized:
            self.initCommunication()
            self.inicialized = 1
            
        self.stream.send(data)



    def setDoctype(self,doctype, system):
        self.doctype = doctype
        self.system = system


