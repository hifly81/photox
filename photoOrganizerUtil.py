# coding: latin-1

'''
Created on Mar 21, 2013

@author: hifly
'''

import os
import urllib
import imghdr
import logging
import logging.config
from gi.repository import Gtk
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS

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
    self.latitude = None
    self.longitude = None
    self.copyright = None

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
    photoDictionary = {}
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
                    photoDictionary[album.title+"/"+photo.fileName] = photo
                    treestore.append(piter, ['%s' %album.title+"/"+photo.fileName])
                imageMap[album.title] = subImageMap    
                treeview.set_model(treestore)
                
                albumNameCell = Gtk.CellRendererText()
                titleTree = "Album found ("+str(len(albumCollection.albums))+") - Total pics ("+str(totalPicsFound)+")"
                albumNameCol = Gtk.TreeViewColumn(titleTree, albumNameCell, text=0)
                for col in treeview.get_columns():
                    treeview.remove_column (col)
                treeview.insert_column(albumNameCol, 0)
                leftPanel.add(treeview)
                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)
                
                
    logger.debug("Total pics found:%d"%totalPicsFound)  
    logger.debug("Albums found:%d"%len(albumCollection.albums))
    albumCollection.totalPics = totalPicsFound
    return albumCollection,imageMap,photoDictionary    
         
def get_exif_data(fname):
    ret = {}
    photoFile = None
    lat = None
    longit = None
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "GPSInfo":
                        lat,longit = extractCoordinates(value)  
                    else:
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
                if(ret.has_key('Copyright')):     
                    photoFile.copyright=ret['Copyright']
                    
                if lat:
                    photoFile.latitude = lat
                if longit:
                    photoFile.longitude = longit
                                    
                
    except IOError:
        logger.error("IOERROR %s",fname)
    return photoFile  

def extractCoordinates(exifValue):
    #geocoding
    gpsData = {}
    for gpsTag in exifValue:
        tagElem = GPSTAGS.get(gpsTag, gpsTag)
        gpsData[tagElem] = exifValue[gpsTag]
    
    if "GPSLatitude" in gpsData:
        lat =  gpsData["GPSLatitude"]
        lat = decimalCoordinatesToDegress(lat)
    if "GPSLongitude" in gpsData:
        longit =  gpsData["GPSLongitude"]
        longit = decimalCoordinatesToDegress(longit)
    if "GPSLatitudeRef" in gpsData:
        latRef =  gpsData["GPSLatitudeRef"]
    if "GPSLongitudeRef" in gpsData:
        longitRef =  gpsData["GPSLongitudeRef"]
        
    if latRef != "N":                     
        lat = 0 - lat
    if longitRef != "E":
        longit = 0 - longit
        
    return lat,longit

def decimalCoordinatesToDegress(coord):
    dec = float(coord[0][0])/float(coord[0][1])
    minut = float(coord[1][0])/float(coord[1][1])
    sec = float(coord[2][0])/float(coord[2][1])
    return dec+(minut/60.0)+(sec/3600.0)
    
def savePhotoFromUrl(url,filename):
    f = open( filename, 'wb' )
    data = urllib.urlopen(url).read()
    f.write( data )
    f.close()

def savePhotoFromPixbuf(pixbuf,type,quality,filename):
    pixbuf.savev(filename, type, [],[])
