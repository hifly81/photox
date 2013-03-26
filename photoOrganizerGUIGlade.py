'''
Created on Mar 01, 2013

@author: hifly
'''

import os
import math
import urllib2
import logging.config
import twitterUtil
import photoOrganizerStorage
import photoOrganizerUtil
import photoEffects
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

#context menu not designed in GLADE
UI_INFO = """
<ui>
  <popup name='PopupMenu'>
    <menuitem action='EditOriginalSize' />
    <menuitem action='EditMirror' />
    <menuitem action='EditRotate' />
    <menuitem action='EditBordered' />
    <menuitem action='EditUnbordered' />
    <menuitem action='EditAutocontrast' />
    <menuitem action='EditDeform' />
    <menuitem action='EditEqualize' />
    <menuitem action='EditGreyScale' />
    <menuitem action='EditInvert' />
    <menuitem action='EditPosterize' />
    <menuitem action='EditSolarize' />
    <menuitem action='EditBlur' />
    <menuitem action='EditContour' />
    <menuitem action='EditEdge' />
    <menuitem action='EditEmboss' />
    <menuitem action='EditSmooth' />
    <menuitem action='EditSharpen' />
    <menuitem action='EditBrigthness' />
    <menuitem action='EditContrast' />
    <menuitem action='EditSharpness' />
    <menuitem action='EditColor' />
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
                    "on_PhotoOrganizer_original_size_clicked":self.on_PhotoOrganizer_original_size_clicked,
                    "on_PhotoOrganizer_mirror_clicked": self.on_PhotoOrganizer_mirror_clicked,
                    "on_PhotoOrganizer_rotate_clicked": self.on_PhotoOrganizer_rotate_clicked,
                    "on_PhotoOrganizer_border_clicked": self.on_PhotoOrganizer_border_clicked,
                    "on_PhotoOrganizer_unborder_clicked":self.on_PhotoOrganizer_unborder_clicked,
                    "on_PhotoOrganizer_autocontrast_clicked": self.on_PhotoOrganizer_autocontrast_clicked,
                    "on_PhotoOrganizer_deform_clicked": self.on_PhotoOrganizer_deform_clicked,
                    "on_PhotoOrganizer_equalize_clicked": self.on_PhotoOrganizer_equalize_clicked,
                    "on_PhotoOrganizer_greyscale_clicked":self.on_PhotoOrganizer_greyscale_clicked,
                    "on_PhotoOrganizer_invert_clicked": self.on_PhotoOrganizer_invert_clicked,
                    "on_PhotoOrganizer_posterize_clicked": self.on_PhotoOrganizer_posterize_clicked,
                    "on_PhotoOrganizer_solarize_clicked": self.on_PhotoOrganizer_solarize_clicked,
                    "on_PhotoOrganizer_blur_clicked":self.on_PhotoOrganizer_blur_clicked,
                    "on_PhotoOrganizer_contour_clicked":self.on_PhotoOrganizer_contour_clicked,
                    "on_PhotoOrganizer_edge_clicked": self.on_PhotoOrganizer_edge_clicked,
                    "on_PhotoOrganizer_emboss_clicked": self.on_PhotoOrganizer_emboss_clicked,
                    "on_PhotoOrganizer_smooth_clicked": self.on_PhotoOrganizer_smooth_clicked,
                    "on_PhotoOrganizer_sharpen_clicked":self.on_PhotoOrganizer_sharpen_clicked,
                    "on_PhotoOrganizer_brightness_clicked": self.on_PhotoOrganizer_brightness_clicked,
                    "on_PhotoOrganizer_contrast_clicked": self.on_PhotoOrganizer_contrast_clicked,
                    "on_PhotoOrganizer_sharpness_clicked": self.on_PhotoOrganizer_sharpness_clicked,
                    "on_PhotoOrganizer_color_clicked":self.on_PhotoOrganizer_color_clicked,
                    "on_PhotoOrganizer_save_clicked":self.on_PhotoOrganizer_save_clicked,
        }
        #handler of GUI signals
        self.builder.connect_signals(handlers)
        
        #change textview color
        parse, color = Gdk.Color.parse('#F0F0F0')
        self.builder.get_object("detailsEntry").modify_bg(Gtk.StateType.NORMAL, color) 
            
        #show main window
        self.window = self.builder.get_object("PhotoOrganizer")
        self.window.connect("key_press_event",self.on_PhotoOrganizer_image_keypress_event)           
        self.window.show_all()
        
        #load pref at startup, including albums saved
        self.loadPreferences()
    
        #main gtk
        Gtk.main()
    
    
    '''
        SECTION FOR EVENTS
    '''
    
    #event on quit app
    def on_PhotoOrganizer_delete_event  (self, *args):
        if(self.lastAlbumCollectionScanned is not None):
            #save the preferences
            photoFile = PhotoOrganizerPref(self.hiddenFolders,self.entry_folder_text,self.lastAlbumCollectionScanned)
        photoOrganizerStorage.savePref(photoFile)
        Gtk.main_quit()
    
    #event on filesystem search
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
            self.removeSearchResult(self.builder.get_object("treeviewAlbum"));
            
            # You'll need to import gobject
            GObject.timeout_add(100, self.callScanPhoto)
            dialog.destroy()

    
    def on_PhotoOrganizer_twitter_search_event(self,widget,event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "Return":
            self.twitterSearch = True
            self.removeSearchResult(self.builder.get_object("treeviewTwitter"));    
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
                    treeview = self.builder.get_object("treeviewTwitter")
                    self.createFixedPhotoTree(albumCollection,treeview)
                    #set current tab
                    self.builder.get_object("notebook1").set_current_page(1)
                    leftPanel = self.builder.get_object("leftPanel1")
                    leftPanel.add(treeview)
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
        #take the treeview linked to specific tab
        currentPage = self.builder.get_object("notebook1").get_current_page()
        if currentPage == 0:
            self.currentTreeview = self.builder.get_object("treeviewAlbum")
            self.twitterSearch = False
        else:
           self.currentTreeview = self.builder.get_object("treeviewTwitter") 
           self.twitterSearch = True
        
        selection = self.currentTreeview.get_selection()
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
    
    def on_PhotoOrganizer_border_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_border(pixbuf)) 
    
    def on_PhotoOrganizer_unborder_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_unborder(pixbuf)) 
    
    def on_PhotoOrganizer_autocontrast_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()   
        self.imageOpened.set_from_pixbuf(photoEffects.apply_autocontrast(pixbuf)) 
        
    def on_PhotoOrganizer_deform_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_deformer(pixbuf))    
    
    def on_PhotoOrganizer_equalize_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_equalizer(pixbuf))
    
    def on_PhotoOrganizer_greyscale_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_greyscale(pixbuf))
    
    def on_PhotoOrganizer_invert_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_invert(pixbuf))
    
    def on_PhotoOrganizer_mirror_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_mirror(pixbuf))
    
    def on_PhotoOrganizer_posterize_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_posterize(pixbuf))
    
    def on_PhotoOrganizer_solarize_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_solarize(pixbuf))
    
    def on_PhotoOrganizer_blur_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_blur(pixbuf))
    
    def on_PhotoOrganizer_contour_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_contour(pixbuf))
    
    def on_PhotoOrganizer_edge_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_edge(pixbuf))
    
    def on_PhotoOrganizer_emboss_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_emboss(pixbuf))
    
    def on_PhotoOrganizer_smooth_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_smooth(pixbuf))
    
    def on_PhotoOrganizer_sharpen_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_sharpen(pixbuf))
        
    def on_PhotoOrganizer_brightness_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_brightness(pixbuf)) 
    
    def on_PhotoOrganizer_contrast_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_contrast(pixbuf)) 
    
    def on_PhotoOrganizer_sharpness_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_sharpness(pixbuf))   
    
    def on_PhotoOrganizer_color_clicked(self, widget):
        pixbuf = self.imageOpened.get_pixbuf()
        self.imageOpened.set_from_pixbuf(photoEffects.apply_color(pixbuf))  
        
    def on_PhotoOrganizer_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Save your image", self,Gtk.FileChooserAction.SAVE,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_default_size(800, 400)
     
        Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True)
        Gtk.FileChooser.set_current_name(dialog, "Untitled document")
        
        filter = Gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
   
        filter = Gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.xpm")
        dialog.add_filter(filter)

        response = dialog.run()
        
        if response == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()
            dialog.destroy()
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)
            if(self.twitterSearch):
                photoOrganizerUtil.savePhotoFromUrl(self.lastTwitterImageUrl,filename)
            else:
                photoOrganizerUtil.savePhotoFromPixbuf(self.imageOpened.get_pixbuf(),"jpeg",100,filename);
           
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
    
    '''
        END SECTION FOR EVENTS
    '''
            
    def create_image_context_menu(self):
        action_group = Gtk.ActionGroup("my_actions")
        action_group.add_actions([                   
            ("EditOriginalSize", Gtk.STOCK_ZOOM_FIT, "Original size", "<control><alt>O", None,
             self.on_PhotoOrganizer_original_size_clicked),
            ("EditMirror", Gtk.STOCK_OK, "Mirror", "<control><alt>M", None,
             self.on_PhotoOrganizer_mirror_clicked),
            ("EditRotate", Gtk.STOCK_REFRESH, "Rotate", "<control><alt>R", None,
             self.on_PhotoOrganizer_rotate_clicked),
            ("EditBordered", Gtk.STOCK_REFRESH, "Border", "<control><alt>B", None,
             self.on_PhotoOrganizer_border_clicked),
            ("EditUnbordered", Gtk.STOCK_REFRESH, "Unborder", "<control><alt>U", None,
             self.on_PhotoOrganizer_unborder_clicked),                      
            ("EditAutocontrast", Gtk.STOCK_REFRESH, "Autocontrast", "<control><alt>A", None,
             self.on_PhotoOrganizer_autocontrast_clicked),        
            ("EditDeform", Gtk.STOCK_REFRESH, "Deform", "<control><alt>D", None,
             self.on_PhotoOrganizer_deform_clicked),    
            ("EditEqualize", Gtk.STOCK_REFRESH, "Equalize", "<control><alt>E", None,
             self.on_PhotoOrganizer_equalize_clicked),      
            ("EditGreyScale", Gtk.STOCK_REFRESH, "GreyScale", "<control><alt>G", None,
             self.on_PhotoOrganizer_greyscale_clicked), 
            ("EditInvert", Gtk.STOCK_OK, "Invert", "<control><alt>I", None,
             self.on_PhotoOrganizer_invert_clicked), 
            ("EditPosterize", Gtk.STOCK_OK, "Posterize", "<control><alt>P", None,
             self.on_PhotoOrganizer_posterize_clicked),  
            ("EditSolarize", Gtk.STOCK_OK, "Solarize", "<control><alt>Z", None,
             self.on_PhotoOrganizer_solarize_clicked),         
            ("EditBlur", Gtk.STOCK_OK, "Blur", "<control><alt>K", None,
             self.on_PhotoOrganizer_blur_clicked),
            ("EditContour", Gtk.STOCK_OK, "Contour", "<control><alt>W", None,
             self.on_PhotoOrganizer_contour_clicked),   
            ("EditEdge", Gtk.STOCK_OK, "Edge", "<control><alt>E", None,
             self.on_PhotoOrganizer_edge_clicked),
            ("EditEmboss", Gtk.STOCK_OK, "Emboss", "<control><alt>B", None,
             self.on_PhotoOrganizer_emboss_clicked),     
            ("EditSmooth", Gtk.STOCK_OK, "Smooth", "<control><alt>T", None,
             self.on_PhotoOrganizer_smooth_clicked), 
            ("EditSharpen", Gtk.STOCK_OK, "Sharpen", "<control><alt>H", None,
             self.on_PhotoOrganizer_sharpen_clicked), 
            ("EditColor", Gtk.STOCK_OK, "Color", "<control><alt>Y", None,
             self.on_PhotoOrganizer_color_clicked), 
            ("EditBrigthness", Gtk.STOCK_OK, "Brigthness", "<control><alt>B", None,
             self.on_PhotoOrganizer_brightness_clicked),
            ("EditContrast", Gtk.STOCK_OK, "Contrast", "<control><alt>L", None,
             self.on_PhotoOrganizer_contrast_clicked),  
            ("EditSharpness", Gtk.STOCK_OK, "Sharpness", "<control><alt>G", None,
             self.on_PhotoOrganizer_sharpness_clicked),      
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
                    pass
        else:
            self.builder.get_object("detailsEntry").get_buffer().set_text("")
            currentPhoto = self.totalPhotoDictionary[imagePath]
            gpsText = "\ntaken at:"
            dateText = "date:"
            authorText = "\nby:"
            descText = "\ndescription:"
            modelText = "\ncamera:"
            if currentPhoto.date:
                dateText = dateText+currentPhoto.date
            if currentPhoto.description:
                descText = descText+currentPhoto.description
            if currentPhoto.author:
                authorText = authorText+currentPhoto.author
            if currentPhoto.brand:
                modelText = modelText+str(currentPhoto.brand)+","+str(currentPhoto.model)
            if currentPhoto.latitude:
                gpsText = gpsText+str(currentPhoto.latitude)+","+str(currentPhoto.longitude)
            self.builder.get_object("detailsEntry").get_buffer().set_text(dateText+descText+authorText+modelText+gpsText)
    
    #create image viewer panel
    def createImagePanel(self,pimage,imageName):    
        imagePanel = self.builder.get_object("imagePanel")
        try:
            imagePanel.remove(imagePanel.get_children()[0])
        except:
            pass
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
        treeview = self.builder.get_object("treeviewAlbum")    
        leftPanel = self.builder.get_object("leftPanel")
        #set current tab
        self.builder.get_object("notebook1").set_current_page(0)

        # call retrieve album list
        albumCollection,imageDictionary,photoDictionary = photoOrganizerUtil.walkDir(self.searchEntry,self.hiddenFolders,statusBar,context,treestore,treeview,self.imageMap,leftPanel)
        self.lastAlbumCollectionScanned = albumCollection 
        self.totalPhotoDictionary = photoDictionary
        #create tree panel
        if len(albumCollection.albums) >0:
            self.imageMap = imageDictionary
            self.currentTreeview = treeview
            treeview.connect('cursor-changed', self.on_PhotoOrganizer_tree_entry_selected)
            loadWindow.destroy()
            leftPanel.show_all()
        else:
            loadWindow.destroy()
            self.on_PhotoOrganizer_search_error_event() 
    
    #create the main panel with a tree
    def createFixedPhotoTree(self,albumCollection,treeview):
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
        treeview.set_model(treestore)
        albumNameCell = Gtk.CellRendererText()
        #build title tree string
        titleTree = "Album found ("+str(len(albumCollection.albums))+") - Total pics ("+str(albumCollection.totalPics)+")"
        albumNameCol = Gtk.TreeViewColumn(titleTree, albumNameCell, text=0)
        self.currentTreeview = treeview
        treeview.connect('cursor-changed', self.on_PhotoOrganizer_tree_entry_selected)
        treeview.insert_column(albumNameCol, 0)
            
    def removeSearchResult(self,treeview):
        try:
            treeview.remove_column(treeview.get_column(0))
        except:
            pass  
    
    def loadPreferences(self):
        #load preferences
        photoOrganizerPref = photoOrganizerStorage.loadPref()
        if(photoOrganizerPref!=None):
            try:
                #load album saved
                self.hiddenFolders = photoOrganizerPref.hiddenFolders
                self.entry_folder_text = photoOrganizerPref.lastSearch
                treeview = self.builder.get_object("treeviewAlbum")
                self.createFixedPhotoTree(photoOrganizerPref.albumCollection,treeview)
                #rebuild photo indexes
                self.totalPhotoDictionary = {}
                savedAlbums = photoOrganizerPref.albumCollection
                for album in savedAlbums.albums:
                    for photo in album.pics:
                        self.totalPhotoDictionary[album.title+"/"+photo.fileName] = photo

                
                #set current tab
                self.builder.get_object("notebook1").set_current_page(0)
                leftPanel = self.builder.get_object("leftPanel")
                leftPanel.add(treeview)
                leftPanel.show_all()
                self.twitterSearch = False
            #some pref properties stored could be not present --> no previous search available
            except:
                pass


def init_GUI():
    PhotoOrganizerGUI()

if __name__ == "__main__":
    init_GUI()