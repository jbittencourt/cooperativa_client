#file level.py

import os,pygame, math
from pygame.locals import *


#xml includes
import string
import xml.dom.minidom
import sys, re


#import re, array
import actors
import actionareas
import gfx
import iso_math
import gameobjs


class CPlevel:
    
    def __init__(self, evManager,xmlfile):

        self.images = {}

        self.name = ""
        self.objs = {}
        self.areas = {}
        
        self.evManager = evManager

        self.__xmlfile = xmlfile
        self.__loadXMLFile()

        
        
        self.floor_size = (40,40)
        self.floor_cut_size = (50,50)
        
        #self.floor_factor_size = 27.0
        self.floor_factor_size = (self.floor_size[0]/2)*math.sqrt(2)

                
        #self.renderIsoPlane()
        self.__loadImages()
        self.__loadFloor()
        
        
    

        self.original_size = ( self.floor_size[0]*self.x ,
                               self.floor_size[1]*self.y )
                               
        
        sin26_6 = 0.707106781
        cos26_6 = 0.707106781
        # 26.6 is the angle between the isometric floor and the base of the screen
        # tam_y = a+b where a = sin 26.6 * y and b = sin 26.6 * x
        x = float(self.x * self.floor_size[0])
        y = float(self.y * self.floor_size[1])
        tam_y = math.ceil( ((sin26_6*y) + (sin26_6*x)) /2 )
        
        # tam_x = c+d where c = cos 26.6 * y and d = cos 26.6 * x
        tam_x = math.ceil((cos26_6*y) + (cos26_6*x))
        
        self.total_size = (tam_x, tam_y)
        


    
    def getAreas(self):
        return self.areas


    def __loadFloor(self):
    
        self.__floor_array = []
        
        self.x = self.y =0
        for line in self.STAGE.split('='):
            self.y+=1
            self.x =0
            line = re.sub(r'[^ -z]','',line)
            row = []
            for i in line:
                row.append(i)
                self.x+=1
                
            
            self.__floor_array.append(row)
        
        
    def render(self,rect):
       
        x0, t = iso_math.getIsoPoint(rect.topleft ,
                                      self.total_size,
                                      self.original_size,
                                      self.floor_size)
        t,  y0 = iso_math.getIsoPoint(rect.topright ,
                                      self.total_size,
                                      self.original_size,
                                      self.floor_size)
        
        t, y1  =iso_math.getIsoPoint(rect.bottomleft ,
                                      self.total_size,
                                      self.original_size,
                                      self.floor_size)
        
        x1, t = iso_math.getIsoPoint(rect.bottomright ,
                                      self.total_size,
                                      self.original_size,
                                      self.floor_size)
        
        x0-=1
        y0-=1
        x1+=1
        y1+=1
        
        if x0 < 0:
            x0 = 0
        if y0 < 0:
            y0 = 0
        
        if x1>self.x:
            x1 = self.x
        if y1>self.y:
            y1 = self.y
        
        tam_x, tam_y = rect.size
        
        self.surface = pygame.surface.Surface( (tam_x, tam_y) )
        
        #color of a blue sky
        self.colorKey = (124, 172, 253)
        
        self.surface.fill(self.colorKey)
        
        for x in range(x0,x1):
            for y in range(y0,y1):
                
                i = self.__floor_array[y][x]
                posx, posy = iso_math.isoProjection( (x,y,0) ,
                                                     self.floor_size,
                                                     self.original_size,
                                                     self.total_size )
                
                posx -= rect.left + self.floor_factor_size
                posy -= rect.top
                
                self.surface.blit(self.images[i],(posx,posy))


    def __loadImages(self):
        fullPath = os.path.join('data/images/')


        image = pygame.image.load(fullPath+"floor.png")
        try:
            image = pygame.image.load(fullPath+"floor.png")
        except:
            print "Cannot load the floor image file"
            sys.exit()

        color_key = image.get_at((0,0))
        image.set_colorkey(color_key,HWACCEL)
        image.convert()
        
        
        w, h = self.floor_cut_size
        tam = image.get_size()[0] / w
        for k in range(int(tam)):
            i = ""
            if k > 9:
                i = chr( 97 + k - 10 )
            else:
                i = str(k)
            self.images[i] = image.subsurface( ( w*k, 0, w, h ) )
            
        
        print "Start Rotating floor images"
        for k in self.images:
            
            self.images[k] = pygame.transform.rotate(self.images[k],-45)
            x,y = self.images[k].get_size()
            self.images[k] = pygame.transform.scale(self.images[k],(x,y/2))
        
        print "End Rotating floor images"    

        
    def __loadXMLFile(self):

        fullname = os.path.join("data/levels/"+self.__xmlfile)

        xmldoc = xml.dom.minidom.parse(fullname)

        try:
            xmldoc = xml.dom.minidom.parse(fullname)
        except:
            print "Cannot read XML level description file:"+fullname
            sys.exit()
            

        #reads the name of the cenario
        desc = xmldoc.getElementsByTagName("descrition")
        desc = desc.item(0)

        for k in range(desc.attributes.length):
            attr = desc.attributes.item(k)
            if attr.name == "name":
                self.name = attr.value

        #reads the flor definition string
        stage = ""
        floor =  xmldoc.getElementsByTagName("floor")

        for data in floor.item(0).childNodes:
            stage += data.data

        self.STAGE = stage


        #reads the actors and objects
        #<object id="0" instante="sofa" posx="10" posy="10">
        objs = xmldoc.getElementsByTagName("objects")
        objs = objs.item(0)
        


        if objs.hasChildNodes():
            
            groups = objs.getElementsByTagName("object_group")
            
            for group in groups:
            
                if group.hasAttributes():
                    egx = group.getAttributeNode("posx")
                    egy = group.getAttributeNode("posy")
                    gx = int(egx.value)
                    gy = int(egy.value)
                else:
                    print "Group dont have a position"
                    continue
            
            
                obj_list = group.getElementsByTagName("object")

            
                for node in obj_list:
                    if node.hasAttributes():
                        new_obj = ""

                        instance = ""
                        id = -1 
                        x = 0
                        y = 0
                        z = 0
                        init = 0

                    
                        for k in range(node.attributes.length):
                            attr = node.attributes.item(k)
                            if attr.name == "instance":
                                instance = attr.value
                            elif attr.name == "id":
                                id = int(attr.value)
                            elif attr.name == "posx":
                                x = int(attr.value)
                            elif attr.name == "posy":
                                y = int(attr.value)
                            elif attr.name == "posz":
                                z = attr.value
                            elif attr.name == "init":
                                init = attr.value


                        
                        
                        if id >= 0:
                            if actors.actorsDict.has_key(instance):
                                objclass = actors.actorsDict[instance]
                                    
                                if issubclass( objclass, gameobjs.actionObj ):
                                    new_obj = objclass(init, self.evManager)
                                    print instance
                                else:
                                    new_obj = objclass(init)

                                new_obj.id = id
                                self.objs[id] = (new_obj,(gx+x,gy+y,z))
                                
                                
                                if new_obj.soundEmissor:
                                    rect = new_obj.getSoundArea()
                                    rect.bottom += gy +x
                                    rect.right += gx +y
                                    
                                    nrect = ( rect.right,rect.bottom, rect.width, rect.height )
                                        
                                    new_area = actionareas.CPlinkedPlayMusicArea(self.evManager, nrect,new_obj)
                                    self.areas[self.areas.__len__()] = new_area
                                    new_obj.soundActionArea = new_area
                                




        #construct the action areas
        areas = xmldoc.getElementsByTagName("areas")
        areas = areas.item(0)


        if areas.hasChildNodes():
            area_list = areas.getElementsByTagName("area")
            
            for node in area_list:
                if node.hasAttributes():
                    new_area = ""

                    x = 0
                    y = 0
                    w = 0
                    h = 0
                    sound = ""
                    type = ""
                    objs = {}

                    
                    for k in range(node.attributes.length):
                        attr = node.attributes.item(k)
                        if attr.name == "type":
                            type = attr.value
                        elif attr.name == "x":
                            x = int(attr.value)
                        elif attr.name == "y":
                            y = int(attr.value)
                        elif attr.name == "w":
                            w = int(attr.value)
                        elif attr.name == "h":
                            h = int(attr.value)
                        elif attr.name == "music":
                            sound = attr.value


                    if type=="showhide":
                        #search for the objects
                        cont = 0
                        if node.hasChildNodes():
                             objs_list = node.getElementsByTagName("object")
                             for node in objs_list:
                                 objs[cont],pos = self.objs[int(node.attributes.item(0).value)]
                                 cont += 1

                             new_area = actionareas.CPshowHideArea((x,y,w,h),objs)
                    elif type=="music":
                        new_area = actionareas.CPplayMusicArea(self.evManager, (x,y,w,h),sound)


                    if new_area:
                        self.areas[self.areas.__len__()] = new_area
            
