import pygame
from pygame.locals import *
from pygame.sprite import *
import math
import copy

import gameobjs
import quicksort

class relativeGroup(pygame.sprite.RenderClear):
    """A group that change the postition of
    the sprites on render time to a set viewport"""
    
    def __init__(self):
        pygame.sprite.RenderClear.__init__(self)
        self.relative = 1

    def setViewport(self,viewport,factor):
        self.viewport = viewport
        self.factor = factor
    
    def draw(self,surface):

        spritedict = self.spritedict
        items = spritedict.items()

        dirty = self.lostsprites
        self.lostsprites = []

        #Z Buffer

        v = self.viewport.colliderect
        zlevel = [item for item in items if v(item[0].rect)]
        

        if zlevel.__len__() > 0:
            
            for k in range(len(zlevel)):
                s,r = zlevel[k]
                
                r = copy.copy(s.rect)
                if self.relative:
                    r.top -=  self.viewport.top
                    r.left-=  self.viewport.left
                
                newrect = surface.blit(s.image,r.topleft)

                if r is not 0:
                    dirty.append(newrect.union(r))
                else:
                    dirty.append(newrect)

                spritedict[s] = newrect
                
            return dirty




class  CPzorderGroup(relativeGroup):


    def __init__(self):
        relativeGroup.__init__(self)

    
    def draw(self,surface, relative=0):

        spritedict = self.spritedict
        items = spritedict.items()

        dirty = self.lostsprites
        self.lostsprites = []

        #Z Buffer

        #test if the obj is being visualized in the screen now.
        # if not, they dont need to be z-buffered
        v = self.viewport.colliderect
        zlevel = [item for item in items if v(item[0].rect)]
        

        if zlevel.__len__() > 0:
            quicksort.quicksort(zlevel,0,zlevel.__len__()-1)
            
            #zlevel.sort(cmp)
            
            a = range(zlevel.__len__())
            a.reverse()

            for k in a:
                s,r = zlevel[k]
                
                r = copy.copy(s.rect)
                if self.relative:
                    r.top -=  self.viewport.top
                    r.left-=  self.viewport.left
                
                newrect = surface.blit(s.image,r.topleft)

                if r is not 0:
                    dirty.append(newrect.union(r))
                else:
                    dirty.append(newrect)

                spritedict[s] = newrect
                
            return dirty
 

            
class layeredGroup(RenderUpdates):
    """..."""
    def __init__(self, sprite=[]):
        RenderUpdates.__init__(self, sprite)
        self.orderedSprites = []

    def add_internal(self, sprite):
        #prevent duplication
        if self.spritedict.has_key( sprite ):
            return

        RenderUpdates.add_internal(self, sprite)

        if not hasattr( sprite, 'depth' ):
            #TODO: is this legal?
            sprite.depth = 0

        self.orderedSprites.append( sprite )
        
        fn = lambda x,y: x.depth - y.depth
        self.orderedSprites.sort(fn)
        

    def remove_internal(self, sprite):
        RenderUpdates.remove_internal(self, sprite)
        self.orderedSprites.remove( sprite )

 
    def add(self, sprite):
        """add(sprite)
           add sprite to group

           Add a sprite or sequence of sprites to a group."""
        if sprite==[]: return
        if not hasattr(sprite, 'depth'):
            sprite.depth = 0
        
        has = self.spritedict.has_key
        if hasattr(sprite, '_spritegroup'):
            for nsprite in sprite.sprites():
                if not has(sprite):
                    nsprite.depth += sprite.depth
                    self.add_internal( nsprite )
                    nsprite.add_internal(self)
        else:
            try: len(sprite) #see if its a sequence
            except (TypeError, AttributeError):
                if not has(sprite):
                    self.add_internal( sprite )
                    sprite.add_internal(self)
            else:
                for sprite in sprite:
                    if not has(sprite):
                        self.add_internal( sprite )
                        sprite.add_internal(self)

    def add_top(self, sprite):
        """add_top(sprite)
           add sprite to group

           Add a sprite to a group above the highest z-axis level."""
        topsprite = self.orderedSprites[len(self.orderedSprites)-1]
        z = topsprite.depth +1
        
        has = self.spritedict.has_key
        if hasattr(sprite, '_spritegroup'):
            for tsprite in sprite.sprites():
                if not has(sprite):
                    tsprite.depth = z + tsprite.depth
        else:
            sprite.depth = z
    
        self.add( sprite )


    def draw(self, surface):
        """draw(surface)
           draw all sprites onto the surface

           Draws all the sprites onto the given surface. It
           returns a list of rectangles, which should be passed
           to pygame.display.update()"""

        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        dirty_append = dirty.append
        self.lostsprites = []
        
        
        for s in self.orderedSprites:
            #s = self.orderedSprites[i]
            r = spritedict[s]
            newrect = surface_blit(s.image, s.rect)
            if r is 0:
                dirty_append(newrect)
            else:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
                    dirty_append(r)
            spritedict[s] = newrect
        return dirty

    def update(self, *args):
        """update(...)
           call update for all member sprites

           calls the update method for all sprites in the group.
           passes all arguments are to the Sprite update function.
           if a sprites' depth changes during its update(), the
           orderedSprites list is re sorted"""
        
        zBefore = 0
        dirty = 0
        if args:
            a=apply
            for s in self.spritedict.keys():
                zBefore = s.depth
                a(s.update, args)
                if zBefore != s.depth:
                    dirty = 1
        else:
            for s in self.spritedict.keys():
                zBefore = s.depth
                s.update()
                if zBefore != s.depth:
                    dirty = 1
        if dirty:
            fn = lambda x,y: x.depth-y.depth
            self.orderedSprites.sort( fn )
            
    
    
