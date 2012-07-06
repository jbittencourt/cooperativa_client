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
import prefs

from events import *
import backpack


class dialogTextBox(textarea.TextAreaSprite):

    def __init__(self, evManager, cols, rows, viewport):
        textarea.TextAreaSprite.__init__( self, evManager, cols, rows )
        self.viewport = viewport
    
    def onKeypress(self, key, modifier):
        char, k = key
        if k==K_RETURN or k==K_KP_ENTER:
            iduser = self.viewport.player_data["iduser"]
            if iduser:
                self.evManager.Post( SendTalkEvent( iduser, self.text ) )
                self.clear()
                self.dirty =1


class buttonSend(button.buttonImageSprite):
    
    def __init__(self, evManager, text):
        images = gfx.loadImageSlices("btn_ok.png", (0,0,40,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])        
        
        self.text = text
            
    def onClick(self, pos):
        iduser = self.text.viewport.player_data["iduser"]
        self.evManager.Post( SendTalkEvent( iduser, self.text.text ) )
        self.text.clear()
        
class buttonQuit(button.buttonImageSprite):
    
    def __init__(self, evManager):
        images = gfx.loadImageSlices("btn_leave.png", (0,0,40,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])        
        
            
    def onClick(self, pos):
        self.evManager.Post( QuitEvent() )


class mainFront(ui.CPui):

    def __init__(self):
         ui.CPui.__init__(self)
         
         self.image = gfx.loadImage("main.png")
         self.rect = self.image.get_rect()
        

class mainScreen(ui.CPgui):
    
    def __init__(self, evManager):
        ui.CPgui.__init__(self, evManager)
        
        font = prefs.config.get("fonts","dialog_font")
        size = int(prefs.config.get("fonts_size","dialog_font_size"))
        
        self.viewport = viewport.CPviewport( evManager, (17,70,600,400) )
        self.viewport.depth = 1
        self.add(self.viewport)

        
        
        text = dialogTextBox(evManager, 50, 3, self.viewport)
        text.rect.topleft = (110,480)
        text.setFont(font,size)
        text.max_chars = 90
        text.setFocus(1)

        send = buttonSend(evManager, text)
        send.rect.topleft = (550,480)
        
        quit = buttonQuit(evManager)
        quit.rect.topleft = (760,0)
        
    
        front = mainFront()
        front.depth = 2
        text.depth = 3
        quit.depth = 4
        send.depth = 5
        
        back = backpack.Backpack(evManager, (700,70,120,500) )
        back.depth = 6
        

        self.add(front)
        self.add(text)
        self.add(back)
        self.add(send)
        self.add(quit)

