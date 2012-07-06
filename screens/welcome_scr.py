import os,sys

import pygame
from pygame.locals import *

import ui
import viewport
import button

import widgets
import textbox
import textarea
import gfx
import coopdialogs

from events import *



class connectDialog(coopdialogs.COOPok_cancelDialog):

    def __init__(self, evManager, text):
        coopdialogs.COOPok_cancelDialog.__init__(self, evManager, text)
    
    def ok(self):
        self.evManager.Post( GUIDialogRemoveRequest( self ) )
        self.evManager.Post( tryConnectEvent() ) 
    
    def cancel(self):
        sys.exit()
    

class background(ui.CPui):

    def __init__(self):
         ui.CPui.__init__(self)
         
         self.image = gfx.loadImage("welcome.png")
         self.rect = self.image.get_rect()
    

class yesButton(button.buttonImageSprite):
    
    def __init__(self, evManager):
        images = gfx.loadImageSlices("yes.png", (0,0,60,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])        
        
        self.evManager.Post( loadSoundEvent("yes", "yes.wav") )
    def __del__(self):            
        self.evManager.Post( unloadSoundEvent("yes") )
        
    def onClick(self,pos):
        self.evManager.Post(StartLoginEvent())
        
    def onMouseOver(self, pos):
        self.evManager.Post( playSoundEvent("yes") )


class noButton(button.buttonImageSprite):
    
    def __init__(self, evManager):
        images = gfx.loadImageSlices("no.png", (0,0,60,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])      
        
        self.evManager.Post( loadSoundEvent("no", "no.wav") )
                
    def __del__(self):            
        self.evManager.Post( unloadSoundEvent("no") )
    
    def onClick(self,pos):
        self.evManager.Post(StartRegistryEvent())

    def onMouseOver(self, pos):
        self.evManager.Post( playSoundEvent("no") )
    
class welcome(ui.CPgui):

    def __init__(self, evManager):
     
        ui.CPgui.__init__(self, evManager)
        
        self.evManager.addListener( self, socketEvent )
        
        self.evManager.Post( loadSoundEvent("speak1", "speak1.wav") )
        self.__ticks_to_play = 0

        back = background()

        
        ybutton = yesButton(evManager)
        ybutton.setPos((130,500))
        ybutton.depth = 2
        
        nbutton = noButton(evManager)
        nbutton.setPos((560,500))
        nbutton.depth = 3
                
                
        
        self.add(back)


        self.add(ybutton)
        self.add(nbutton)
        
        self.evManager.Post( tryConnectEvent() )

    def __del__(self):            
        self.evManager.Post( unloadSoundEvent("speak1") )

    def Notify(self, event):
    
        if event==connectFailedEvent:
            text = "N"+unicode(chr(227),"latin-1")+"o consegui contatar o servidor.\n Tentar Novamente?"
            diag = connectDialog(self.evManager, text )
            self.evManager.Post( GUIDialogAddRequest( diag ) )      
        elif event==TickEvent:
            self.__ticks_to_play +=1
            if self.__ticks_to_play==20:
                self.evManager.Post( playSoundEvent("speak1") )
