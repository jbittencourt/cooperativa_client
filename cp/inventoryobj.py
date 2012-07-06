import pygame


import gameobjs
from events import *


class iobj(gameobjs.CPgameobj):


    def __init__(self, evManager):
        gameobjs.CPgameobj.__init__(self)
        
        self.evManager = evManager
        self.possibleActions = []
        
        self.image_inventory = None
        self.human_name = "Objeto"
        
        self.rect_inventory = pygame.Rect(0,0,1,1)
        
        self.evManager.RegisterListener( self, [objActionEvent] )
        
        self.onInventory = 0
        
    
    def getInventoryImage(self):
        return self.image_inventory

        
    def loadInventoryImage(self):
        import gfx
    
        if not self.original_image.has_key(self.image_filename):
            print "Li imagem "+self.images_path+self.image_filename
            self.original_image[self.image_filename] = pygame.image.load(self.images_path+self.image_filename)
            
        self.image_inventory = self.original_image[self.image_filename].subsurface(self.rect_inventory)
    
    def handle_action(self, action):
        pass
    
    def Notify(self, event):
    
        if event==objActionEvent:
            if event.obj == self:
                self.handle_action(event.action)
