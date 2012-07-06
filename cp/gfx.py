import os, pygame
from pygame.locals import *

import prefs

def loadImage(name, path=None):
    
    if not path:
        fullname = prefs.config.get("paths","images")+"/"+name
    else:
        fullname = path+"/"+name

    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message\
              
    #image = image.convert()
    
        
    return image
    
def loadImageSlices(filename, rect, num):

    image = loadImage(filename)
    
    x,y,w,h = rect
    images = {}
    for i in range(num):
        images[i] = image.subsurface(( x+(i*w) , y , w ,h ))

    return images

def rotate45(pos):

    x, y  = pos
    
    siny = cosy = 0.707

    xpos = -y*siny+x*cosy
    ypos = -y*cosy-x*siny

    return (xpos, ypos)


def unrotate45(pos):

    x, y  = pos

    siny = cosy = -0.707

    xpos = -y*siny + x*cosy
    ypos = -y*cosy - x*siny

    return (xpos, ypos)
