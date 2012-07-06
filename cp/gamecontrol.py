

from events import *
import pygame
from pygame.locals import *

import prefs
import groups


class CPgameControl:


    def __init__(self, evManager):

        self.evManager = evManager


        #inicializa the interface
        pygame.init()
        pygame.font.init()


        self.screen = pygame.display.set_mode((800, 600),DOUBLEBUF)
        pygame.display.set_caption('Cooperativa do Conhecimento')
        
        if prefs.config.get("display","full_screen")=="yes":
            pygame.display.toggle_fullscreen()


        #says to the event controller that I want to listen only the One Second event
        self.evManager.RegisterListener( self , [Event]) 
        
        self.spriteGroup = groups.layeredGroup()
        self.subcontrollers = []
        

    def DialogAdd(self, dialog):
        #print "Adding Dialog Controllers", key

        self.subcontrollers.insert(0, dialog)
        self.spriteGroup.add_top(dialog)


    def DialogRemove(self, dialog):

        self.subcontrollers.pop(0)
        self.spriteGroup.remove(dialog)
        
    def switchController(self, key):

        if not self.guiClasses.has_key( key ):
            raise NotImplementedError
        
        self.subcontrollers = []
        self.spriteGroup.empty()
        
        for contClass in self.guiClasses[key]:
            newController = contClass( self.evManager )
            self.subcontrollers.append( newController )
            self.spriteGroup.add( newController )
            
        self.screen.fill( self.subcontrollers[0].background_color )

    def update(self):
            
        self.subcontrollers[0].update()
        #self.spriteGroup.update()
        dirtyRects = self.spriteGroup.draw( self.screen )
        pygame.display.update( dirtyRects )
        pygame.display.flip()


            
    def Notify(self, event):

        if event == TickEvent:
            
            #Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.evManager.Post( QuitEvent() )


                elif event.type == KEYDOWN \
                  or event.type == MOUSEBUTTONUP \
                  or event.type == MOUSEBUTTONDOWN \
                  or event.type == MOUSEMOTION:
                    for cont in self.subcontrollers:
                        if cont.wantsEvent( event ):
                            cont.HandlePyGameEvent(event)
                            break


            # update the screen
            self.update()
        
        elif event == GUIDialogAddRequest:
            self.DialogAdd( event.gui )

        elif event == GUIDialogRemoveRequest:
            self.DialogRemove( event.gui )




