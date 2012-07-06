''' Inventariable objects '''
import pygame

import inventoryobj
from objactions import *
from events import *



        
class hotdog(inventoryobj.iobj):

    def __init__(self, init, evManager):
        inventoryobj.iobj.__init__(self, evManager)
    
        self.image_filename = "iobjs.png"
        
        self.iso_rect.size = (1,1)
        self.setRect((0,0,50,25))
        
        images_2_load = 1
        imgnum = 0
        pos_stat_load = (0,70)
    
        self.image_inventory = None
        self.human_name = "Cachorro-quente"
        
        self.rect_inventory = pygame.Rect(50,70,70,70)
        
        self.load(pos_stat_load, images_2_load)
        self.setActualImage(imgnum)
        self.loadInventoryImage()
        
        
        self.possible_actions = [storeAction,eatAction]
    

    def handle_action(self, action):
        import viewport
        id = viewport.main_user_id
        
        if isinstance(action,eatAction):
            msg = "Hummmm!!! "
            self.evManager.Post( SendTalkEvent(id, msg) )
            
            if self.onInventory:
                self.evManager.Post( removeBackpackEvent(self) )
            
        elif isinstance(action,storeAction):
            self.evManager.Post( addBackpackEvent(self) )

            
            
class garrafa_dagua(inventoryobj.iobj):

    def __init__(self, init, evManager):
        inventoryobj.iobj.__init__(self, evManager)
    
        self.image_filename = "iobjs.png"
        
        self.iso_rect.size = (1,1)
        self.setRect((0,0,50,25))
        
        images_2_load = 1
        imgnum = 0
        pos_stat_load = (0,70)
    
        self.image_inventory = None
        self.human_name = "Garrafa com agua"
        
        self.rect_inventory = pygame.Rect(50,140,70,70)
        
        self.load(pos_stat_load, images_2_load)
        self.setActualImage(imgnum)
        self.loadInventoryImage()
        
        
        self.possible_actions = [storeAction,eatAction]
    

    def handle_action(self, action):
        import viewport
        id = viewport.main_user_id
        
        if isinstance(action,eatAction):
            msg = "Ahhhh. "
            self.evManager.Post( SendTalkEvent(id, msg) )
            
            if self.onInventory:
                self.evManager.Post( removeBackpackEvent(self) )
            
        elif isinstance(action,storeAction):
            self.evManager.Post( addBackpackEvent(self) )
