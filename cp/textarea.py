import pygame
from pygame.locals import *

import widgets
import textwrap
from events import *
import textbox


class TextAreaSprite(textbox.TextBoxSprite):

    def __init__(self, evManager, cols, rows ):
        textbox.TextBoxSprite.__init__(self, evManager, cols)
        
        self.cols = cols
        self.rows = rows
        
        self.background_color = (0,0,0)
        
        self.__cursor_on = 1
        
                
    def setFont(self, fontfile, size=30):
        self.font = pygame.font.Font(fontfile, size)        
        try:
            self.font = pygame.font.Font(fontfile, size)
        except:
            self.font = pygame.font.Font(None, size)
            raise Exception("Cannot load the font file")


        self.size = size
        size = self.font.size("A"*self.cols)[0]
        self.linesize = self.font.get_linesize()
        x,y = self.rect.topleft
        self.rect = pygame.Rect( (x,y,size, self.linesize*self.rows +4) )                
                
    
    def clear(self):
        self.text = ""
        self.pos_cursor = 0
    
    
    def update(self):
        if not self.dirty:
            return


        text = self.text
        
        text_2_cursor = text[0:self.pos_cursor]
        text_a_cursor = text[self.pos_cursor:len(text)]
        
        if self.focused:
            text = text_2_cursor  + text_a_cursor
            
        lines = textwrap.wrap(text, self.cols)

        textColor = (255,0,0)
        
        x,y,w,h = self.rect
        self.image = pygame.Surface( (w, h) )
        self.image.fill( (255,255,128) )
        self.image.set_colorkey( (255,255,128) )
                
        cursor_relative_pos = 0    
        cursor_line = 0
        
        pos_y = 0
        ac = 0
        textColor = (255,0,0)
        count = 0
        offset = self.linesize - self.font.get_ascent()/2
        for line in lines:
            tempImg = self.font.render( line.encode("latin-1"), 1, textColor )
            self.image.blit( tempImg, (0, pos_y) )
            pos_y +=  offset
            ll = len(line)
            
            #discover the cursor line
            if self.pos_cursor>ac and self.pos_cursor<= ac+ll+1:
                cursor_line = count
                cursor_relative_pos = self.pos_cursor - ac
                
            ac += ll
            count +=1
            
        if self.focused and self.__cursor_on:
            color = (0,0,0)
            posy = -self.font.get_descent()
            w,h = self.font.size(lines[cursor_line][0:cursor_relative_pos])
            rect = pygame.Rect( w, (cursor_line * offset)+posy, 1, self.linesize - posy  )
            
            pygame.draw.rect( self.image, color, rect, 0 )
        
        
        self.dirty = 1

