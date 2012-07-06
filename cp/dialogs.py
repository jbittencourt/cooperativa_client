import pygame
import ui


class Dialog(ui.CPgui):

    def __init__(self, evManager):
        ui.CPgui.__init__(self, evManager)
        
        self.__background = None
        self.rect = pygame.Rect( (0,0,1,1) )
        
    def setBackground(self, background):
        
        if not self.__background==None:
            self.remove(self.__background)
            
        ui.CPgui.add(self,background)
        self.__background = background
        self.__background.depth = 0
                
    def setPos(self, pos):
        self.rect.topleft = pos
        x,y = pos
        if self.__background:
            self.__background.rect.topleft = pos
    
    def adjustPos(self, obj):
        x,y = self.rect.topleft
        obj.rect.left += x
        obj.rect.top += y
        
    def add(self, sprite):
        if not sprite: return
        
        sprite.rect.top += self.rect.top
        sprite.rect.left += self.rect.left
        ui.CPgui.add(self,sprite)
  
    def wantsEvent(self, event):
        return 1

