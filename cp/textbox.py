import pygame
from pygame.locals import *

import widgets
from events import *

class TextBoxSprite(widgets.Widget):

    #----------------------------------------------------------------------
    def __init__(self, evManager, width):
        widgets.Widget.__init__(self, evManager)

        self.unicode_keypress = 1    #keypress will be send as a unicode char
        self.size = 30
        self.font = pygame.font.Font(None, self.size)
        self.linesize = self.font.get_linesize()

        self._render_as_password = 0
        self.width = width
        
        self.rect = pygame.Rect( (0,0,self.width, self.linesize +4) )
        
        self.text = u''
        self.textPos = (22, 2)
        self.pos_cursor = 0    
        
        self.max_chars = -1
        
        self.bgcolor = color
        self.__curson_ticks = 0
        self.__cursor_on = 1
        
                
        self.isFocusable = 1    #the widget can receive focus

        # self.dead_keys = {u"~":{"a":unicode(chr(227),"utf-8"), 
        #                         "o":unicode(chr(245),"utf-8"), 
        #                         "n":unicode(chr(241),"utf-8") 
        #                         },
        #                   unicode(chr(180),"utf-8"): {"a":unicode(chr(225),"utf-8"), 
        #                          "e":unicode(chr(233),"utf-8"), 
        #                          "i":unicode(chr(237),"utf-8"), 
        #                          "o":unicode(chr(243),"utf-8"), 
        #                          "u":unicode(chr(250),"utf-8"), 
        #                          "c":unicode("c","utf-8")
        #                         },
        #                   u"`": {"a":unicode(chr(224),"utf-8"), 
        #                         "o":unicode(chr(242),"utf-8"), 
        #                         "e":unicode(chr(232),"utf-8"), 
        #                         "i":unicode(chr(236),"utf-8"), 
        #                         "u":unicode(chr(249),"utf-8")
        #                         },
        #                   u"^": {"a":unicode(chr(226),"utf-8"), 
        #                         "e":unicode(chr(234),"utf-8"), 
        #                         "i":unicode(chr(238),"utf-8"), 
        #                         "o":unicode(chr(244),"utf-8")
        #                         }
        #                     }
        
        self.last_key = ""

    #----------------------------------------------------------------------
    def setFont(self, fontfile, size=30):
        self.font = pygame.font.Font(fontfile, size)        
        try:
            self.font = pygame.font.Font(fontfile, size)
        except:
            self.font = pygame.font.Font(None, size)
            raise Exception("Cannot load the font file")


        self.size = size
        self.linesize = self.font.get_linesize()
        x,y = self.rect.topleft
        self.rect = pygame.Rect( (x,y,self.width, self.linesize +4) )
        
        self.__blit_posx = 0
        
        self.drawBox()

    #----------------------------------------------------------------------
    def setPassword(self):
        self._render_as_password = 1


    #----------------------------------------------------------------------
    def setText(self, newText):
        self.text = newText
        self.dirty = 1


    #----------------------------------------------------------------------
    def drawBox(self):
        colorkey = (124,244,22)
    
        boxImg = pygame.Surface( self.rect.size )
        boxImg.set_colorkey(colorkey)
        boxImg.fill( colorkey )
        
        color = (0,0,100)
        rect = pygame.Rect( 0, 0, self.rect.w, self.rect.h)
        
        self.emptyImg = boxImg
        self.image = boxImg
        
        
        
        

    #----------------------------------------------------------------------
    def insertText(self, text):
        if self.max_chars > 0:
            if len(self.text) >= self.max_chars:
                return 1
    
        text_2_cursor = self.text[0:self.pos_cursor]
        text_a_cursor = self.text[self.pos_cursor:len(self.text)]
        
        newText = text_2_cursor + text + text_a_cursor
        self.pos_cursor  += len(text)
        self.setText(newText)        

    
    #----------------------------------------------------------------------
    def update(self):
        if not self.dirty:
            return
        
        self.drawBox()

        if self._render_as_password:
            text = "*" * len(self.text)
        else:
            text = self.text


        
        text_2_cursor = text[0:self.pos_cursor]
        text_a_cursor = text[self.pos_cursor:len(text)]
        
        if self.focused:
            text = text_2_cursor + text_a_cursor

        textColor = (255,0,0)
        textImg = self.font.render( text.encode("utf-8"), True, textColor )
        w2, h =  self.font.size( text_2_cursor.encode("utf-8") )
        w = w2+5
        
        
        #dx = textImg.get_rect().width - self.image.get_rect().width
        #dx1 = w - self.image.get_rect().width
        
        min = self.__blit_posx
        max = self.__blit_posx + self.image.get_rect().width

        #temp = self.__blit_posx - dx
        dx = 0
        if w < min:
            dx -= (min-w)
        elif w >max:
            dx += (w-max)
        
            
        self.__blit_posx += dx
        
        self.image.blit( self.emptyImg, (0,0) )
        
        if self.focused and self.__cursor_on:
            color = (0,0,0)
            posy = -self.font.get_descent()
            
            rect = pygame.Rect( w2-self.__blit_posx, posy, 1, self.linesize - posy  )
            
            pygame.draw.rect( self.image, color, rect, 0 )
        
        
        self.image.blit( textImg, (-self.__blit_posx, 0) )

        self.dirty = 1
        
        


    #----------------------------------------------------------------------
    def onClick(self, pos):
        self.evManager.Post(GUIFocusThisWidgetEvent(self))


       
    #----------------------------------------------------------------------        
    def M_keypress(self, okey, modifier):
        
        key, keycode = okey
        
        if keycode==K_BACKSPACE:
            self.pos_cursor -= 1
            if self.pos_cursor < 0:
                self.pos_cursor = 0
            else:
                newText = self.text[0:self.pos_cursor]+self.text[self.pos_cursor+1:len(self.text)]
                self.setText( newText )
        elif keycode==K_DELETE:
            if self.pos_cursor:
                newText = self.text[0:self.pos_cursor]+self.text[self.pos_cursor+1:len(self.text)]
                
                if self.pos_cursor > len(self.text):
                    self.pos_cursor = len(self.text)
                self.setText( newText )                    
        elif keycode==K_LEFT:
            self.pos_cursor -= 1
            if self.pos_cursor < 0:
                self.pos_cursor = 0
            self.dirty = 1
        elif keycode==K_RIGHT:
            self.pos_cursor += 1
            tam = len(self.text)
            if self.pos_cursor > tam:
                self.pos_cursor = tam
            self.dirty = 1
        else:
            if not key:
                return 0
            # if self.last_key:
            #     temp = self.dead_keys[self.last_key]
            #     if temp.has_key(key):
            #         key = temp[key]
            #         
            #     self.last_key = ""
            # elif self.dead_keys.has_key(key):
            #     self.last_key = key
            #     return 1
                    
                
            if modifier>0 and key>=97 and key<122:
                if modifier & KMOD_SHIFT \
                or modifier & KMOD_CAPS:
                    key = string.upper(key)
                    
            self.insertText(key)
            
        self.onKeypress(okey,modifier)


    def Notify(self, event):
        widgets.Widget.Notify(self, event)
        
        if event==TickEvent:
            self.__curson_ticks +=1
            if self.__curson_ticks>5:
                self.__curson_ticks =0 
                if self.__cursor_on:
                    self.__cursor_on = 0
                else:
                    self.__cursor_on = 1
    
#----------------------------------------------------------------------



