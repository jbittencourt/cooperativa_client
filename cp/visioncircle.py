import pygame
import math



class visionCircle(pygame.sprite.Sprite):
    diameter = 10

    def __init__(self, actor, floor_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.__actor = actor
        self.__floor_size = floor_size
        
        
        w,h = self.draw()
        
        self.rect = pygame.Rect( (0,0,w,h) )
        self.iso_rect = pygame.Rect( (0,0,self.diameter,self.diameter) )
        
        self.update()
        
    def draw(self):
    
        sizex = self.diameter * self.__floor_size[0]
        sizey = int(sizex/2)
        
        ck = (234, 234, 02)
        self.image = pygame.surface.Surface( (sizex, sizey) )
        self.image.fill( ck )
        self.image.set_colorkey( ck )
        self.image.set_alpha(90)
        
        color = (0,0,0)
        colorf = (244,226,28)
               
        
        pygame.draw.ellipse(self.image, colorf,  (2,2,sizex-2,sizey-2), 0)
        pygame.draw.ellipse(self.image, color,  (2,2,sizex-2,sizey-2), 2)
        
        
        
        return (sizex, sizey)
        
    def isIn(self,pos):
        
        if not self.iso_rect.collidepoint(pos):
            return 0
        
        x = math.fabs(pos[0] - self.iso_real_pos[0] )
        y = math.fabs(pos[1] - self.iso_real_pos[1] )
        
        d = math.hypot(x,y)
        if d < (self.diameter/2):
            return 1
        
        return 0
        
    def update(self):
    
        self.rect.centerx = self.__actor.rect.centerx
        self.rect.centery = self.__actor.rect.bottom
        self.iso_real_pos = self.__actor.iso_real_pos
        
        self.iso_rect.center = self.iso_real_pos
