'''
Created on Mar 01, 2013

@author: hifly
'''

import os
import math
import urllib2
import logging
import logging.config
import twitterUtil
import photoOrganizerStorage
import photoOrganizerUtil
from gi.repository import Gtk,GdkPixbuf,Gdk,GObject
from PIL import Image
from twitterUtil import TwitterSearchResult
from photoOrganizerStorage import PhotoOrganizerPref
from photoOrganizerUtil import AlbumCollection
from photoOrganizerUtil import Album
from photoOrganizerUtil import PhotoFile

#logging conf
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger('photoOrganizer')

#Initializing the gtk's thread engine
GObject.threads_init()

#const
GLADE_CONF = "glade/photoOrganizerGui.glade"

UI_INFO = """
<ui>
  <popup name='PopupMenu'>
    <menuitem action='EditOriginalSize' />
    <menuitem action='EditFlip' />
    <menuitem action='EditRotate' />
    <menuitem action='EditSave' />
  </popup>
</ui>
"""

class PhotoOrganizerGUI(Gtk.Window):
    
    def __init__(self):
        #references
        self.imagePathOpened = None
        self.imageMap = {}
        self.thubnailPanel = {}
        self.twitterCurrentQuery = None
        self.currenWinImage = None
        self.entry_folder_text = None
        
        #build GUI from glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_CONF)
        handlers = {
                    "on_PhotoOrganizer_delete_event": self.on_PhotoOrganizer_delete_event,
                    "on_PhotoOrganizer_search_event": self.on_PhotoOrganizer_search_event,
                    "on_PhotoOrganizer_twitter_search_event": self.on_PhotoOrganizer_twitter_search_event,

        }
        #handler of GUI signals
        self.builder.connect_signals(handlers)
        
        #show main window
        self.window = self.builder.get_object("PhotoOrganizer")
        self.window.connect("key_press_event",self.on_PhotoOrganizer_image_keypress_event)
        self.window.show_all()
        
        #load pref
        self.loadPreferences()
        
        #main gtk
        Gtk.main()
   
    def loadPreferences(self):
        #load preferences
        photoOrganizerPref = photoOrganizerStorage.loadPref()
        if(photoOrganizerPref!=None):
            try:
                self.hiddenFolders = photoOrganizerPref.hiddenFolders
                self.entry_folder_text = photoOrganizerPref.lastSearch
                self.createTwitterPhotoTree(photoOrganizerPref.albumCollection)
                leftPanel = self.builder.get_object("leftPanel")
                leftPanel.add(self.treeview)
                leftPanel.show_all()
                self.twitterSearch = False
            #some pref properties stored could be not present --> no previous search available
            except:
                pass
            
    def on_PhotoOrganizer_delete_event  (self, *args):
        if(self.lastAlbumCollectionScanned is not None):
            #save the preferences
            photoFile = PhotoOrganizerPref(self.hiddenFolders,self.entry_folder_text,self.lastAlbumCollectionScanned)
        photoOrganizerStorage.savePref(photoFile)
        Gtk.main_quit()
    
    def on_PhotoOrganizer_search_event  (self, *args):
        #set no twitter search
        self.twitterSearch = False
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            #get directory selected
            self.searchEntry = dialog.get_filename()
            self.removeSearchResult();
            
            # You'll need to import gobject
            GObject.timeout_add(100, self.callScanPhoto)
            dialog.destroy()

    
    def on_PhotoOrganizer_twitter_search_event(self,widget,event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "Return":
            self.twitterSearch = True
            self.removeSearchResult();    
            queryToSend = self.builder.get_object("twitterSearchField").get_text()
            numberOfTweets = self.builder.get_object("twitterSpin").get_value_as_int()
            try:
                self.twitterSearchResult = twitterUtil.searchMediaTweets(queryToSend,numberOfTweets) 
                if(self.twitterSearchResult is not None and len(self.twitterSearchResult.entries)>0):
                    #create album collection
                    albumCollection = AlbumCollection()
                    album = Album()
                    album.title = queryToSend
                    for entry in self.twitterSearchResult.entries:
                        photoFile = PhotoFile() 
                        photoFile.mediaUrl = entry.url;
                        photoFile.dirName = entry.url
                        photoFile.fileName = entry.url
                        photoFile.shortName = entry.url
                        photoFile.author = entry.author
                        album.pics.append(photoFile)
                    albumCollection.albums.append(album) 
                    album.totalPics = len(album.pics)
                    albumCollection.totalPics = len(album.pics)
            
                    self.twitterCurrentQuery = queryToSend
                    self.createTwitterPhotoTree(albumCollection)
            
                    leftPanel = self.builder.get_object("leftPanel")
                    leftPanel.add(self.treeview)
                    leftPanel.show_all()
                else:
                    self.on_PhotoOrganizer_search_error_event()    
            except Exception as e:
                self.on_PhotoOrganizer_generic_error_event(e)
    
    def on_PhotoOrganizer_generic_error_event  (self,e):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,Gtk.ButtonsType.CANCEL,e)
        dialog.run()
        dialog.destroy()
        
    def on_PhotoOrganizer_search_error_event  (self, *args):
        extraTextDialog = None
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, "No pics founded")
        if(self.twitterSearch):
            extraTextDialog = "Specify another twitter search!"
        else:
            extraTextDialog = "Specify another folder!"    
        dialog.format_secondary_text(extraTextDialog)
        dialog.run()
        dialog.destroy()
    
    def on_PhotoOrganizer_image_contextmenu_event(self, widget, event) :
        uimanager = self.create_image_context_menu()
        self.popup = uimanager.get_widget("/PopupMenu")
        #check if right mouse button was preseed
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.popup.popup(None, None, None, None, event.button, event.time)
            return True  
        
    #event selection of a tree entry    
    def on_PhotoOrganizer_tree_entry_selected(self, widget, data = None):
        selection = self.treeview.get_selection()
        if selection is not None:
            tree_model, tree_iter = selection.get_selected()
            imagePath = tree_model.get_value(tree_iter, 0)
        
            if(self.twitterSearch):
                if(imagePath == self.twitterCurrentQuery):
                    self.createThubnailPanel(imagePath)
                else:
                    self.createScaledImage(imagePath)
            else:
                if os.path.isfile(imagePath):
                    self.createScaledImage(imagePath)
                else:
                    self.createThubnailPanel(imagePath) 
    
    def on_PhotoOrganizer_thub_clicked(self, widget,event,imagePath):
        self.createScaledImage(imagePath)
    
    def on_PhotoOrganizer_original_size_clicked(self, widget):
        if os.path.isfile(self.imagePathOpened):
            pimage = Gtk.Image()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.imagePathOpened)
            pimage.set_from_pixbuf(pixbuf)
            self.on_PhotoOrganizer_full_image_clicked(pimage,self.imagePathOpened)  
                    
    def on_PhotoOrganizer_rotate_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        scaled_buf = pixbuf.rotate_simple(90)
        self.imageOpened.set_from_pixbuf(scaled_buf)
    
    def on_PhotoOrganizer_flip_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        scaled_buf = pixbuf.flip(30)
        self.imageOpened.set_from_pixbuf(scaled_buf) 

    def on_PhotoOrganizer_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Save your image", self,Gtk.FileChooserAction.SAVE,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_default_size(800, 400)
     
        Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True)
        Gtk.FileChooser.set_current_name(dialog, "Untitled document")

        response = dialog.run()
        
        if response == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()
            dialog.destroy()
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)
            photoOrganizerUtil.savePhotoFromUrl(self.lastTwitterImageUrl,filename)
           
    def on_PhotoOrganizer_image_keypress_event(self,widget,event) :
        newImagePath = None
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "Right":
            newImagePath = self.nextRightImage()
        if newImagePath is not None:
            self.createScaledImage(newImagePath)
        elif keyname == "Left":
          newImagePath = self.nextLeftImage()
          if newImagePath is not None:
              self.createScaledImage(newImagePath)
    
    #create image viewer panel
    def on_PhotoOrganizer_full_image_clicked(self,pimage,imageName):      
        self.winImage = Gtk.Window()
        self.winImage.set_title(imageName)
        self.winImage_vbox = Gtk.VBox(False,1)
        eventBox = Gtk.EventBox()
        eventBox.add(pimage)
        pimage.show()
        self.winImage_vbox.pack_start(eventBox, True, True, 0)
        self.winImage.add(self.winImage_vbox)
        (x, y) = self.get_position()
        y1 = y+50
        self.winImage.move(x, y1)
        self.winImage.show_all() 
    
    def nextRightImage(self):
        currentImageKey = self.imagePathOpened[self.imagePathOpened.rfind("/")+1:]
        previousKeyFounded = None
        for key, value in self.subImageMap.items():
            if previousKeyFounded is not None:
                return self.imagePathOpened[:self.imagePathOpened.rfind("/")+1]+key
            if key == currentImageKey:
                previousKeyFounded = key
    
    def nextLeftImage(self):
        currentImageKey = self.imagePathOpened[self.imagePathOpened.rfind("/")+1:]
        previousKeyFounded = None
        for key, value in self.subImageMap.items():
            if key != currentImageKey:
                previousKeyFounded = key
            if key == currentImageKey and previousKeyFounded is not None:
                return self.imagePathOpened[:self.imagePathOpened.rfind("/")+1]+previousKeyFounded 
    
    def create_image_context_menu(self):
        action_group = Gtk.ActionGroup("my_actions")
        action_group.add_actions([                   
            ("EditOriginalSize", Gtk.STOCK_ZOOM_FIT, "Original size", "<control><alt>O", None,
             self.on_PhotoOrganizer_original_size_clicked),
            ("EditFlip", Gtk.STOCK_OK, "Flip", "<control><alt>P", None,
             self.on_PhotoOrganizer_flip_clicked),
            ("EditRotate", Gtk.STOCK_REFRESH, "Rotate", "<control><alt>R", None,
             self.on_PhotoOrganizer_rotate_clicked),
            ("EditSave", Gtk.STOCK_SAVE, "Save", "<control><alt>S", None,
             self.on_PhotoOrganizer_save_clicked)                                             
        ])
        uimanager = Gtk.UIManager()
        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)
        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        uimanager.insert_action_group(action_group)
        return uimanager
    
    def createScaledImage(self,imagePath): 
        pimage = Gtk.Image()
        
        if(self.twitterSearch):
            self.lastTwitterImageUrl = imagePath
            imagePath = imagePath[imagePath.index('http'):]
            response=urllib2.urlopen(imagePath)
            loader=GdkPixbuf.PixbufLoader()
            loader.write(response.read())
            loader.close() 
            pixbuf = loader.get_pixbuf()
                         
        if os.path.isfile(imagePath):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(imagePath)
            
        # scale the image
        orig_width =  pixbuf.get_width()
        orig_height = pixbuf.get_height()
        if orig_width >= orig_height:
            if orig_width > 400:
                orig_width = 400
            if orig_height > 300:
                orig_height = 300  
        if orig_width < orig_height:
            if orig_width > 300:
                orig_width = 300
            if orig_height > 400:
                orig_height = 400            
        scaled_buf = pixbuf.scale_simple(orig_width,orig_height,GdkPixbuf.InterpType.BILINEAR)
        pimage.set_from_pixbuf(scaled_buf)
        self.imagePathOpened = imagePath
        self.createImagePanel(pimage,imagePath)
        
        if(self.twitterSearch):
            mediaUrl = self.imagePathOpened
            for entry in self.twitterSearchResult.entries:
                try:
                    if(entry.url.index(mediaUrl)!=-1):
                        self.imageOpened.set_tooltip_text("user:"+entry.author+"\ndate:"+entry.creationDate+"\ntext:"+entry.text)
                        self.imageOpened.show_all()
                        self.builder.get_object("detailsEntry").get_buffer().set_text("user:"+entry.author+"\ndate:"+entry.creationDate+"\ntext:"+entry.text)
                except:
                    logger.error("Error in show details..")
        else:
            currentPhoto = self.totalPhotoDictionary[imagePath]
            if currentPhoto.latitude:
                self.builder.get_object("detailsEntry").get_buffer().set_text("photo taken at:\nlatitude:"+str(currentPhoto.latitude)+"\nlongitude:"+str(currentPhoto.longitude))
    
    #create image viewer panel
    def createImagePanel(self,pimage,imageName):    
        imagePanel = self.builder.get_object("imagePanel")
        try:
            imagePanel.remove(imagePanel.get_children()[0])
        except:
            logger.error("skip remove image")
        eventBox = Gtk.EventBox()
        eventBox.add(pimage)
        #reference to image selected
        self.imageOpened = pimage
        eventBox.connect("button_press_event",self.on_PhotoOrganizer_image_contextmenu_event)
        pimage.show()
        imagePanel.add(eventBox)
        imagePanel.show_all()
    
    def createThubnailPanel(self,imagePath):
          imagePanel = self.builder.get_object("imagePanel")
          try:
              imagePanel.remove(imagePanel.get_children()[0])
          except:
              #nothing to do
              pass
          if(imagePath in self.thubnailPanel):
               imagePanel.add(self.thubnailPanel[imagePath])
               imagePanel.show_all()
               while Gtk.events_pending():
                    Gtk.main_iteration_do(False)
          else:          
              self.subImageMap = self.imageMap[imagePath]
              thubnailsSize = len(self.subImageMap.items())
              tempRows = math.ceil(thubnailsSize/10)
              tableRows = int(math.fabs(tempRows))
              if tableRows==0:
                  tableRows=1
              thubnailWindow_table = Gtk.Table(tableRows, 10, True)
              imagePanel.add(thubnailWindow_table)
              left_attach = 0
              right_attach = 1
              top_attach = 0
              bottom_attach = 1
              for key, value in self.subImageMap.items():
                   pimage = Gtk.Image()
                   eventBox = Gtk.EventBox()
                   eventBox.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
                   pixbuf = None
                   if(self.twitterSearch):
                        value.fileName = value.fileName[value.fileName.index('http'):]
                        response=urllib2.urlopen(value.fileName)
                        loader=GdkPixbuf.PixbufLoader()
                        loader.write(response.read())
                        loader.close() 
                        eventBox.connect("button_press_event", self.on_PhotoOrganizer_thub_clicked,value.fileName)
                        pixbuf = loader.get_pixbuf()
                   else:
                       eventBox.connect("button_press_event", self.on_PhotoOrganizer_thub_clicked,imagePath+"/"+value.fileName)
                       pixbuf = GdkPixbuf.Pixbuf.new_from_file(imagePath+"/"+value.fileName)           
                   scaled_buf = pixbuf.scale_simple(50,50,GdkPixbuf.InterpType.BILINEAR)
                   pimage.set_from_pixbuf(scaled_buf)
                   eventBox.add(pimage)
                   thubnailWindow_table.attach(eventBox,left_attach,right_attach,top_attach,bottom_attach)
                   thubnailWindow_table.set_col_spacings(5)
                   if right_attach <10:
                       right_attach+=1
                       left_attach+=1
                   else:
                     left_attach = 0  
                     right_attach = 1  
                     top_attach+=1 
                     bottom_attach+=1   
                   self.thubnailPanel[imagePath] = thubnailWindow_table
                   imagePanel.show_all()
                   while Gtk.events_pending():
                        Gtk.main_iteration_do(False)
    
    def callScanPhoto(self):
        loadWindow = Gtk.Window()
        loadImage = Gtk.Image()
        pixbufanim = GdkPixbuf.PixbufAnimation.new_from_file("images/load.gif")
        loadImage.set_from_animation(pixbufanim)
        loadWindow.add(loadImage)  
        loadWindow.show_all()
        
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        
        #get status_bar
        statusBar = self.builder.get_object("statusbar1")
        context = statusBar.get_context_id("example")        
        # create the treestore; the model has one column of type string
        treestore = Gtk.TreeStore(str)
        self.treeview = self.builder.get_object("treeviewAlbum")    
        leftPanel = self.builder.get_object("leftPanel")

        # call retrieve album list
        albumCollection,imageDictionary,photoDictionary = photoOrganizerUtil.walkDir(self.searchEntry,self.hiddenFolders,statusBar,context,treestore,self.treeview,self.imageMap,leftPanel)
        self.lastAlbumCollectionScanned = albumCollection 
        self.totalPhotoDictionary = photoDictionary
        #create tree panel
        if len(albumCollection.albums) >0:
            self.imageMap = imageDictionary
            self.treeview.connect('cursor-changed', self.on_PhotoOrganizer_tree_entry_selected)
            loadWindow.destroy()
            leftPanel.show_all()
        else:
            loadWindow.destroy()
            self.on_PhotoOrganizer_search_error_event() 
    
    #create the main panel with a tree
    def createTwitterPhotoTree(self,albumCollection):
        # create the treestore; the model has one column of type string
        treestore = Gtk.TreeStore(str)
        for album in albumCollection.albums:
            piter = treestore.append(None, ['%s' % album.title])
            self.imageMap[album.title] = None
            subImageMap = {}
            for photo in album.pics:
                subImageMap[photo.fileName] = photo
                treestore.append(piter, ['%s' %album.title+"/"+photo.fileName])
            self.imageMap[album.title] = subImageMap    
        self.treeview = self.builder.get_object("treeviewAlbum")    
        self.treeview.set_model(treestore)
        albumNameCell = Gtk.CellRendererText()
        #build title tree string
        titleTree = "Album found ("+str(len(albumCollection.albums))+") - Total pics ("+str(albumCollection.totalPics)+")"
        albumNameCol = Gtk.TreeViewColumn(titleTree, albumNameCell, text=0)
        self.treeview.connect('cursor-changed', self.on_PhotoOrganizer_tree_entry_selected)
        self.treeview.insert_column(albumNameCol, 0)
            
    def removeSearchResult(self):
        try:
            self.treeview.remove_column(self.treeview.get_column(0))
        except:
            logger.error("skip remove treeitem")  


def init_GUI():
    PhotoOrganizerGUI()

if __name__ == "__main__":
    init_GUI()