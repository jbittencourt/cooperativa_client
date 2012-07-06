import pygame
from pygame.locals import *
import gameobjs

from events import *
import iobjs
import coopdialogs

class CPavatar(gameobjs.CPgameobj):
    avaiable_avatares = 14

    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self,id):
        gameobjs.CPgameobj.__init__(self)

        print "codAvatar "+id
        # a altura dos bonecos sao 108 mas
        # a altura de uma cabeca ateh outra eh de 112
        # confere antes de usar
        self.image_filename = "avatares.png"
        
        self.animated = 1
        self.animate_only_moving = 1
        
        self.walk_speed = 50
        self.name = "Avatar"
        
        #define the image size
        self.iso_rect.size = (1,1)
        self.setRect((0,0,56,108))
        
        self.changeAvatar(id)
       
        self.images_range = (0,23)
        self.speed = 1
        self.frame_rate = 1
        
        
        self.setActualImage(8)

        
    def changeAvatar(self,id):
        posy = 112*int(id)
        loadpos = (0,posy)
       
        self.load(loadpos,23)
        self.setActualImage(8)

    #set the direction for movement
    def setRange(self):
        if self.direction=="N":
            self.images_range = (4,7)
        elif self.direction=="NO":
            self.images_range = (12,15)
        elif self.direction=="O":
            self.images_range = (12,15)
        elif self.direction=="SO":
            self.images_range = (20,23)
        elif self.direction=="S":
            self.images_range = (8,11)
        elif self.direction=="SE":
            self.images_range = (8,11)
        elif self.direction=="L":
            self.images_range = (0,3)
        elif self.direction=="NE":
            self.images_range = (16,19)        
            
        self.setActualImage(self.images_range[0])


class CPsofa(gameobjs.CPgameobj):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    images = {}

    def __init__(self,tipo="0"):
        gameobjs.CPgameobj.__init__(self)


        self.image_filename = "sofas.png"

        
        if tipo=="s2L":
            self.iso_rect.size = (3,2)
            self.setRect((0,0,131,114))
            pos_stat_load = (0,0)
            images_2_load = 2
            imgnum = 0
        elif tipo=="s2LI":
            self.iso_rect.size = (2,3)
            self.setRect((0,0,127,114))
            pos_stat_load = (0,0)
            images_2_load = 2
            imgnum = 1
        elif tipo=="plt":
            self.iso_rect.size = (2,2)
            self.setRect((0,0,100,100))
            pos_stat_load = (0,125)
            images_2_load = 2
            imgnum = 0
        elif tipo=="pltI":
            self.iso_rect.size = (2,2)
            self.setRect((0,0,100,100))
            pos_stat_load = (0,125)
            images_2_load = 2
            imgnum = 1
        elif tipo=="s3B":
            self.iso_rect.size = (4,2)
            self.setRect((0,0,168,114))
            pos_stat_load = (0,256)
            images_2_load = 2
            imgnum = 0
        elif tipo=="s3BI":
            self.iso_rect.size = (2,4)
            self.setRect((0,0,158,114))
            pos_stat_load = (10,256)
            images_2_load = 2
            imgnum = 1
        elif tipo=="s2B":
            self.iso_rect.size = (3,2)
            self.setRect((0,0,135,97))
            pos_stat_load = (0,383)
            images_2_load = 4
            imgnum = 0
        elif tipo=="s2BI":
            self.iso_rect.size = (2,3)
            self.setRect((0,0,134,98))
            pos_stat_load = (0,383)
            images_2_load = 4
            imgnum = 1
        elif tipo=="s2R":
            self.iso_rect.size = (3,2)
            self.setRect((0,0,135,97))
            pos_stat_load = (0,383)
            images_2_load = 4
            imgnum = 2
        elif tipo=="s2RI":
            self.iso_rect.size = (2,3)
            self.setRect((0,0,134,98))
            pos_stat_load = (0,383)
            images_2_load = 4
            imgnum = 3

        self.animated = 0
        self.name = "sofas"

        self.load(pos_stat_load, images_2_load)
        self.setActualImage(imgnum)



class CPparede(gameobjs.CPgameobj):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self,tipo=0):
        gameobjs.CPgameobj.__init__(self)

        self.state["TRANSPARENT"] = 0

        self.iso_rect.size = (15,1)

        if tipo==0:
            self.image_prefix = "parede_a"
            self.image_suffix = ".png"
            
        self.animated = 0
        self.name = "parede"

        self.load()




    def changeState(self, state, value):

        gameobjs.CPgameobj.changeState(self,state, value)
        
        if self.state["TRANSPARENT"]:
            self.image = self.images[1]
        else:
            self.image = self.images[0]




class CPparedeLanchonete(gameobjs.CPgameobj):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    images = {}
    
    def __init__(self,tipo="0"):
        gameobjs.CPgameobj.__init__(self)
        
        self.state["TRANSPARENT"] = 0
        
        self.image_filename = "lanchonete5.png"

        #Porta Grande
        if tipo=="prtGF":
            self.iso_rect.size = (7,1)
            self.setRect((0,0,223,266))
            pos_stat_load = (0,0)
            
            self.dirty_rects.append( (0,0,2,1) )
            self.dirty_rects.append( (5,0,2,1) )
            
            images_2_load = 8
            imgnum = 0 
            
        elif tipo=="prtGFI":
            self.iso_rect.size = (1,7)
            self.setRect((0,0,223,266))
            pos_stat_load = (0,0)
            images_2_load = 8
            imgnum = 2
        elif tipo=="prtGT":
            self.iso_rect.size = (7,1)
            self.setRect((0,0,223,266))
            pos_stat_load = (0,0)
            images_2_load = 8
            imgnum = 4
        elif tipo=="prtGTI":
            self.iso_rect.size = (1,7)
            self.setRect((0,0,223,266))
            pos_stat_load = (0,0)
            images_2_load = 8
            imgnum = 6 

        #Janelas traseiras
        elif tipo=="vdrJT":
            self.iso_rect.size = (3,1)
            self.setRect((0,0,145,136))
            pos_stat_load = (0,281)
            images_2_load = 4
            imgnum = 0
        elif tipo=="vdrJTI":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,145,136))
            pos_stat_load = (0,281)
            images_2_load = 4
            imgnum = 2
        elif tipo=="jnlT":
            self.iso_rect.size = (3,1)
            self.setRect((0,0,116,216))
            pos_stat_load = (0,442)
            images_2_load = 4
            imgnum = 0
        elif tipo=="jnlTI":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,116,216))
            pos_stat_load = (0,442)
            images_2_load = 4
            imgnum = 2
            
        #janelas da frente
        elif tipo=="vdrJF":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,115,160))
            pos_stat_load = (0,673)
            images_2_load = 4
            imgnum = 0 
        elif tipo=="vdrJFI":
            self.iso_rect.size = (3,1)
            self.setRect((0,0,115,160))
            pos_stat_load = (0,673)
            images_2_load = 4
            imgnum = 2
        elif tipo=="jnlF":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,115,213))
            pos_stat_load = (0,844)
            images_2_load = 4
            imgnum = 0
        elif tipo=="jnlFI":
            self.iso_rect.size = (3,1)
            self.setRect((0,0,115,213))
            pos_stat_load = (0,844)
            images_2_load = 4
            imgnum = 2            

        #Paredes Lisas e Basculantes
        elif tipo=="prdB":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,120,220 ))
            pos_stat_load = (0,1075)
            images_2_load = 10
            imgnum = 0 
        elif tipo=="prdL":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,105,215))
            pos_stat_load = (10,1075)
            images_2_load = 10
            imgnum = 2
        elif tipo=="prdLL":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,117,220))
            pos_stat_load = (0,1075)
            images_2_load = 10
            imgnum = 2
        elif tipo=="prdLLI":
            self.iso_rect.size = (3,1)
            self.setRect((0,0,114,211))
            pos_stat_load = (0,1075)
            images_2_load = 10
            imgnum = 4 
        elif tipo=="prdLI":
            self.iso_rect.size = (3,1)
            self.setRect((0,0,113,220))
            pos_stat_load = (0,1075)
            images_2_load = 10
            imgnum = 4 
        elif tipo=="prtP":
            self.iso_rect.size = (3,1)
            self.setRect((0,0,113,220))
            pos_stat_load = (0,1075)
            images_2_load = 10
            imgnum = 6
        elif tipo=="prtPI":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,115,212))
            pos_stat_load = (0,1075)
            images_2_load = 10
            imgnum = 8 


        #Cantos da Parede
        elif tipo=="prdCID":
            self.iso_rect.size = (1,1)
#            self.setRect((0,0,70,193))
            self.setRect((0,0,63,189))
            pos_stat_load = (0,1309)
            images_2_load = 8
            imgnum = 0 
        elif tipo=="prdCSD":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,66,186))
            pos_stat_load = (0,1309)
            images_2_load = 8
            imgnum = 2
        elif tipo=="prdCIE":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,67,190))
            pos_stat_load = (0,1309)
            images_2_load = 8
            imgnum = 4
        elif tipo=="prdCSE":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,67,191))
            pos_stat_load = (0,1309)
            images_2_load = 8
            imgnum = 6

        
        #paredes pequenas (emendas)
        elif tipo=="prdP":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,59,184))
            pos_stat_load = (0,1520)
            images_2_load = 4
            imgnum = 0 
        elif tipo=="prdPI":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,59,184))
            pos_stat_load = (0,1520)
            images_2_load = 4
            imgnum = 2 
            

   
        self.animated = 0
        self.name = "paredes lanchonete"
        
        self.load(pos_stat_load, images_2_load)
        
        self.setActualImage(imgnum)
        

    def changeState(self, state, value):

        gameobjs.CPgameobj.changeState(self,state, value)
        
        if state=="TRANSPARENT":
            if self.state["TRANSPARENT"]:
                self.setActualImage(self.actual_image+1)
            else:
                self.setActualImage(self.actual_image-1)



class CPObjectLanchonete(gameobjs.CPgameobj):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    images = {}
    
    def __init__(self,tipo="0"):
        gameobjs.CPgameobj.__init__(self)
        
        self.state["TRANSPARENT"] = 0
        
        self.image_filename = "obj_lanchonete.png"

        if tipo=="cdrF":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,52,82))
            pos_stat_load = (0,0)
            images_2_load = 2
            imgnum = 0
        elif tipo=="cdrFI":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,52,82))
            pos_stat_load = (0,0)
            images_2_load = 2
            imgnum = 1 
        elif tipo=="cdrC":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,52,75))
            pos_stat_load = (0,76)
            images_2_load = 2
            imgnum = 0
        elif tipo=="cdrCI":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,52,71))
            pos_stat_load = (0,82)
            images_2_load = 2
            imgnum = 1 
        elif tipo=="msP":
            self.iso_rect.size = (2,1)
            self.setRect((0,0,84,85))
            pos_stat_load = (0,150)
            images_2_load = 2
            imgnum = 0 
        elif tipo=="msPI":
            self.iso_rect.size = (1,2)
            self.setRect((0,0,87,83))
            pos_stat_load = (0,150)
            images_2_load = 2
            imgnum = 1
        elif tipo=="msG":
            self.iso_rect.size = (3,3)
            self.setRect((0,0,160,137))
            pos_stat_load = (0,236)
            images_2_load = 2
            imgnum = 0        
        elif tipo=="Iblco":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,136,159))
            pos_stat_load = (0,562)
            images_2_load = 2
            imgnum = 0 
        elif tipo=="Fblco":
            self.iso_rect.size = (4,1)
            self.setRect((0,0,145,196))
            pos_stat_load = (0,722)
            images_2_load = 2
            imgnum = 0 

   
        self.animated = 0
        self.name = "object lanchonete"
        
        self.load(pos_stat_load, images_2_load)
        
        self.setActualImage(imgnum)
        

    def changeState(self, state, value):

        gameobjs.CPgameobj.changeState(self,state, value)
        
        if state=="TRANSPARENT":
            if self.state["TRANSPARENT"]:
                self.setActualImage(self.actual_image+1)
            else:
                self.setActualImage(self.actual_image-1)

class CPObjectPraca(gameobjs.CPgameobj):
    
    images = {}
    
    def __init__(self,tipo="0"):
        gameobjs.CPgameobj.__init__(self)
        
        self.state["TRANSPARENT"] = 0
        
        self.image_filename = "obj_praca.png"

        if tipo=="cxcrr":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,50,79))
            pos_stat_load = (0,0)
            images_2_load = 2
            imgnum = 0
        elif tipo=="cxcrrI":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,50,79))
            pos_stat_load = (0,0)
            images_2_load = 2
            imgnum = 1
        elif tipo=="cxcrr2":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,50,95))
            pos_stat_load = (0,88)
            images_2_load = 2
            imgnum = 0
        elif tipo=="cxcrr2I":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,50,95))
            pos_stat_load = (0,88)
            images_2_load = 2
            imgnum = 1
        elif tipo=="arvrP":
            self.iso_rect.size = (1,1)
            self.setRect((10,0,88,90))
            pos_stat_load = (0,202)
            images_2_load = 2
            imgnum = 0
        elif tipo=="arvrM":
            self.iso_rect.size = (1,1)
            self.setIsoPosition((40,30)) 
            self.setRect((0,0,179,221))
            pos_stat_load = (0,1048)
            images_2_load = 1
            imgnum = 0
        elif tipo=="arvrG":
            self.iso_rect.size = (1,1)
            self.setRect((0,0,416,310))
            pos_stat_load = (0,736)
            images_2_load = 1
            imgnum = 0
        elif tipo=="fnt":
            self.iso_rect.size = (4,4)
            self.setRect((0,0,224,183))
            pos_stat_load = (0,540)
            images_2_load = 1
            imgnum = 0
        elif tipo=="arbst":
            self.iso_rect.size = (1,4)
            self.setRect((0,0,150,123))
            pos_stat_load = (0,287)
            images_2_load = 2
            imgnum = 0
        elif tipo=="arbst1":
            self.iso_rect.size = (4,1)
            self.setRect((0,0,150,123))
            pos_stat_load = (0,287)
            images_2_load = 2
            imgnum = 1
        elif tipo=="arbst2":
            self.iso_rect.size = (1,4)
            self.setRect((0,0,150,123))
            pos_stat_load = (0,410)
            images_2_load = 2
            imgnum = 0
        elif tipo=="arbst3":
            self.iso_rect.size = (4,1)
            self.setRect((0,0,150,123))
            pos_stat_load = (0,410)
            images_2_load = 2
            imgnum = 1
        elif tipo=="bncP":
            self.iso_rect.size = (3,1)
            self.setRect((0,0,135,125))
            pos_stat_load = (0,1450)
            images_2_load = 2
            imgnum = 0
            self.isSeatable = 1
        elif tipo=="bncPI":
            self.iso_rect.size = (1,3)
            self.setRect((0,0,135,125))
            pos_stat_load = (0,1450)
            images_2_load = 2
            imgnum = 1
            self.isSeatable = 1

        
        self.animated = 0
        self.name = "object lanchonete"
        
        self.load(pos_stat_load, images_2_load)
        
        self.setActualImage(imgnum)
        

        
class CPminiSystem(gameobjs.actionObj):

    def __init__(self, init, evManager):
        gameobjs.actionObj.__init__(self, evManager)
        
        self.image_filename = "minisystem.png"
        
        self.iso_rect.size = (2,1)
        self.setRect((0,0,93,117))
        
        images_2_load = 1
        imgnum = 0
        pos_stat_load = (0,0)
        
        self.load(pos_stat_load, images_2_load)
        self.setActualImage(imgnum)
        
        self.__status = 0

        self.soundAreaSize = (12,12)
        self.soundEmissor = 1
        self.__status = 0
        
        self.__musics = { 0: "progressive.wav",
                          1: "theme1.wav"
                        }
    
        
    def onClick(self):
        
        next = self.__status +1
        
        if not self.__musics.has_key(next):
            next = 0
        
        self.evManager.Post( SendObjectChangeState( self.id , next ) )
        
    def getSoundFile(self):
        return self.__musics[self.__status]

    def changeObjStatus(self,status):
        self.__status = int(status)
        self.soundActionArea.refresh()
        

class CPbancahotdog(gameobjs.actionObj):

    def __init__(self, tipo, evManager):
        gameobjs.actionObj.__init__(self, evManager)
        
        self.image_filename = "obj_praca.png"
        if tipo=="N":
            self.iso_rect.size = (2,3)
            self.setRect((0,0,135,164))
            pos_stat_load = (0,1276)
            images_2_load = 2
            imgnum = 0
        elif tipo=="I":
            self.iso_rect.size = (3,2)
            self.setRect((0,0,135,164))
            pos_stat_load = (0,1276)
            images_2_load = 2
            imgnum = 1
        
        self.load(pos_stat_load, images_2_load)
        self.setActualImage(imgnum)

    def onClick(self):
        import iobjs
    
        obj = iobjs.hotdog(0, self.evManager)
        self.evManager.Post( GUIDialogAddRequest( coopdialogs.COOPinventoryDialog( self.evManager, obj) ) )


        
class CPgeladeira(gameobjs.actionObj):

    def __init__(self, tipo, evManager):
        gameobjs.actionObj.__init__(self, evManager)
        
        self.image_filename = "obj_lanchonete.png"
        
        self.iso_rect.size = (1,3)
        self.setRect((0,0,104,161))
        pos_stat_load = (0,401)
        images_2_load = 2
        imgnum = 0
        
        self.load(pos_stat_load, images_2_load)
        self.setActualImage(imgnum)

    def onClick(self):
        import iobjs
    
        print "Aqui4"
        obj = iobjs.garrafa_dagua(0, self.evManager)
        self.evManager.Post( GUIDialogAddRequest( coopdialogs.COOPinventoryDialog( self.evManager, obj) ) )



# Actors dict is used by level.py to map xml instance string into objets
actorsDict = {               "sofas": CPsofa,
                            "parede": CPparede,
                "parede_lanchonete": CPparedeLanchonete,
                "object_lanchonete": CPObjectLanchonete,
                      "object_praca": CPObjectPraca,
                      "banca_hotdog": CPbancahotdog,
                         "geladeira": CPgeladeira,
                      "minisystem": CPminiSystem
             }

             
             
