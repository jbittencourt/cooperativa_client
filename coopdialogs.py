
import dialogs
import button
import gfx
import prefs
import ui
import widgets
import objactions

from events import *

class okButton(button.buttonImageSprite):
    
    def __init__(self, evManager, dialog):
                
        images = gfx.loadImageSlices("btn_ok.png", (0,0,40,40),2)
        
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])
        
        self.dialog = dialog

    def onClick(self, pos):
        self.dialog.ok()
        

class cancelButton(button.buttonImageSprite):
    
    def __init__(self, evManager, dialog):
        images = gfx.loadImageSlices("btn_cancel.png", (0,0,40,40),2)
        button.buttonImageSprite.__init__(self, evManager, images[0])
        self.addState(self.state_over, images[1])        
        
        self.dialog = dialog

    def onClick(self,pos):
        self.dialog.cancel()
        

class genericImage(ui.CPui):

    def __init__(self,image):
        ui.CPui.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        
class background(ui.CPui):

    def __init__(self):
         ui.CPui.__init__(self)
         
         self.image = gfx.loadImage("dialog.png")
         self.rect = self.image.get_rect()
    
    def onClick(self, pos):
        print pos

class COOPdialog(dialogs.Dialog):

    def __init__(self, evManager):
        dialogs.Dialog.__init__(self, evManager)
        
                
        back = background()
        self.setBackground(back)
        
        self.setPos((175,125))
    
    
class COOPokDialog(COOPdialog):

    def __init__(self, evManager, text):
        COOPdialog.__init__(self, evManager)
        
        self.text = text
        
        self.okb = okButton(evManager, self)
        self.okb.rect.topleft = (190,280)
        self.okb.depth = 1
        self.add(self.okb)
        
        #draw text
        font = prefs.config.get("fonts","dialog_font")
        size = int(prefs.config.get("fonts_size","dialog_font_size"))
        label = widgets.LabelSprite(self.evManager, self.text)
        label.setFont(font, size)
        label.depth = 2
        label.color = (244,28,29)
        
        label.rect.top = 40
        label.rect.centerx = 222
        label.align = "center"
        self.add(label)
        
    def ok(self):
        pass
        

        
class COOPok_cancelDialog(COOPokDialog):

    def __init__(self, evManager, text):
        COOPokDialog.__init__(self, evManager, text)
        
        
        self.okb.rect.topleft = (130,280)
        self.adjustPos(self.okb)
        
        self.cancelb = cancelButton(evManager, self)
        self.cancelb.rect.topleft = (260,280)
        self.cancelb.depth = 3
        self.add(self.cancelb)
    
    def cancel(self):
        pass
        
class COOPmessageDialog(COOPokDialog):

    def __init__(self, evManager, text):
        COOPokDialog.__init__(self, evManager, text)
    
    def ok(self):
        self.evManager.Post( GUIDialogRemoveRequest( self ) )

        


class COOPinventoryDialog(COOPdialog):

    def __init__(self, evManager, obj, supressStoreEvent=0):
        COOPdialog.__init__(self, evManager)
    
        self.img = genericImage( obj.getInventoryImage() )
        self.img.rect.topleft = (187,50)
        self.img.depth = 1
        self.add(self.img)
        
        #draw text
        font = prefs.config.get("fonts","dialog_font")
        size = int(prefs.config.get("fonts_size","dialog_font_size"))
        label = widgets.LabelSprite(self.evManager, obj.human_name )
        label.setFont(font, size)
        label.depth = 2
        label.color = (244,28,29)
        
        label.rect.top = 170
        label.rect.centerx = 222
        label.align = "center"
        self.add(label)
        
        posx = 20
        posy = 280
        depth = 3
        
        
        for action in obj.possible_actions:
            if supressStoreEvent and action==objactions.storeAction:
                continue
        
            oaction = action( evManager, self, obj )
            print posx, posy
            oaction.rect.topleft = (posx, posy)
            oaction.depth = depth
            depth +=1
            posx += oaction.rect.width +10
            self.add(oaction)

    
