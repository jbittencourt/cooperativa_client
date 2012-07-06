

import pygame
from pygame.locals import *

import gfx
import ui
from events import *
from objactions import *

backpack_closed = 0
backpack_open = 1


class itemsList(ui.CPui):
    
    numSlots = 5
    slotSize = (70,70)
    
    def __init__(self, evManager, rect):
        ui.CPui.__init__(self)
        
        self.evManager = evManager
        
        self.ck = (255,0,0)
        
        self.rect = pygame.Rect( rect )
        self.image = pygame.Surface( self.rect.size, HWSURFACE, 24 )
        self.image.fill(self.ck)
        self.image.set_colorkey(self.ck)
        
        #inicialize slot dict
        self.__items = {}
        for i in range(self.numSlots):
            self.__items[i] = None
        
        self.__slots_rects = []
        
        self.draw()
        
    def setItem(self, slot, item):
        
        if slot>=self.numSlots:
            raise Exception("Invalid Slot")
        
        self.__items[slot] = item
        self.draw()
        
    def draw(self):
        posy = 5
        posx = 5
        w,h = self.slotSize
        
        self.image.fill(self.ck)
        
        color = (0,0,0)
        
        for i in range(self.numSlots):
            pygame.draw.rect( self.image, color, (posx, posy, w,h), 2)
            self.__slots_rects.append( pygame.Rect( (posx, posy, w,h) ) )
            if self.__items[i]:
                img = self.__items[i].getInventoryImage()
                img.convert(self.image)
                self.image.blit( img, (posx+1, posy+1) )
            posy += 5+h
        
        self.update()
        
    def onClick(self,pos):
        slot = None
        
        posy = 5
        posx = 5
        cont = 0
        for rect in self.__slots_rects:
            if rect.collidepoint(pos):
                slot = cont
                break
            cont +=1
        
        if slot==None:
            return 0
        
        obj = self.__items[cont]
        if obj==None:
            return 0
        
        import coopdialogs
        
        diag = coopdialogs.COOPinventoryDialog( self.evManager, obj, 1) 
        self.evManager.Post( GUIDialogAddRequest( diag ) )
        
    def getNumSlots(self):
        return self.numSlots
        
    def hide(self):
        self.image.set_alpha(255)
        
    def show(self):
        self.image.set_alpha(0)
        

class back(ui.CPui):

    def __init__(self, parent):
        ui.CPui.__init__(self)
        global backpack_open, backpack_closed
        
        self.parent = parent
        
        self.images = {}
        self.images[backpack_closed] = gfx.loadImage("mochila_0.png")
        self.images[backpack_open] = gfx.loadImage("mochila_1.png")
        
    def updateState(self, state, rect):
        self.image = self.images[state]
        self.rect = self.images[state].get_rect()
        self.rect.bottomleft = rect.bottomleft
        
    def onClick(self, pos):
        self.parent.changeState()
        
    

class Backpack(ui.CPgui):

    def __init__(self, evManager, rect):
        ui.CPgui.__init__(self,evManager)
        global backpack_open, backpack_closed
        
        
        self.evManager.addListener(self, BackpackEvent)
        
        self.rect = pygame.Rect( rect )
        
        self.__backpack = back(self)
        self.__backpack.depth = 1
        
        
        self.state = backpack_closed
        self.add(self.__backpack)
        self.__backpack.updateState(self.state, self.rect)
        
        self.__list = ui.CPui()
        x,y,w,h = self.rect
        w -= 15
        h -= 10+self.__backpack.rect.height
        
        self.__list = itemsList( self.evManager, (x,y,w,h) )
        self.__list.depth = 2
        self.__list.show()
        
        self.add(self.__list)
        
        self.wants_event = 1
        
        self.items = {}
        self.__numSlots = self.__list.getNumSlots()
        for i in range(self.__numSlots):
            self.items[i] = None
        
    def changeState(self):
        global backpack_open, backpack_closed
    
        if self.state == backpack_closed:
            self.state = backpack_open
            self.__list.hide()
        elif self.state == backpack_open:
            self.state = backpack_closed
            self.__list.show()
        
        self.__backpack.updateState(self.state, self.rect)
        self.dirty = 1
        self.update()

        
    def findEmptySlot(self):
    
        ret = None
        for i in range(self.__numSlots-1,-1,-1):
            if self.items[i]==None:
                ret = i
                
        return ret
        
    def addItem(self, obj):
    
        slot = self.findEmptySlot()
        
        import viewport
        id = viewport.main_user_id
        
        if slot==None:
            msg = "Ja tenho muito peso na mochila."
            self.evManager.Post(  SendTalkEvent(id, msg) )
        else:
            #verify if item is alredy in the backpack
            in_backpack = 0
            for item in self.items.values():
                if item == None:
                    continue
                if item.__class__==obj.__class__:
                    in_backpack = 1
        
            if not in_backpack:
                self.items[slot] = obj
                self.__list.setItem(slot,obj)
                obj.onInventory = 1
            else:
                msg = obj.human_name+" !!! Ja tenho um desses na mochila."
                self.evManager.Post(  SendTalkEvent(id, msg) )
            
    def removeItem(self, obj):
        for k in self.items.keys():
            item = self.items[k]
            if item==obj:
                self.items[k] = None
                self.__list.setItem(k,None)
    
    def Notify(self, event):
    
        if event==addBackpackEvent:
            self.addItem(event.obj)
        elif event==removeBackpackEvent:
            self.removeItem(event.obj)
    
        
    
    
        

    
    
