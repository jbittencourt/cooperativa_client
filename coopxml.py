import sys
import threading

import prefs


import xml.sax
import network
from error import *
from events import *


class COOPxmlHandler(xml.sax.handler.ContentHandler):

    def __init__(self, evManager):
        self.evManager = evManager

        self.__status = "IDENTIFY"
        self.main_user = {}
        self.__user = {}
        
        self.__objs = []
        
        self.__login_status = 0
        self.__chating = 0
        

    def startElement(self, name, attrs):
    
        
        if name=="identify_ack":
            # 0 on success an positive integer on failure. If fail, the interger represents the error code
            if attrs['status']=="0":
                self.__login_status = 1
            else:
                self.evManager.Post( LoginFailureEvent(attrs['status']) )
            

        elif name=="userinfo":
            if self.__status == "IDENTIFY":
                for k in attrs.keys():
                    self.main_user[k] = attrs[k]
            elif self.__status == "USER_STATUS":
                for k in attrs.keys():
                    self.__user[k] = attrs[k]
        elif name=="navigate":
            self.__status = "NAVIGATE"
        
        elif name=="request_enter_cenario_ack":
            if attrs["status"]=="0":
                self.__status = "ENTERING_CENARIO"
                self.users = []
            else:
                #sent a refuse comment
                pass 
            
        elif name=="cenario_status_info":
            self.__status = "USER_STATUS"
        
        elif name=="user_status":
            id = attrs["iduser"]
            pos = ( int(attrs["posx"]), int(attrs["posy"]) )
            if self.__status == "IDENTIFY":
                self.main_user["id"] = id
                self.main_user["pos"] = pos
            elif self.__status == "USER_STATUS":
                self.__user = {}
                self.__user["id"] = id
                self.__user["pos"] = pos
        
        elif name=="object_status":
            obj = {}
            obj["idobj"] = attrs["idobj"]
            obj["pos"] = ( int(attrs["posx"]), int(attrs["posy"]) )
            obj["status"] = attrs["status"]
            obj["tag"] = attrs["tag"]
            obj["flagInventario"] = attrs["flagInventario"]
            obj["iduser"] = attrs["iduser"]
            
            self.__objs.append( obj )
            

        elif name=="chat":
            self.__status = "CHATING"
            self.__chating = 1
            self.evManager.Post( syncServerEvent() )
            self.evManager.Post( ChatStartEvent() )
                
        elif name=="enter_cenario":
            id = attrs["iduser"]
            pos = ( int(attrs["posx"]), int(attrs["posy"]) )
            avatar = attrs["avatar"]
            self.evManager.Post( EnterChatEvent(id, pos, avatar) )

        elif name=="move_to":
            id = attrs["iduser"]
            pos = ( int(attrs["posx"]), int(attrs["posy"]) )
            self.evManager.Post( MoveToEvent(id, pos) )

        elif name=="talk":
            self.__status = "TALKING"
            self.__talk_text = ""
            self.__talk_user = attrs["iduser"]
        
        elif name=="change_object_state":
            id = attrs["idobj"]
            status = attrs["status"]
            self.evManager.Post( ObjectChangeState(id, status) )
    
        elif name=="sync":
            if self.__chating == 1:
                self.evManager.Post( OneSecondEvent() )
            
        elif name=="logout":
            id = attrs["iduser"]
            self.evManager.Post( LogoutEvent(id) )
            
        elif name=="create_user":
            if not attrs["status"]=="0":
                self.evManager.Post( createUserFailedEvent(attrs["status"]) )
            
            

    def endElement(self, name):
        if name=="identify_ack":
            if self.__login_status:
                self.evManager.Post(LoginSuccessEvent(self.main_user))
        elif name=="request_enter_cenario_ack":
            if self.__status == "ENTERING_CENARIO":
                self.evManager.Post( LoadLevelEvent("praca.xml", self.users , self.__objs) )
        
        elif name=="talk":    
            if self.__talk_text:
                self.__status == "CHATING"
                self.evManager.Post( TalkEvent( self.__talk_user, self.__talk_text ) )
        
        elif name=="user_status":
            if self.__status == "USER_STATUS":
                self.users.append( self.__user )
        
        elif name=="cenario_status_info":
            self.__status = "ENTERING_CENARIO"
    
    def characters (self, ch): 
        if self.__status == "TALKING":
            self.__talk_text += ch
        
    






class COOPcommunication(threading.Thread):


    def __init__(self, evManager):
        threading.Thread.__init__(self)

        self.evManager = evManager
        self.evManager.RegisterListener(self, [Event])
        
        self.host = prefs.config.get("server","hostname")
        self.port = int(prefs.config.get("server","port"))
        
        self.socket = network.CPSocket(self.host, self.port, 1)
        self.__connected = 0
        self.conn = None
        
        self.__stop_lock = threading.Lock()
        self.__stop = 0
        
    def stop(self):
        self.__stop_lock.acquire()
        self.__stop = 1
        self.__stop_lock.release()

        self.socket.close()
        
        

    def connect(self):

        try:
            self.socket.connect()
            self.__connected = 1
        except:
            raise CPSocketConnectError(0)

        self.__status = {}
        self.__status["navigate"] = 0   #can navigate flag

        self.main_user = {}
        
        #inicializa the handler
        self.handler = COOPxmlHandler( self.evManager )
        self.parser = xml.sax.make_parser()
        self.parser.setContentHandler(self.handler)


        self.conn = network.CPSocketContent(self.socket, self.parser)

        self.conn.setDoctype("cooperativa_cliente_servidor", "coop_cliente_servidor.dtd")

        self.conn.send("<cooperativa_cliente_servidor version=\"1.0\">")

        self.state = "IDENTIFY"
        
        

    def identify(self,username,password):
        self.__status["login"] = -1
        self.conn.send("<identify username=\""+username+"\" password=\""+password+"\"/>")

            

    def setStatus(self, key, value):
        self.__status[key]=value
        


    def startChat(self):
        self.conn.send("<chat>")
        return 1        
        
    def requestEnterCenario(self, id, pos):
        x, y = pos
        
        self.conn.send("<request_enter_cenario idcenario=\""+id+"\" celpos=\"0\" request_cenario_xml=\"0\"/>")
        return 1
    
    def requestEnterChat(self, id, pos):
        x, y = pos
        self.conn.send("<enter_cenario iduser=\""+id+"\" posx=\""+str(x)+"\"  posy=\""+str(y)+"\" method=\"0\"/>")
        return 1    

    def moveTo(self, id, pos):
        x, y = pos
        self.conn.send("<move_to iduser=\""+id+"\" posx=\""+str(x)+"\"  posy=\""+str(y)+"\"/>")
        return 1    

    def talk(self, user_id, text):
        print "<talk iduser=\""+user_id+"\">"+text+"</talk>\n"
        self.conn.send("<talk iduser=\""+user_id+"\">"+text+"</talk>")
        return 1    
    
    def send_obj_state(self, obj_id, status, pos):
        x,y = pos
        msg = "<change_object_state idobj=\""+str(obj_id)+"\" status=\""+str(status)+"\" tag=\"0\" posx=\""+str(x)+"\" posy=\""+str(y)+"\"/>"
        self.conn.send(msg)
        return 1

    def create_user(self, username, password, name, avatar):
        men = "<create_user username=\""+username+"\""
        men += " password=\""+password+"\""
        men += " nomPessoa=\""+name+"\""
        men += " idAvatar=\""+avatar+"\""
        men += " />"
        self.conn.send(men)
        return 1
    
    def add_inventory(self, user_id,obj_id):
    
        user_id = str(user_id)
        obj_id = str(obj_id)
        
        msg = "<inventory_add_item idobj=\""+obj_id+"\"  iduser=\""+user_id+"\">"
        self.conn.send(msg)

    def Notify(self, event):
        
        
        if event==QuitEvent:
            self.stop()
        
        if not self.__connected:
            if event==tryConnectEvent:
                try:
                    self.connect()
                    self.evManager.Post( connectSuccessEvent() )
                except (CPSocketConnectError):
                    self.evManager.Post( connectFailedEvent() )
                    
                
                
        else:
            if event==TryLoginEvent:
                self.identify(event.user, event.password)
            elif event==LoginSuccessEvent:
                self.conn.send("<navigate>")
            
            elif event==RequestEnterLevel:
                self.requestEnterCenario(event.level,event.pos)
            
            elif event==RequestEnterChatEvent:
                self.requestEnterChat(event.user_id, event.pos)
                
            elif event==ChatStartEvent:
                self.startChat()
            
            elif event==RequestMoveToEvent:
                self.moveTo(event.user_id, event.pos)
                
            elif event==SendTalkEvent:
                self.talk(event.user_id, event.text)
                
            elif event==SendObjectChangeState:
                self.send_obj_state( event.obj_id, event.status, event.pos)
        
            elif event==createUserEvent:
                self.create_user(event.username, event.password, event.name, event.idAvatar)
                
            elif event==SendAddObjInventary:
                self.add_inventory(event.user_id,event.obj.id)
    

    def run(self):

        while(not self.__stop):
            if self.__connected  and self.conn:
                self.conn.update()
            
       
        
        
