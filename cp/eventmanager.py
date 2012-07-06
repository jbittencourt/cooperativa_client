# This code was almost a copy from the one in the site http://sjbrown.ezide.com/writing-games.html
import threading

from weakref import WeakKeyDictionary
from copy import copy

from events import *






class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""
    def __init__(self, initlist=None ):
        self.listeners = WeakKeyDictionary()
        self.eventQueue = []
     
        self.__lock = threading.Lock()


    #----------------------------------------------------------------------
    def RegisterListener( self, listener , eventList):
        #if not hasattr( listener, "Notify" ): raise blah blah...
        self.listeners[ listener ] = eventList
    
    def addListener(self, listener, eventList):
    
        if self.listeners.has_key( listener ):
            self.listeners[ listener ].append( eventList )
        else:
            self.listeners[ listener ] = eventList

    #----------------------------------------------------------------------
    def UnregisterListener( self, listener ):
        if listener in self.listeners.keys():
            del self.listeners[ listener ]
        
    #----------------------------------------------------------------------
    def Post( self, event ):

        if event==OneSecondEvent:
            self.sendEvent( event )
                
        if not event==TickEvent: 
            self.__lock.acquire()
            self.eventQueue.append( event )
            self.__lock.release()
        else:
            self.flushEvents()

            #at the end, notify listeners of the Tick event
            for listener in self.listeners.keys():
                listener.Notify( event )
        
        
    def flushEvents(self):
        if self.eventQueue:
            for k in range(len(self.eventQueue)):
                ev = self.eventQueue.pop(0)
                self.sendEvent(ev)
                
    def sendEvent(self, ev):
        for listener in self.listeners.keys():
            throwable_events = self.listeners[listener]
            if ev in throwable_events:
                listener.Notify( ev )
    
