

import pygame
#import string


import prefs
import gfx

smiles_dict = {}
smiles_dict[":0"]  = "face-aah.png"
smiles_dict[";)"]  = "face-blink.png"
smiles_dict["B)"]  = "face-cool.png"
smiles_dict[":')"] = "face-crying.png"
smiles_dict[":$"]  = "face-dollar.png"
smiles_dict[":S"]  = "face-dollar.png"
smiles_dict[":|"]  = "face-hmm.png"
smiles_dict[":O"]  = "face-hysteric.png"
smiles_dict[":D"]  = "face-laugh.png"
smiles_dict[":("]  = "face-sad.png"
smiles_dict["0:)"]  = "face-saint.png"
smiles_dict[":)"]  = "face-smile.png"
smiles_dict["=)"]  = "face-smile2.png"
smiles_dict[":P"]  = "face-tongue.png"
smiles_dict[":\\"]  = "face-undecided.png"

smiles_dict["\\bolo"]  = "happy_birthday_tig.png"
smiles_dict["\\ideia"] = "ideia.png"
smiles_dict["\\tux"]  = "tux.png"
smiles_dict["\\pinguim"]  = "tux.png"
smiles_dict["\\amor"] = "amor.png"
smiles_dict["\\bomba"]  = "bomba.png"
smiles_dict["\\fruta"]  = "apple.png"
smiles_dict["\\casa"]  = "casa.png"
smiles_dict["\\flor"]  = "flor.png"
smiles_dict["\\cobra"]  = "cobra.png"
smiles_dict["\\chaves"]  = "chaves.png"
smiles_dict["\\livro"]  = "livro.png"
smiles_dict["\\chapeu"]  = "chapeu.png"
smiles_dict["\\aranha"]  = "aranha.png"




smiles_images = {}
images_loaded = 0


def loadSmiles():
    global smiles_images, images_loaded
    
    path = prefs.config.get("paths","smiles")
    for key in smiles_dict.keys():
        value = smiles_dict[key]
        smiles_images[key] = gfx.loadImage(value,path)
        

    images_loaded = 1

class Smile:

    def __init__(self, smile):
        self.smile_index = smile

    def getImage(self):
        global smiles_images, images_loaded
        
        if not images_loaded:
            loadSmiles()
        
        return smiles_images[self.smile_index]

        
def __getSlicedList(text):
    global smiles_dict

    smiles = smiles_dict.keys()
    path = prefs.config.get("paths","smiles")

    list = [(0,len(text))]
    
    for option in smiles:
        i = 0
        while i < len(list):
            
            if not isinstance( list[i] , Smile):
                s,e = list[i]
                pos = text[s:e].find(option)
                
                if not pos == -1:
                    pos +=s
                    
                    if not pos == s:
                        list[i] = (s,pos)
                        list.insert(i+1,Smile(option))
                        k = i+2
                    else:
                        list[i] = Smile(option)
                        k = i+1
                    
                    if not pos+len(option)==e:
                        list.insert(k, (pos+len(option), e))
                
            i +=1


    return list
    
    
    
    
def size(text,font):
    

    list = __getSlicedList(text)
    
    sizex = 0
    sizey = font.get_linesize()
    for item in list:
        if isinstance(item, Smile):
            image = item.getImage()
            w, h = image.get_size()
            sizex += w
            sizey = max(sizey,h)
        else:
            s,e = item
            fsize = font.size(text[s:e])
            sizex += fsize[0]
            
    return (sizex, sizey)
     
     
     
def render(text,font, rgb):

    w,h  = size(text,font)
    
    ck = (128,128,128)
    surf = pygame.Surface( (w,h) )
    surf.fill(ck)
    surf.set_colorkey(ck)
    
    ls = font.get_linesize()
    
    font_dy = int( (h-ls)/2 )
    
    
    list = __getSlicedList(text)
    
    posx = 0
    for item in list:
        if isinstance(item, Smile):
            image = item.getImage()
            w0, h0 = image.get_size()
            
            dy = int( (h-h0)/2 )
            surf.blit(image, (posx,dy) )
            posx += w0
        else:
            s,e = item
            fimage = font.render( text[s:e], 1, rgb).convert_alpha(surf)
            
            surf.blit(fimage, (posx,font_dy) )
            
            posx += fimage.get_size()[0]
            
     
    return surf
