'''
Created on Mar 25, 2012

@author: hifly
'''

import sys
import os
import imghdr
import logging
import logging.config
from gi.repository import Gtk
from PIL import Image
from PIL.ExifTags import TAGS

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger('photoOrganizer')

#class which stores img info
class PhotoFile:
  def __init__(self):
    self.dirName = None  
    self.fileName = None
    self.mediaUrl = None
    self.shortName = None
    self.date = None
    self.description = None
    self.brand = None
    self.model = None
    self.width = None
    self.height = None
    self.author = None

class Album:
  def __init__(self):
    self.totalPics = None
    self.title = None
    self.pics = []

class AlbumCollection:    
  def __init__(self):
    self.totalAlbums = None
    self.totalPics = None
    self.title = None
    self.albums = []
  
  #prints class info  
  def __str__(self):
        return "%s %s %s %s %s %s %s %s"%(self.fileName,self.shortName,self.date,self.description,self.brand,self.model,self.width,self.height)
  

#scan dirs and searches for img
def walkDir(dirPath,hiddenFolders,statusBar,context,treestore,treeview,imageMap,leftPanel):
    dirPath = dirPath.strip('\n')
    totalPicsFound = 0
    albumCollection = AlbumCollection()
    if os.path.exists(dirPath):
        for (path, dirs, files) in os.walk(dirPath):
            logger.debug("Scanning path:%s"%path)
            statusBar.push(context, path)
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)
            album = Album()
            album.title = path
            for file in files:
                filename = os.path.join(path, file)
                try:
                    if imghdr.what(filename)!=None:
                        photoFile = get_exif_data(filename)
                        if photoFile==None:
                            photoFile = PhotoFile()  
                        photoFile.dirName = path
                        photoFile.fileName = file
                        photoFile.shortName = photoFile.fileName
                        album.pics.append(photoFile)
                        totalPicsFound+=1 
                except IOError:
                    logger.error("IOERROR %s",filename)      
            if len(album.pics) >0 :           
                albumCollection.albums.append(album) 
                album.totalPics = len(album.pics)
                
                #add to tree
                piter = treestore.append(None, ['%s' % album.title])
                imageMap[album.title] = None
                subImageMap = {}
                for photo in album.pics:
                    subImageMap[photo.fileName] = photo
                    treestore.append(piter, ['%s' %album.title+"/"+photo.fileName])
                imageMap[album.title] = subImageMap    
                treeview.set_model(treestore)
                
                albumNameCell = Gtk.CellRendererText()
                titleTree = "Album found ("+str(len(albumCollection.albums))+") - Total pics ("+str(totalPicsFound)+")"
                albumNameCol = Gtk.TreeViewColumn(titleTree, albumNameCell, text=0)
                treeview.insert_column(albumNameCol, 0)
                leftPanel.add(treeview)
                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)
                
                
    logger.debug("Total pics found:%d"%totalPicsFound)  
    logger.debug("Albums found:%d"%len(albumCollection.albums))
    albumCollection.totalPics = totalPicsFound
    return albumCollection,imageMap     
         
def get_exif_data(fname):
    ret = {}
    photoFile = None
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
                photoFile = PhotoFile()    
                if(ret.has_key('DateTimeDigitized')):    
                    photoFile.date=ret['DateTimeDigitized']
                if(ret.has_key('ImageDescription')):    
                    photoFile.description=ret['ImageDescription']
                if(ret.has_key('Make')):    
                    photoFile.brand=ret['Make']
                if(ret.has_key('Model')):     
                    photoFile.model=ret['Model']
                if(ret.has_key('ExifImageWidth')):     
                    photoFile.width=ret['ExifImageWidth']
                if(ret.has_key('ExifImageHeight')):     
                    photoFile.height=ret['ExifImageHeight'] 
    except IOError:
        logger.error("IOERROR %s",fname)
    return photoFile   