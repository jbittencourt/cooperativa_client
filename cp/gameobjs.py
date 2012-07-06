import os,pygame
from pygame.locals import *



class CPgameobj(pygame.sprite.Sprite):

    original_image = {}
    images_path = os.path.join("data/images/")     #local path of the images
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
 
        
        self.id = -1
 

        self.images = {}             #array of the animation/state images
        self.loaded_images = 0       #total number of loades images

        self.filename = ""
        

        self.images_range = (0,0)   #define the actual range of images to be parte of animation
        self.actual_image = 0

        #animation parameters
        self.animated = 0
        self.speed = 0.0
        self.ticks = 0
        self.animate_only_moving = 0


        #state properties
        self.state = {}
        self.state["MOVING"] = 0

        #movimentation properties
        self.walk_to = (-1,-1)
        self.walk_speed = 1
        self.walk_step = 0
        self.walk_path = []
        self.way_point = None
        self.direction = None

        #size
        self.iso_rect = pygame.Rect((0,0,1,1))
        self.iso_rect.size = (1,1)
        self.iso_real_pos = (0,0)
        
        self.isSeatable = 0

        #image rect
        self.rect = ""
        
        self.dirty_rects = []
        
        self.soundEmissor = 0
        self.soundAreaSize = (0,0)
        self.soundActionArea = None
        
    def getSoundArea(self):
        if self.soundEmissor:
            w,h = self.soundAreaSize
            rect = pygame.Rect( (0,0,w,h) )
            rect.center = self.iso_rect.center
            return ( rect )
    
    def getSoundFile(self):
        return None

    def setRect(self, rect):
        self.rect = pygame.Rect(rect)


    def load(self,startpos,imgnum):

        if not self.original_image.has_key(self.image_filename):
            print "Li imagem "+self.images_path+self.image_filename
            self.original_image[self.image_filename] = pygame.image.load(self.images_path+self.image_filename)


        x,y = startpos
        x0, y0, w, h = self.rect
        
        if not self.loaded_images:
            for i in range(imgnum):
                self.images[i] = self.original_image[self.image_filename].subsurface((x,y,w,h))
                x += w
                

            self.loaded_images = imgnum
            self.images_range = (0,imgnum)

        try:
            self.image = self.images[0]
        except:
            print "Cannot load any image in "+self.image_filename
            
        self.actual_image = 0

    def changeState(self,state,value):
        self.state[state] = value
                
    def setIsoPosition(self, pos):
        self.iso_rect.bottomright = pos


    def setActualImage(self, key):
        self.actual_image = key
        self.image = self.images[key]


    def collideWithMe(self,pos):
        collide = 0
        if not self.dirty_rects:
            collide = self.iso_rect.collidepoint(pos)
        else:
            x0, y0 = self.iso_rect.topleft
            for x,y,w,h in self.dirty_rects:
                x += x0
                y += y0
                collide = pygame.Rect( (x,y,w,h) ).collidepoint( pos )
                
                if collide:
                    return collide
        
        return collide
    
    
    def getDirection(self,pos):
        #tx,ty = self.way_point
##~         if self.walk_path:
##~             pos = self.walk_path[0]
##~         else:
##~             pos = self.way_point
        tx,ty = pos 
        x,y = self.iso_rect.topleft
        direction = ""
        if tx != x or ty != y:
            if y < ty:
                direction += "S"
            elif y > ty:
                direction += "N"
            if x < tx:
                direction += "O"
            elif x > tx:
                if direction=="S" or direction=="N" and direction!="":
                    direction += "E"
                else:
                    direction += "L"
            return direction
        else:
            return 0    
    
    
    def update(self):

        animate = 0
        if self.animated:
            if self.animate_only_moving:
                if self.state["MOVING"]:
                    animate = 1
            else:
                animate = 1
        
        if (self.loaded_images > 0) and animate:

            if self.ticks >= self.frame_rate:
                self.ticks = 0
                start, end = self.images_range;
                self.image = self.images[self.actual_image]
                
                #increase to next image
                self.actual_image +=1
                if self.actual_image >= end:
                    #go to the start of the image range
                    self.actual_image = start

            self.ticks += 1

    
            
    def __lt__(self, y):
        tanx = 0.500762698
        
        a = self
        b = y

        x_a, y_a = a.rect.bottomright
        x_b, y_b = b.rect.bottomright

        change = 0
        
        if a.rect.colliderect(b.rect):
        
            iso_x_a, iso_y_a = a.iso_rect.bottomright
            iso_x_b, iso_y_b = b.iso_rect.bottomright

            iso_size_x_a, iso_size_y_a = a.iso_rect.size
            iso_size_x_b, iso_size_y_b = b.iso_rect.size

            if ((iso_x_b > iso_x_a) and  (iso_y_b > iso_y_a)):
                change = 1
            elif (iso_y_b > iso_y_a) and (iso_x_b > iso_x_a-iso_size_x_a):
                change = 1
            elif (iso_x_b > iso_x_a) and (iso_y_b > iso_y_a-iso_size_y_a):
                change = 1
            
        else:
            if y_b > y_a:
                change = 1
        
        return not change
        
    def changeObjStatus(self, state):
        pass

    

    
class actionObj(CPgameobj):

    def __init__(self, evManager):
        CPgameobj.__init__(self)

        self.evManager = evManager
        
    
    def onClick(self):
        pass
    
    
    
