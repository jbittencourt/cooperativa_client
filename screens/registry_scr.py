import os

import pygame
from pygame.locals import *


import ui
import viewport
import button

import widgets
import textbox
import textarea
import gfx

from events import *
import gfx
import prefs

import actors
import coopdialogs

class createButton(button.buttonImageSprite):
    
    def __init__(self, evManager, login, passwd, name, avatar):
                
        images = gfx.loadImageSlices("btn_ok.png", (0,0,40,40),2)
        
        button.buttonImageSprite.__init__(self, evManager, images[0])
        
        self.addState(self.state_over, images[1])
        
        self.login = login
        self.passwd = passwd
        self.name = name
        self.avatar = avatar
            
    
    def onClick(self,pos):
        #listener of createUserEvent implemented at coopxml.py
        self.evManager.Post(createUserEvent(self.login.text, self.passwd.text, self.name.text, str(self.avatar.index)))

        
class cancelButton(button.buttonImageSprite):
    
    def __init__(self, evManager):
        images = gfx.loadImageSlices("btn_cancel.png", (0,0,40,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])        

    def onClick(self,pos):
        self.evManager.Post(StartWelcomeEvent())        
   
    
class changeLeftButton(button.buttonImageSprite):
    
    def __init__(self, evManager, avatar_browser):
        images = gfx.loadImageSlices("btn_left.png", (0,0,40,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])        
        
        self.avatar_browser = avatar_browser

    def onClick(self,pos):
        index = self.avatar_browser.index
        self.avatar_browser.setIndex(index-1)

class changeRightButton(button.buttonImageSprite):
    
    def __init__(self, evManager, avatar_browser):
        images = gfx.loadImageSlices("btn_right.png", (0,0,40,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])        

        self.avatar_browser = avatar_browser

    def onClick(self,pos):
        index = self.avatar_browser.index
        self.avatar_browser.setIndex(index+1)



        
class avatarBrowser(ui.CPui):

    def __init__(self,avatar_id, rect):
        ui.CPui.__init__(self)
        
        self.rect = pygame.Rect(rect)
        self.orect = pygame.Rect(rect)
        self.index = avatar_id
        self.avatar = actors.CPavatar(str(self.index))
        self.dirty = 1
        self.update()
        
    def setIndex(self,index):
        if index < 0 or index>= self.avatar.avaiable_avatares:
            return 0
        self.index = index
        #self.avatar.changeAvatar(str(self.index))
        self.avatar = actors.CPavatar(str(self.index))
        self.dirty =1
        
        print index

    
    def update(self):
    
        if self.dirty:
            w,h = self.rect.size
            w1,h1 = self.avatar.rect.size
            
            ax = w/w1
            ay = h/h1
            
            if ax>ay :
                min = ay
            else:
                min = ax
        
            self.image = pygame.transform.scale(self.avatar.image, ( int(w1*min), int(h1*min) ) )
            w2,h2 = self.image.get_size()
            dx = int( (w-w2) /2)
            dy = int( (h-h2) /2)
            
            self.rect.left = self.orect.left + dx
            self.rect.top = self.orect.top + dy            
            
            self.dirty = 0
            
            


class background(ui.CPui):

    def __init__(self):
         ui.CPui.__init__(self)
         
         
         self.image = gfx.loadImage("registration.png")
         self.rect = self.image.get_rect()
        

class registryScreen(ui.CPgui):
    
    def __init__(self, evManager):
        ui.CPgui.__init__(self, evManager)
        
        font = prefs.config.get("fonts","dialog_font")
        size = int(prefs.config.get("fonts_size","dialog_font_size"))
        
        self.evManager.RegisterListener(self, [LoginEvent])

             
        back = background()
        back.depth = 0
        
        username = textbox.TextBoxSprite(evManager, 250)
        username.rect.topleft = (295,38)
        username.setFocus(1)
        username.setFont(font,size)
        username.depth = 1
        username.tabOrder = 1
        
        name = textbox.TextBoxSprite(evManager, 400)
        name.rect.topleft = (295,88)
        name.setFont(font,size)
        name.depth = 2
        name.tabOrder = 2
        
        passwd = textbox.TextBoxSprite(evManager, 250)
        passwd.rect.topleft = (295,134)
        passwd.setFont(font,size)
        passwd.depth = 3
        passwd.tabOrder = 3
        
        browser = avatarBrowser(0,(292,192,165,225))
        browser.depth = 8

        button = createButton(evManager,username,passwd,name, browser)
        button.setPos((300,450))
        button.depth =4
        
        cancel = cancelButton(evManager)
        cancel.setPos((400,450))
        cancel.depth =5
               
        
        left = changeLeftButton(evManager,browser)
        left.setPos((235,250))
        left.depth = 7
        
        right = changeRightButton(evManager,browser)
        right.setPos((470,250))
        right.depth = 6
        
        
        
        self.add(back)
        self.add(username)
        self.add(name)
        self.add(passwd)
        self.add(button)
        self.add(cancel)
        self.add(left)
        self.add(right)
        self.add(browser)

        
        
        
        
    def Notify(self, event):

        if event==LoginSuccessEvent:
            #requires to que control to change the actual screen to the main screen
            self.evManager.Post( StartGameEvent(event.user_data) ) 
        elif event==createUserFailedEvent:
            diag = coopdialogs.COOPmessageDialog(self.evManager, "J"+unicode(chr(225),"latin-1")+" existe uma outra pessoa com esse apelido." )
            self.evManager.Post( GUIDialogAddRequest( diag ) )      
        
