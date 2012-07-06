import pygame
from pygame.locals import *

import widgets
import gfx


class buttonSprite(widgets.Widget):


    def __init__(self, evManager):
        widgets.Widget.__init__(self, evManager)
        self.caption = "Button"
        self.font_file_name = None
        self.width = 0
        self.rect= pygame.Rect((0,0,1,1))
        self.color = (255,255,255)

        self.size = 12
        self.oldsize = 12


    
    #----------------------------------------------------------------------
    def setFont(self, fontfile):
        try:
            self.font = pygame.font.Font(fontfile, self.size)
        except:
            self.font = pygame.font.Font(None, self.size)
            raise Exception("Cannot load the font file")


        self.font_file_name = fontfile
        self.linesize = self.font.get_linesize()
        self.width = self.font.size( self.caption.encode("latin-1")+ " " )[0]
        x,y = self.rect.topleft
        self.rect = pygame.Rect( (x, y, self.width, self.linesize +4) )

        self.dirty = 1
    
    #----------------------------------------------------------------------
    def update(self):
        if not self.dirty:
            return

        if not self.size == self.oldsize:
            self.font = pygame.font.Font(self.font_file_name, self.size)
            self.oldsize = self.size
        
        textImg = self.font.render( self.caption.encode("latin-1"), 1, self.color )
        self.width = textImg.get_size()[0]
        x,y = self.rect.topleft
        self.rect = pygame.Rect( (x, y, self.width, self.linesize +4) )
        self.image = textImg

        self.dirty = 0
        

class buttonImageSprite(widgets.Widget):

    state_normal = 1
    state_over = 2
    state_down = 3

    def __init__(self, evManager, image):
        widgets.Widget.__init__(self, evManager)
        
        self.images = {}
        self.rect = Rect(0,0,1,1)
        
        self.images[self.state_normal] = image
        
        self.state = self.state_normal
        self.__change_state = 0
        self.__changeImage()

    def __changeImage(self):
        self.image = self.images[self.state]
        self.rect.size = self.image.get_size()
                
    def addState(self, state, image):
        self.images[state] = image
    
    def M_mouseover(self,pos):
        if self.images.has_key(self.state_over):
            self.state = self.state_over
            self.__changeImage()
        
        self.onMouseOver(pos)

    def M_mouseout(self,pos):
        if self.images.has_key(self.state_over):
            self.state = self.state_normal
            self.__changeImage()
        
        self.onMouseOut(pos)
    
    
    #----------------------------------------------------------------------
    def update(self):
        
        self.dirty = 0
        
        if self.__change_state:
            self.__changeImage()
            self.dirty = 1


