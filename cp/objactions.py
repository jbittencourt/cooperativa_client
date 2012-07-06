import pygame

import ui
import button
import gfx
from events import *


class objAction(button.buttonImageSprite):

    def __init__(self, evManager, dialog, obj, image):
        button.buttonImageSprite.__init__(self, evManager, image)
        
        self.obj = obj
        self.dialog = dialog
        
    
        
    def onClick(self, pos):
        self.evManager.Post( GUIDialogRemoveRequest( self.dialog ) )
        self.evManager.Post( objActionEvent( self.obj, self ) )


class storeAction(objAction):


    def __init__(self, evManager, dialog, obj):
        images = gfx.loadImageSlices("actions.png", (0,0,140,45),2)
        objAction.__init__( self, evManager, dialog, obj, images[0] )
        self.addState(self.state_over, images[1])        
        

class eatAction(objAction):


    def __init__(self, evManager, dialog, obj):
        images = gfx.loadImageSlices("actions.png", (0,45,140,45),2)
        objAction.__init__( self, evManager, dialog, obj, images[0] )
        self.addState(self.state_over, images[1])        
        
    
