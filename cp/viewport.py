import pygame
import isoplane
import level
import actors
import ui

import random

import copy

from events import *

main_user_id = None

class CPviewport(ui.CPui):

    # size is a tuple with the size of the viewport
    def __init__(self, evManager , rect):

        ui.CPui.__init__(self)

        
        self.rect = rect

        self.player_data = {}
        self.follow_actor = 0
        self.actor_to_follow = ""

        self.iv_pos=  (0,0)     #relative position of the viewport in the isoplane

        self.rect = pygame.Rect(rect)

        x,y,h,w  = rect
        self.image = pygame.Surface((h,w))
        self.__size = (w , h)

        
        
        self.image.fill((255,255,255))

        #game specific
        self.evManager = evManager
        self.evManager.RegisterListener( self , [TickEvent,GameEvent] )

        iso_plane = isoplane.CPisoplane( evManager )
       
        isoplane.cenario_render_border = (0,0)
        self.setIsoplane(iso_plane)
        
        self.player_data = ""


    def get_pos(self):
        x,y,h,w  = self.rect
        return (x,y)

    #isoplane pygame.Surface or CPisoplane
    def setIsoplane(self, iso_plane):
        self.iso_plane = iso_plane
        
    def update(self):

        if not self.iso_plane.curent_level:
            return 0
    
        if self.follow_actor:
            actor, pos = self.actor_to_follow
            x1, y1, w, h = actor.rect
            if not pos == (x1, y1):
                self.iv_pos = self.calculatePosActor(actor)
                

        x,y = self.iv_pos
        x1,x2,w,h = self.rect
       

        if x < 0:
            x = 0
        if y < 0:
            y = 0

        self.iv_pos = (x,y)

        vx,vy = self.image.get_size()
        maxx, maxy = self.iso_plane.curent_level.total_size

        if maxx-vx-x < 0:
            x = maxx - vx
        if maxy-vy-y < 0:
            y = maxy - vy

        self.iso_plane.setViewport(pygame.Rect(x,y,w,h))
                                 
        
        #to limit the cliping area of the isoplane surface give
        #an enormous performace jump. 
        #self.iso_plane.surface.set_clip( (x,y,w,h) )
        self.iso_plane.update()

        #sub = self.iso_plane.surface.subsurface( (x,y,w,h) )
        sub = self.iso_plane.surface
        
        self.image.blit(sub, (0,0) )


    def onClick(self,pos):
        x1,y1 = pos
        x2, y2 = self.iv_pos
        self.iso_plane.click((x1+x2,y1+y2))


    def followActor(self, actor):
        self.follow_actor = 1
        x,y,w,h = actor.rect
        self.actor_to_follow = (actor,(x,y))

        self.iv_pos = self.calculatePosActor(actor)

    def calculatePosActor(self, actor):
        x, y, w, h = actor.rect
        x2, y2, w, h = self.rect

        x1 = x - (w/2)
        y1 = y - (h/2)

        return (x1, y1)
    

    
    def Notify(self, event):
        if event==MainPlayerEvent:
            self.player_data = copy.copy( event.player_data )
            self.evManager.Post( RequestEnterLevel(self.player_data["codHomeCenario"],(0,0)) )
        elif event==LoadLevelEvent:
            clevel = level.CPlevel(self.evManager, event.level_file_name)
            self.iso_plane.loadLevel(clevel)
            
            
            if event.users:
                for user in event.users:
                    user_id = user["id"]
                    pos = user["pos"]
                    avatar = actors.CPavatar(user["codAvatar"])
                    self.iso_plane.addNewObj("avatar_"+user_id, avatar, (pos[0], pos[1], 0) )
                    
            
        elif event==ChatStartEvent:
            import random
            out = 0
            max_x = self.iso_plane.curent_level.x
            max_y = self.iso_plane.curent_level.y
            while not out:
                x = random.randint(0,max_x-1)
                y = random.randint(0,max_y-1)
                if not self.iso_plane.isPositionDirty((x,y)):
                    out = 1
            self.evManager.Post( RequestEnterChatEvent(self.player_data["iduser"],(x,y)) )
        
        elif event==EnterChatEvent:
            avatar = actors.CPavatar(event.avatar)
            self.iso_plane.addNewObj("avatar_"+event.user_id, avatar, (event.pos[0], event.pos[1], 0) )

            if event.user_id == self.player_data["iduser"]:
                global main_user_id
                main_user_id = event.user_id
                self.followActor(avatar)
                self.iso_plane.setMainActor( event.user_id, avatar )
                
        
            
            
        

    
    
