
import os
import pygame

from events import *

class CPactionArea:

    def __init__(self,area):

        x, y, w, h = area

        rect = pygame.Rect((0,0,0,0))
        rect.size = (w,h)
        rect.bottomright = (x,y)


        self.rect = rect
        self.inside = 0


    def isIn(self,area):


        if self.inside:
            if not self.rect.colliderect(area):
                self.inside = 0
                self.onLeave()
        else:
            if self.rect.colliderect(area):
                self.inside = 1
                self.onEnter()
        
        

    def onEnter(self):
        pass

    def onLeave(self):
        pass




class CPshowHideArea(CPactionArea):



    def __init__(self,rect,objs):
        CPactionArea.__init__(self,rect)

        self.objs = objs


    def onEnter(self):
        
        for obj in self.objs.values():
            obj.changeState("TRANSPARENT",1)
            
    def onLeave(self):
        
        for obj in self.objs.values():
            obj.changeState("TRANSPARENT",0)
        

class CPplayMusicArea(CPactionArea):


    def __init__(self,evManager, rect,file):
        CPactionArea.__init__(self,rect)
        self.evManager = evManager
        self.soundfile = file


    def onEnter(self):
        self.evManager.Post( loadMusicEvent(self.soundfile) )
            
    def onLeave(self):
        self.evManager.Post( stopMusicEvent() )


class CPlinkedPlayMusicArea(CPactionArea):


    def __init__(self,evManager, rect, obj):
        CPactionArea.__init__(self,rect)
        self.evManager = evManager
        self.__playng = 0
        self.obj = obj

        
         
    def refresh(self):
        if self.inside:
            self.onEnter()
        
    def onEnter(self):
        file = self.obj.getSoundFile()
        if file:
            self.evManager.Post( loadMusicEvent(file) )
            self.__playng = 1
            
    def onLeave(self):
        if self.__playng:
            self.evManager.Post( stopMusicEvent() )
            self.__playng = 0
