import pygame
from pygame.locals import *


CP_ONEFRAME = USEREVENT + 1


class Event:
    """this is a superclass for any events that might be generated by an
    object and sent to the EventManager"""
    _name = "Generic Event"
    _pygame_event_id = USEREVENT

    def __init__(self):
        pass
        
    
    def __eq__(self,b):
        return isinstance(self, b)

    def __str__(self):
        return "EVENT:"+self._name

    def getPygameId(self):
        return self._pygame_event_id
   

class NoneEvent(Event):
    _name = "None Event" 
       

class ExceptionEvent( Event ):

    _name = "Exception Event"
    
    def __init__(self, text):
        Event.__init__(self)
        self.text = text

class OneSecondEvent(Event):
    _name = "One Second"

    def __init__(self):
        Event.__init__(self)
   
class syncServerEvent(  Event ):
    _name = "One Frame"
    
    def __init__(self):
        Event.__init__(self)


class TickEvent(Event):
    _name = "Tick"


class FrameEvent(Event):
    _name = "Tick"

    
class QuitEvent(Event):
    _name = "Quit"

#------------- GUI Events ------

class GUIEvent(Event):
    
    def __init__(self, gui):
        self.gui = gui


class GUIDialogAddRequest(GUIEvent):
    _name = "GUI add dialog"
    
    def __init__(self, dialog):
        GUIEvent.__init__(self, dialog)

class GUIDialogRemoveRequest(GUIEvent):
    _name = "GUI remove dialog"
    
    def __init__(self, dialog):
        GUIEvent.__init__(self, dialog)
    
    
    
class GUIWidgetEvent(Event):
    
    def __init__(self, widget):
        self.widget = widget
    
    
class GUIFocusThisWidgetEvent(GUIWidgetEvent):
    _name = "GUI focus this Widget"
    
    def __init__(self, widget):
        GUIWidgetEvent.__init__(self, widget)
        

class GUIFocusNextWidgetEvent(GUIWidgetEvent):
    _name = "GUI focus next Widget"
    
    def __init__(self, widget):
        GUIWidgetEvent.__init__(self, widget)
        
class GUIFocusPrevWidgetEvent(GUIWidgetEvent):
    _name = "GUI focus previous Widget"
    
    def __init__(self, widget):
        GUIWidgetEvent.__init__(self, widget)
        

        
#--------------------------------------------------------------------------
# Change Screen Events

class StartGameEvent(Event):

    def __init__(self, player_data):
        Event.__init__(self)
        self.player_data = player_data
    

class StartLoginEvent(Event):

    def __init__(self):
        Event.__init__(self)
        

class StartRegistryEvent(Event):

    def __init__(self):
        Event.__init__(self)
        
class StartWelcomeEvent(Event):

    def __init__(self):
        Event.__init__(self)


#--------------------------------------------------------------------------
#-  Socket Events

class socketEvent(Event):
    _name = "Socket control events"
    def __init__(self):
        Event.__init__(self)
        
class tryConnectEvent(socketEvent):
    _name = "Try to connecct with socket events"
    
    def __init__(self):
        socketEvent.__init__(self)
        

class connectSuccessEvent(socketEvent):
    _name = "Connect success events"
    
    def __init__(self):
        socketEvent.__init__(self)

class connectFailedEvent(socketEvent):
    _name = "Connect failure events"
    
    def __init__(self):
        socketEvent.__init__(self)


#--------------------------------------------------------------------------
#- sound events

class soundEvent(Event):
    _name = "Sound control events"
    def __init__(self):
        Event.__init__(self)


class loadSoundEvent(soundEvent):
        
    def __init__(self,name,filename):
        soundEvent.__init__(self)
        self.name = name
        self.filename = filename

class unloadSoundEvent(soundEvent):
        
    def __init__(self,name):
        soundEvent.__init__(self)
        self.name = name

        
class playSoundEvent(soundEvent):
        
    def __init__(self,name):
        soundEvent.__init__(self)
        self.name = name
        
    
class loadMusicEvent(soundEvent):
        
    def __init__(self,filename):
        soundEvent.__init__(self)
        self.filename = filename

class stopMusicEvent(soundEvent):
        
    def __init__(self):
        soundEvent.__init__(self)

class changeMusicEvent(soundEvent):
        
    def __init__(self,filename):
        soundEvent.__init__(self)
        self.filename = filename

class restoreMusicEvent(soundEvent):
        
    def __init__(self):
        soundEvent.__init__(self)        
# --------------------------------------------------------------------------
#  Login events
       
class LoginEvent(Event):
    _name = "Login events"
    
    def __init__(self):
        Event.__init__(self)


class createUserEvent(LoginEvent):
    _name = "Create User Event"
    
    def __init__(self, user, passwd, name, idAvatar):
        LoginEvent.__init__(self)

        self.username = user
        self.password = passwd
        self.name = name
        self.idAvatar = idAvatar

class createUserFailedEvent(LoginEvent):
    _name = "Create user failure event"
    
    def __init__(self, error):
        LoginEvent.__init__(self)
        self.error = error

        
class TryLoginEvent(LoginEvent):
    _name = "Trying to login events"
    
    def __init__(self, user, passwd):
        LoginEvent.__init__(self)

        self.user = user
        self.password = passwd

        

class LoginSuccessEvent(LoginEvent):
    _name = "Login success event"
    
    def __init__(self, userdata):
        LoginEvent.__init__(self)
        self.user_data = userdata

class LoginFailureEvent(LoginEvent):
    _name = "Login failure event"
    
    def __init__(self, error):
        LoginEvent.__init__(self)
        self.error = error

        
        

#--------------------------------------------------------------------------        
#Backpack Events


class BackpackEvent(Event):
    def __init__(self):
        Event.__init__(self)


class addBackpackEvent(BackpackEvent):

    def __init__(self, obj):
        BackpackEvent.__init__(self)
        
        self.obj = obj
        
class removeBackpackEvent(BackpackEvent):

    def __init__(self, obj):
        BackpackEvent.__init__(self)
        
        self.obj = obj


#--------------------------------------------------------------------------        
#Game Events

class GameEvent(Event):
    def __init__(self):
        Event.__init__(self)
        

class LogoutEvent(GameEvent):
    def __init__(self, id):
        GameEvent.__init__(self)
        self.iduser = id

class MainPlayerEvent(GameEvent):
    
    def __init__(self, player_data):
        GameEvent.__init__(self)
        self.player_data = player_data

class RequestEnterLevel(GameEvent):

    def __init__(self, level, pos):
        GameEvent.__init__(self)
        self.level = level
        self.pos = pos
        
class LoadLevelEvent(GameEvent):

    def __init__(self, level_file_name, users, objs):
        GameEvent.__init__(self)
        self.level_file_name = level_file_name
        self.users = users
        self.objs = objs

class ChatStartEvent(GameEvent):
    
    def __init__(self):
        GameEvent.__init__(self)
        
class RequestEnterChatEvent(GameEvent):
    
    def __init__(self, user_id, pos):
        GameEvent.__init__(self)
        self.user_id = user_id
        self.pos = pos
        
class EnterChatEvent(GameEvent):
    
    def __init__(self, user_id, pos, avatar):
        GameEvent.__init__(self)
        self.user_id = user_id
        self.pos = pos
        self.avatar = avatar
        
class RequestMoveToEvent(GameEvent):

    def __init__(self, user_id, pos):
        GameEvent.__init__(self)
        self.user_id = user_id
        self.pos = pos

class MoveToEvent(GameEvent):

    def __init__(self, user_id, pos):
        GameEvent.__init__(self)
        self.user_id = user_id
        self.pos = pos

        
class SendTalkEvent(GameEvent):
    
    def __init__(self, user_id, text ):
        GameEvent.__init__(self)
        self.user_id = user_id
        self.text = text
        

class TalkEvent(GameEvent):
    
    def __init__(self, user_id, text ):
        GameEvent.__init__(self)
        self.user_id = user_id
        self.text = text
        


class SendObjectChangeState(GameEvent):

    def __init__(self, obj_id, status ):
        GameEvent.__init__(self)
        self.obj_id = obj_id
        self.status = status
        self.pos = (-1,-1)
        
        
class ObjectChangeState(GameEvent):

    def __init__(self, obj_id, status ):
        GameEvent.__init__(self)
        self.obj_id = obj_id
        self.status = status
        
        
class objActionEvent(GameEvent):

    def __init__(self, obj, action):
        GameEvent.__init__(self)
        self.obj = obj
        self.action = action
        
class SendAddObjInventary(GameEvent):


    def __init__(self, user_id, obj):
        GameEvent.__init__(self)
        
        self.obj = obj
        self.user_id = user_id