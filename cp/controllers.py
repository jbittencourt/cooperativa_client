import pygame

from events import *



class CPUSpinnerController:
    """..."""
    def __init__(self, evManager):
        global coop_fps
    
        self.evManager = evManager
        self.evManager.RegisterListener( self , [QuitEvent,OneSecondEvent,syncServerEvent] )

        self.keepGoing = 1
        self.fps = 15    #frames per second
        self.__onesecond = 0
        self.__syncronized = 0

    #----------------------------------------------------------------------
    def Run(self):
        self.clock = pygame.time.Clock()
        ticks = 0
        if not self.keepGoing:
            raise Exception('dead spinner')
            
        while self.keepGoing:
            event = TickEvent()
            self.evManager.Post( event )

            self.clock.tick(self.fps)
            if ticks >= self.fps and self.__syncronized:
                while( not self.__onesecond ):
                    pass
                self.__onesecond = 0
                ticks = 0
            else:
                ticks +=1

    #----------------------------------------------------------------------
    def Notify(self, event):
        if event==QuitEvent:
            #this will stop the while loop from running
            self.keepGoing = 0
        elif event==OneSecondEvent:
            self.__onesecond = 1
        elif event==syncServerEvent:
            self.__syncronized = 1
            
            
