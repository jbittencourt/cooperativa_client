import os,pygame
import math
import level
import gfx
import groups
import ballon

import astar
import prefs
import visioncircle

from events import *

import sys, copy
import iso_math
import gameobjs



class CPisoplane:

    def __init__(self, evManager ):

        self.evManager = evManager
        self.evManager.RegisterListener( self , [GameEvent] )

        self.objects_plain = groups.CPzorderGroup()

        self.cenario_render_border = (0,0)

        self.objs = {}
        
        #the rect of the viewpor in the isoplane
        self.__viewport = (0,0,0,0)

        self.main_actor = ""
        
        self.curent_level = None
        self.__areas = None
        
        self.dialogs_plain = groups.relativeGroup()
        self.__user_dialogs = {}
        
        self.circle_plain = groups.relativeGroup()

    def loadLevel(self,level):

        self.curent_level = level
        

        #get objs
        for key in self.curent_level.objs.keys():
            obj, pos = self.curent_level.objs[key]
            self.addNewObj("obj_"+str(key),obj,pos)


        
        self.__tam_x = self.curent_level.x
        self.__tam_y = self.curent_level.y

        self.__areas = level.getAreas()
        
        self.__walk_method = "DIRECT"

    def setViewport(self,rect):
        self.__viewport = rect
        
        self.curent_level.render(rect)
        self.surface = self.curent_level.surface


    def getSize(self):
        return (self.__tam_x, self.__tam_y)


    def addNewObj(self, key, obj, pos3d):
        self.moveObj(obj,pos3d)

        self.objects_plain.add(obj)
        self.objs[key] = obj
                

    def setMainActor(self,key, actor):
        self.main_actor = ( key, actor )
        
        self.__vcircle = visioncircle.visionCircle( actor , self.curent_level.floor_size )
        self.circle_plain.add(self.__vcircle)
    

    def moveObj(self,obj,pos3d,range=None):
        ax,ay,z = pos3d

        pos3d = (ax+1,ay+1,z)
        
        x,y = self.isometricProjection(pos3d)

        #add half of the tile size to position the object correctly
        dx,dy = obj.iso_rect.size
        dx = self.curent_level.floor_factor_size * dy

        obj.rect.bottomright = (x+dx, y)
        obj.iso_rect.bottomright = (ax+1,ay+1)
        obj.iso_real_pos = (ax,ay)
        
        if self.__areas and self.main_actor:
            if obj==self.main_actor[1]:
                for area in self.__areas.values():
                    area.isIn(obj.iso_rect)


    def isometricProjection(self,pos3d):
        
        return iso_math.isoProjection(pos3d, 
                                      self.curent_level.floor_size,
                                      self.curent_level.original_size,
                                      self.curent_level.total_size )



    def click(self,pos):
        
        
        list = [o for o in self.objs.values() if isinstance(o,gameobjs.actionObj)]
        if list:
            list = [o for o in list if o.rect.collidepoint(pos)]
            if list:
                for o in list:
                    o.onClick()
                
                return 1
        
        x,y = iso_math.getIsoPoint(pos,
                                   self.curent_level.total_size, 
                                   self.curent_level.original_size,
                                   self.curent_level.floor_size)
        
        
        a,b = iso_math.isoProjection( (x,y,0),
                                      self.curent_level.floor_size,
                                      self.curent_level.original_size,
                                      self.curent_level.total_size )
                                      
        
        

        if x>=0 and x<self.curent_level.x and y>=0 and y<self.curent_level.y:
            
            self.event_handler((x,y,0))
            return 1

        return 0

    def event_handler(self,pos):
        x,y,z = pos
        can_click = 1
        
        
        for k in self.objs:
            if self.objs[k].collideWithMe((x,y)):
                can_click = 0
                

        if can_click:
            if self.main_actor:
                key, obj = self.main_actor
                self.evManager.Post( RequestMoveToEvent( key, (x,y) ) )
        
        



    #set a target of moviment the object in the isoplane
    def set_mov_target(self, obj, pos):
        obj.walk_to = pos
        obj.direction = obj.getDirection(pos)
        obj.setRange()
        obj.changeState("MOVING", 1)            

        


    #move the object in the isoplane
    def walk_to(self, obj):

        #speed of the moviment of the object
        speed = self.curent_level.floor_factor_size/obj.walk_speed
        tx,ty = obj.walk_to
        
        if self.__walk_method == "A_STAR":
            if not obj.walk_path:
                obj.walk_path = astar.Astar(self, obj, obj.iso_rect.topleft, obj.walk_to)
                #removes the first element that is the start position
                if obj.walk_path:
                    obj.walk_path.pop(0)

            
            if obj.walk_path==None:
                obj.walk_to = (-1, -1)
                obj.changeState("MOVING", 0)            

            else:   
                i = 0
                  
                if not obj.way_point:
                    obj.way_point = obj.walk_path.pop(0)
                    direction = obj.getDirection()
    
                    obj.animated = 1
                    obj.animate_only_moving = 1
                    if obj.direction != direction:
                        obj.direction = direction
                        obj.setRange()
                   
                
                if not self.isPositionDirty(obj.way_point, obj):
                    x0, y0 = obj.iso_real_pos
                    x, y = obj.way_point
                    x = float(x)
                    y = float(y)
                    
                    if not (x,y)==(x0,y0):
                        if x>x0:
                            tmp = x
                            x=x0+speed
                            if x>tmp:
                                x = tmp
                        elif x<x0:
                            tmp = x
                            x=x0-speed
                            if x<tmp:
                                x = tmp
                        if y>y0:
                            tmp = y
                            y=y0+speed
                            if y>tmp:
                                y = tmp
                        elif y<y0:
                            tmp = y
                            y=y0-speed
                            if y<tmp:
                                y = tmp
    
                    self.moveObj(obj,(x, y, 0))
                    if (x,y)==obj.way_point:
                        obj.way_point= None
                        
                else:
                    obj.walk_path = None
                    return 1
                
    
                if obj.iso_rect.topleft == obj.walk_to and \
                    not obj.walk_path  and \
                    not obj.way_point:
                    obj.walk_to = (-1, -1)
                    obj.changeState("MOVING", 0)
        
        elif self.__walk_method == "DIRECT":
            x,y = obj.iso_real_pos
            if tx > x:
                sum = tx-x
                if sum > speed: 
                    sum = speed
                x = x+sum
            elif tx < x:
                sum = x-tx
                if sum > speed: 
                    sum = speed
                x = x-sum
            
            if ty > y:
                sum = ty-y
                if sum > speed: 
                    sum = speed
                y = y+sum
            elif ty < y:
                sum = y-ty
                if sum > speed: 
                    sum = speed
                y = y-sum
            
            newpos = x,y
            new_tile = int(x),int(y)
            stop_moving = 0
            if self.isPositionDirty(new_tile,obj):
                stop_moving = 1
            
            dx = x - float(int(x))
            dy = y - float(int(y))
            
            if dx==0 and dy==0:
                stop_moving = 1
            
            if stop_moving:
                obj.walk_to = (-1, -1)
                obj.changeState("MOVING", 0)
            else:
                direction = obj.getDirection(obj.walk_to)
                if obj.direction != direction:
                        obj.direction = direction
                        obj.setRange()
                        return 1
                self.moveObj(obj,(x, y, 0))
            




    def isPositionDirty(self,pos, object=None):
        for obj in self.objs.values():
            if obj==object:
                continue
            
            if obj.collideWithMe(pos):
                return 1

        return 0
            


    def reorderDialogs(self, actor):
    
        #update my onw dialogs
        if len(self.__user_dialogs[actor]) ==0:
            return 0
        
        list = self.__user_dialogs[actor]
        list.sort()
        list.reverse()
        
        list[0].rect.centerx = actor.rect.centerx
        list[0].rect.bottom = actor.rect.top
        
        if len(list) == 3:
            list[2].died =1
            
        if len(list) > 1:
            list[1].rect.bottom = list[0].rect.top-5
            list[1].tick_speed = ballon.desapear_fast_speed
    
    def updateDialogs(self):
        #see if another dialogs are in ou out vision circle
        for tactor in self.__user_dialogs.keys():
            list = self.__user_dialogs[tactor]
            for diag in list:
                filled = diag.filled
                if self.__vcircle.isIn(tactor.iso_real_pos) and not filled:
                    diag.filled = 1
                    diag.render()
                elif not self.__vcircle.isIn(tactor.iso_real_pos) and filled:
                    diag.filled = 0
                    diag.render()


    def update(self):

        if not self.curent_level:
            pass


        #move objs
        for key in self.objs:
            obj = self.objs[key]
            if obj.state["MOVING"]:
                self.walk_to(self.objs[key])
                if self.__user_dialogs.has_key(self.objs[key]):
                    self.reorderDialogs(self.objs[key])
        
        
        self.updateDialogs()

        #draw the surface
        #self.surface.blit(self.curent_level.surface,(0,0))
                
        
        
        self.circle_plain.setViewport(self.__viewport,self.curent_level.floor_factor_size)
        self.objects_plain.setViewport(self.__viewport,self.curent_level.floor_factor_size)
        self.dialogs_plain.setViewport(self.__viewport,self.curent_level.floor_factor_size)
        
        self.circle_plain.clear(self.surface,self.curent_level.surface)
        self.objects_plain.clear(self.surface,self.curent_level.surface)
        self.dialogs_plain.clear(self.surface,self.curent_level.surface)

        self.circle_plain.update()
        self.circle_plain.draw(self.surface)
        
        self.objects_plain.update()
        self.objects_plain.draw(self.surface, 1)

        self.dialogs_plain.update()
        self.dialogs_plain.draw(self.surface)

        for s,k in self.objects_plain.spritedict.items():
            r = s.rect
            s.rect.topleft = s.rect.topleft

        #verify if a dialog has died
        if self.dialogs_plain:
            for diag in self.dialogs_plain.sprites():
                if diag.died:
                    self.dialogs_plain.remove(diag)
                    self.__user_dialogs[diag.actor].remove(diag)
                    del diag
                    continue
                    
        

    

    def Notify(self, event):
    
        if event==MoveToEvent:
            try:
                actor = self.objs["avatar_"+event.user_id]
            except:
                print "Cannot find actor to move"
                return 0
                
            self.set_mov_target(actor,event.pos)
            if self.__user_dialogs.has_key(actor):
                for diag in self.__user_dialogs[actor]:
                    diag.tick_speed = ballon.desapear_fast_speed
        
        elif event==TalkEvent:
            font = prefs.config.get("fonts","dialog_font")
            size = int(prefs.config.get("fonts_size","dialog_font_size"))
        
            
            actor = self.objs["avatar_"+event.user_id]
            fillcolor = (246,226,30)
            
            fill = 0
            if self.__vcircle.isIn(actor.iso_real_pos):
                fill =1 
            
            text = ballon.Ballon( actor, event.text, font, size , fillcolor, fill)
            
            self.dialogs_plain.add(text)
            if not self.__user_dialogs.has_key(actor):
               self.__user_dialogs[actor] = []
            
            self.__user_dialogs[actor].append(text)
            self.reorderDialogs(actor)
            
        elif event==ObjectChangeState:
            key = "obj_"+event.obj_id
            if self.objs.has_key(key):
                obj = self.objs[key]
                obj.changeObjStatus(event.status)
            else:
                print "Cannot find obj with code"+event.obj_id
            
        elif event==LogoutEvent:
            key = "avatar_"+event.iduser
            
            if self.objs.has_key(key):
                
                actor = self.objs[key]
                self.objects_plain.remove(actor)
                if self.__user_dialogs.has_key(actor):
                    for dialog in self.__user_dialogs[actor]:
                        dialog.died = 1
                del(self.objs[key])
            else:
                print "Cannot find avatar to logout"
            
            
            
                
           
            

            
    
