import os

import pygame
from pygame.locals import *

import ui
import viewport
import button

import widgets
import textbox
import textarea
import coopdialogs

import prefs
import gfx


from events import *
    
class mainBack(ui.CPui):

    def __init__(self):
         ui.CPui.__init__(self)
         
         self.image = gfx.loadImage("login.png")
         self.rect = self.image.get_rect()
        
    
class cancelButton(button.buttonImageSprite):
    
    def __init__(self, evManager):
        images = gfx.loadImageSlices("btn_cancel.png", (0,0,40,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])        

    def onClick(self,pos):
        self.evManager.Post(StartWelcomeEvent())    

class loginButton(button.buttonImageSprite):
    
    def __init__(self, evManager, login, passwd):
                
        images = gfx.loadImageSlices("btn_ok.png", (0,0,40,40),2)
        
        button.buttonImageSprite.__init__(self, evManager, images[0])
        
        self.addState(self.state_over, images[1])
        
        self.login = login
        self.passwd = passwd
            
    
    def onClick(self,pos):
        self.evManager.Post(TryLoginEvent(self.login.text, self.passwd.text))




    
class login(ui.CPgui):

    def __init__(self, evManager):
     
        ui.CPgui.__init__(self, evManager)
        
        font = prefs.config.get("fonts","dialog_font")
        size = int(prefs.config.get("fonts_size","dialog_font_size"))

        self.evManager.RegisterListener( self , [LoginEvent])

        back = mainBack() 
        back.depth = 0
        
        user = textbox.TextBoxSprite(evManager, 200)
        user.rect.topleft = (385,220)
        user.setFocus(1)
        user.setFont(font,size)
        user.depth = 1

        senha = textbox.TextBoxSprite(evManager, 200)
        senha.rect.topleft = (295,290)
        
        senha.setFont(font,size)
        senha.depth =2
        
        button = loginButton(evManager,user,senha)
        button.setPos((370,400))
        button.depth =3

        cancel = cancelButton(evManager)
        cancel.setPos((430,400))
        cancel.depth =4

        self.add(back)
        self.add(user)
        self.add(senha)
        self.add(button)
        self.add(cancel)
        
        self.success = ""
        
        

    def Notify(self, event):
        font = prefs.config.get("fonts","dialog_font")
        size = int(prefs.config.get("fonts_size","dialog_font_size"))
             
        if event==LoginSuccessEvent:
            #requires to que control to change the actual screen to the main screen
            self.evManager.Post( StartGameEvent(event.user_data) )
        elif event==LoginFailureEvent:
            diag = coopdialogs.COOPmessageDialog(self.evManager, "N"+unicode(chr(227),"latin-1")+"o achei o seu apelido ou sua senha est"+unicode(chr(225),"latin-1")+" errada." )
            self.evManager.Post( GUIDialogAddRequest( diag ) )      
