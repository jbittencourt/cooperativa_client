from events import *
import pygame
from pygame.locals import *

import prefs


class soundControl:


    def __init__(self, evManager):

        self.evManager = evManager
        self.evManager.RegisterListener( self , [soundEvent])
        
        #initialize sound
        pygame.mixer.pre_init()
        
        self.disable = 0
        
        try:
            pygame.mixer.init()
        except:
            print "Can't open sound device. Disable sound support"
            self.disable = 1
        
        self.sounds = {}
        self.music = None
        
    
    def Notify(self, event):

        if self.disable:
            return 0
    
        if event == loadMusicEvent:
            pathmusic = prefs.config.get("paths","music")
            file = pathmusic+"/"+event.filename
            self.music = file
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)
        elif event == stopMusicEvent:
            pygame.mixer.music.stop()
    
        elif event == changeMusicEvent:
            pathmusic = prefs.config.get("paths","music")
            file = pathsounds+"/"+event.filename
            self.music = file
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)
        
        elif event == restoreMusicEvent:
            if self.music:
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play(-1)
    
        elif event == loadSoundEvent:
            pathsounds = prefs.config.get("paths","sound")
            file = pathsounds+"/"+event.filename
            self.sounds[event.name] = pygame.mixer.Sound(file)
        
        elif event == unloadSoundEvent:
            if self.sounds.has_key(event.name):
                del(self.sounds[event.name])
            else:
                print "Warning: Sound name doesn't exists."
        
        elif event == playSoundEvent:
            if self.sounds.has_key(event.name):
                self.sounds[event.name].play()
            else:
                print "Warning: Sound name doesn't exists."
