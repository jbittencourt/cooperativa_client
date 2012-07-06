from events import *
import pygame
from pygame.locals import *
import string

import ui

vectorSum = lambda a,b: (a[0]+b[0], a[1]+b[1])

#------------------------------------------------------------------------------
class Widget(ui.CPui):

    def __init__(self, evManager):
        ui.CPui.__init__(self)

        self.evManager = evManager
        self.evManager.RegisterListener( self , [TickEvent,GUIWidgetEvent])
        
        self.focused = 0
        self.dirty = 1

        self.isFocusable = 0
        
        self.tabOrder = 0
        
        
    #----------------------------------------------------------------------
    def setFocus(self, val):
        self.focused = val
        self.dirty = 1

    #----------------------------------------------------------------------
    def getFocus(self):
        return self.focused

    def setPos(self, pos):
        self.rect.topleft  = pos

    #----------------------------------------------------------------------
    def kill(self):
        #self.container = None
        #del self.container
        pygame.sprite.Sprite.kill(self)
        
    #----------------------------------------------------------------------
    def onClick(self, pos):
        pass

    #----------------------------------------------------------------------
    def onKeypress(self, key, modifier):
        pass

    #----------------------------------------------------------------------
    def Notify(self, event):
        if event == GUIFocusThisWidgetEvent \
          and event.widget is self:
            self.setFocus(1)
        elif event == GUIFocusThisWidgetEvent \
          and self.focused:
            self.setFocus(0)



#------------------------------------------------------------------------------



class LabelSprite(Widget):
   
    #----------------------------------------------------------------------
    def __init__(self, evManager, caption, font_file_name=None ):
        Widget.__init__(self, evManager)

        self.size = 12

        self.font_file_name = font_file_name
        self.font = pygame.font.Font(self.font_file_name, self.size)
        self.linesize = self.font.get_linesize()
        
        self.caption = caption
        self.rect = pygame.Rect( (0,0,1,1) )

        self.color = (0,0,0)
        
        self.align = "left"

        
    #----------------------------------------------------------------------
    def setFont(self, fontfile, size=30):
        try:
            self.font = pygame.font.Font(fontfile, size)
        except:
            self.font = pygame.font.Font(None, size)
            raise Exception("Cannot load the font file")
        
        self.linesize = self.font.get_linesize()
        self.dirty = 1
        
        
            
    #----------------------------------------------------------------------
    def update(self):
        if not self.dirty:
            return

        centerx = self.rect.centerx 
        top = self.rect.top
        
        lines = self.caption.splitlines()
        w = h =0
        for line in lines:
            size = self.font.size( line.encode("latin-1") )
            w = max(size[0],w)
            h += size[1]
        
        colorkey = (255,255,255)
        surf = pygame.Surface( (w,h) ) 
        surf.set_colorkey( colorkey )
        surf.fill(colorkey)
        
        size_x = 0
        pos_y = 0

        for line in lines:
            textImg = self.font.render( line.encode("latin-1"), 1, self.color )
            x = int( (w - textImg.get_size()[0]) / 2 )
            surf.blit( textImg, (x,pos_y) )
            pos_y += self.linesize
        
        self.rect.width = w
        self.rect.height = h
        self.rect.centerx = centerx
        self.rect.top = top
        
        self.image = surf

        self.dirty = 0
