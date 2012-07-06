

import pygame
from pygame.locals import *
from math import pi

import textwrap
import time
import dialogrender


desapear_fast_speed = 4
desapear_slow_speed = 1


class Ballon(pygame.sprite.Sprite):

    def __init__(self, actor, text, fontfile, size, fillcolor, filled):
        pygame.sprite.Sprite.__init__(self)
        
        self.actor = actor
        self.inicialized = 0
        self.font = pygame.font.Font(fontfile, size)
        self.linesize = self.font.get_linesize()
        
        self.text = textwrap.wrap(text, 25)
        self.filled = filled
        self.fillcolor = fillcolor
        
        self.inicial_altha = 200
        
        self.render()
        
        self.ticks_to_die = 150 + (10*self.total_len)
        self.ticks = 0
        self.tick_speed = 1
        
        self.died = 0
        self.time = time.time()
        
        if not self.filled:
            self.inicial_altha = self.inicial_altha/2
            self.ticks_to_die = self.ticks_to_die *2               
           
        self.image.set_alpha(self.inicial_altha)

    def __lt__(self, y):
        return self.time < y.time
    
    def __gt__(self, y):
        return self.time > y.time    
        
    def update(self):
        tick_rate = 255.0 /  float(self.ticks_to_die / 2)
        self.ticks += self.tick_speed
        if self.ticks > (self.ticks_to_die / 2):
            tick = self.ticks - (self.ticks_to_die / 2)
            self.image.set_alpha( self.inicial_altha - int( tick_rate * tick ) )
            
            if int( tick_rate * tick )>255:
                self.died = 1
            
    
    
    def render(self):
        max = 0
        for line in self.text:
            #tam = self.font.size( line )[0]
            tam = dialogrender.size(line, self.font)[0]
            if tam > max:
                max = tam
        
        inner_y = self.linesize * len(self.text)
        inner_x = max
        
        if inner_x < 40:
            inner_x = 40
        
        if inner_y < 40:
            inner_y = 40
        
        outer_x = int( inner_x * 1.2 )
        outer_y = int( inner_y * 1.5 )
       
        if not self.inicialized:
            self.image = pygame.Surface( (outer_x, outer_y) )
            self.rect = pygame.Rect( (0, 0, outer_x, outer_y) )
        
        self.image.fill( (255,255,128) )
        self.image.set_colorkey( (255,255,128) )
        
        
        # draw a box
        drawBallon(self.image, self.rect, inner_y , 2, (0,0,0), self.fillcolor)
        
        h = int(inner_y * 1.2)
        
        textColor = (0,0,0)
        pos_y = int( ( h - inner_y ) /2 )
        border = int( ( outer_x - inner_x ) /2 )
        total_len = 0
        for line in self.text:
            #tempImg = self.font.render( line.encode("latin-1"), 1, textColor )
            tempImg = dialogrender.render( line.encode("utf-8"), self.font, textColor )
            if self.filled:
                self.image.blit( tempImg, (border, pos_y) )
            pos_y += self.linesize
            total_len += len(line)    
            
        self.total_len = total_len
        self.dirty = 1
        
        
            
        self.inicialized = 1

    
def drawBallon(im, rect, inner_y ,lw, c, fc):
    
    x,y,w,hr = rect
    h = int(inner_y * 1.2)
            
    round = 15
    cround = round * 2
    
    brech = 20
    size = int((w-round)/2)-brech
    center = (int(w/2),hr)
            
    #draw the ballon fill        
    
    pygame.draw.circle(im, fc, (round,round), round  , 0)
    pygame.draw.circle(im, fc, (w-round,round), round , 0)
    pygame.draw.circle(im, fc, (w-round,h-round), round , 0)
    pygame.draw.circle(im, fc, ( round, h-round), round , 0)

    p0= (  round,       0)
    p1= (w-round,       0)
    p2= (   w-lw,   round)
    p3= (   w-lw, h-round)
    p4= (  w-round, h)
    p5= (    round, h)
    p6= (      0, h-round)
    p7= (      0, round-1)
        
    
    p = [p0,p1,p2,p3,p4,p5,p6,p7]
    pygame.draw.polygon(im, fc, p, 0)
    
    
    p1 = (round+size, h)
    p2 = (w-round-size, h)
    
    p = [p1,center,p2]
    pygame.draw.polygon(im, fc, p, 0)


    
    #draw the ballon line
    pygame.draw.arc(im, c, Rect(0       ,0      , cround,cround), pi * 0.5 , pi * 1  , lw)
    pygame.draw.arc(im, c, Rect(w-cround,0      , cround,cround), pi * 0   , pi * 0.5, lw)
    pygame.draw.arc(im, c, Rect(0       ,h-cround, cround,cround), pi * 1.0 , pi * 1.5, lw)
    pygame.draw.arc(im, c, Rect(w-cround,h-cround, cround,cround), pi * 1.5 , pi * 2.0, lw)
    
            
    pygame.draw.line(im, c, ( round,       0), (w-round,       0), lw)
    pygame.draw.line(im, c, (     0, round-1), (      0, h-round), lw)
    pygame.draw.line(im, c, (  w-lw,   round), (      w-lw, h-round), lw)
            
    #seta
    pygame.draw.line(im, c, (       round-1, h), ( round+size, h), lw)
    pygame.draw.line(im, c, (  w-round-size, h), (    w-round, h), lw)
    
    pygame.draw.line(im, c, (    round+size, h), center, lw)
    pygame.draw.line(im, c, (  w-round-size, h), center, lw)

