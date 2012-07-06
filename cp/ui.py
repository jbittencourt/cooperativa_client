import pygame
from pygame.locals import *

from events import *
import groups

class CPui(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.wants_event = 1
        self.absolute_mouse_click = 0
        
        self.unicode_keypress = 0
        
        self.mouse_over = 0

    def onKeypress(self, key, modifier):
        pass

    def onClick(self, pos):
        pass

    def onMouseOver(self, pos):
        pass   
    
    def onMouseOut(self, pos):
        pass   

    #when a pygame event occurs one method is called tha is M_eventtype. This method is mandatory
    #and is responsable to class the user thedos
    def M_keypress(self, key, modifier):
        self.onKeypress( key, modifier )

    def M_click(self, pos):
        self.onClick(pos)

    def M_mouseover(self, pos):
        self.onMouseOver(pos)

    def M_mouseout(self, pos):
        self.onMouseOver(pos)

class CPgui(groups.layeredGroup):
    
    def __init__( self , evManager ):
        groups.layeredGroup.__init__(self)
        
        self.evManager = evManager
        self.evManager.RegisterListener( self , [TickEvent,GUIWidgetEvent])        
        
        self.wants_event = 1
        
        self.background_color = (0,0,0)
        
        self.dialogs = {}

    def wantsEvent(self, event):
        return self.wants_event

    def HandlePyGameEvent(self, event):
        import widgets
                
        if event.type == KEYDOWN:

            if event.key==K_TAB:
                if event.mod & KMOD_CTRL:
                    self.changeFocusedWidget(-1)
                else:
                    self.changeFocusedWidget(1)

                return 1

            key = event.key
            char = event.unicode
            mod = event.mod
            for sprite in self.sprites():

                if not isinstance(sprite,widgets.Widget):
                    continue
            
                send_event = sprite.getFocus()

                if send_event:
                    if sprite.unicode_keypress:
                        sprite.M_keypress((char,key), mod) 
                    else:
                        sprite.M_keypress(key, mod) 
            
        #when de mouse button is pressed
        #test if the click is in the ui area, and relativise the position
        #to the widget position
        elif event.type ==  MOUSEBUTTONDOWN:
            for sprite in self.sprites():
                if sprite.rect.collidepoint(event.pos):
                    if sprite.absolute_mouse_click:    
                        sprite.M_click(event.pos)
                    else:
                        x0, y0 = event.pos
                        x1, y1 = sprite.rect.topleft
                        sprite.M_click( ( x0-x1, y0-y1 ) )
        
        elif event.type == MOUSEMOTION:
            for sprite in self.sprites():
                
                if sprite.rect.collidepoint(event.pos):
                    if not sprite.mouse_over:
                        sprite.M_mouseover(event.pos)
                        sprite.mouse_over = 1
                else:
                    if sprite.mouse_over:
                        sprite.M_mouseout(event.pos)
                        sprite.mouse_over = 0
                    

    def changeFocusedWidget(self, offset):
        import widgets
        
        #map the widgets
        widgets = filter(lambda x: isinstance(x,widgets.Widget) and x.isFocusable  , self.sprites())
        fn = lambda x,y: x.tabOrder - y.tabOrder
        widgets.sort(fn)
        
        
        if widgets:
            focused = -1
            cont = 0
            for w in widgets:
                if w.focused:
                    focused = cont
                cont += 1
            
            if focused < 0:
                focused = 0
            
            widgets[focused].setFocus(0)
            print focused

            tofocus = focused + offset
            if tofocus >= len(widgets):
                tofocus = 0
            elif tofocus < 0:
                tofocus = len(widgets)-1

            widgets[tofocus].setFocus(1)
        


    def Notify(self, event):

        if event == GUIFocusNextWidgetEvent:
            self.ChangeFocusedWidget(1)

        elif event == GUIFocusPrevWidgetEvent:
            self.ChangeFocusedWidget(-1)

    
