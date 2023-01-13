# coding: latin-1

'''
Created on Mar 21, 2013

@author: hifly
'''

import os
import time
import imghdr
import logging
import logging.config
from util import geoUtil
from datetime import datetime
from time import strptime
from gi.repository import Gtk
from PIL import Image
from PIL.ExifTags import TAGS
from constant import constantsAccessor as K

logging.config.fileConfig(K.LoggerConstants.DEFAULT_LOGGING_CONF)
logger = logging.getLogger(K.LoggerConstants.DEFAULT_LOGGER_NAME)

class PeopleTag:
    def __init__(self):
        self.totalPics = None
        self.name = None
        self.surname = None
        self.pics = []


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
        #reference to people
        self.people = []


class Album:
    def __init__(self):
        self.year = None
        self.month = None
        self.totalPics = None
        # path of the album
        self.title = None
        self.pics = []
  
    def __lt__(self, other):
        monthSelf = strptime(self.month, K.DateTimeConstants.MONTH_SHORTCUT).tm_mon
        monthOther = strptime(other.month, K.DateTimeConstants.MONTH_SHORTCUT).tm_mon
        if self.year == other.year:
            return monthSelf > monthOther
        else:
            return self.year > other.year


class AlbumCollection:    
    def __init__(self):
        self.totalAlbums = None
        self.totalPics = None
        self.title = None
        self.albums = []
        self.peopleTags = []
  
    #prints class info
    def __str__(self):
        return "%s %s %s %s %s %s %s %s"%(self.fileName, self.shortName, self.date, self.description, self.brand, self.model, self.width, self.height)
  

#scan dirs and searches for img
def walkDir(dirPath, hiddenFolders, statusBar, context, treestore, treeview, imageMap, leftPanel):
    photoDictionary = {}
    yearDictionary = {}
    monthDictionary = {}
    dirPath = dirPath.strip('\n')
    totalPicsFound = 0
    albumCollection = AlbumCollection()

    fileDateTimeYear = None

    if os.path.exists(dirPath):
        for (path, dirs, files) in os.walk(dirPath):
            validDateParsed = False;
            minYearFound = None
            minMonthFoundAsNumber = None
            minMonthFound = None
            logger.debug("Scanning path:%s"%path)
            statusBar.push(context, path)
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)
            album = Album()
            album.title = path
            for file in files:
                #extract creation date
                try:
                    fileDateTime = datetime.fromtimestamp(os.path.getctime(path + os.sep + file)).strftime(K.DateTimeConstants.FULL_DATE_US_SHORTCUT)
                    fileDateTime = datetime.strptime(fileDateTime, K.DateTimeConstants.FULL_DATE_US_SHORTCUT)
                    validDateParsed = True;
                except:
                    print("Unexpected error: can't parse last modification date")

                if validDateParsed is True:
                    try:
                        fileDateTimeYear = fileDateTime.year
                        fileDateTimeMonthAsNumber = fileDateTime.month
                        fileDateTimeMonth = fileDateTime.strftime(K.DateTimeConstants.MONTH_SHORTCUT)
                        if minYearFound is None:
                            minYearFound = fileDateTimeYear
                        if minMonthFound is None:
                            minMonthFound = fileDateTimeMonth
                            minMonthFoundAsNumber = fileDateTimeMonthAsNumber
                        if fileDateTimeYear < minYearFound:
                            minYearFound = fileDateTimeYear
                            minMonthFound = fileDateTimeMonth
                            minMonthFoundAsNumber = fileDateTimeMonthAsNumber
                        else:
                            if fileDateTimeYear < minYearFound and fileDateTimeMonthAsNumber < minMonthFoundAsNumber:
                                minMonthFound = fileDateTimeMonth
                            minMonthFoundAsNumber = fileDateTimeMonthAsNumber
                    except Exception:
                        print("Unexpected error: can't parse")

  
                filename = os.path.join(path, file)
                try:
                    if imghdr.what(filename)!=None:
                        photoFile = get_exif_data(filename)
                        if photoFile==None:
                            photoFile = PhotoFile()  
                        photoFile.dirName = path
                        photoFile.fileName = file
                        photoFile.shortName = photoFile.fileName
                        #extract photo date
                        if photoFile.date is not None:
                            photoFileDateAsTime = datetime.strptime(photoFile.date, "%Y:%m:%d %H:%M:%S")
                            fileDateTimeYear = photoFileDateAsTime.year
                            fileDateTimeMonthAsNumber = photoFileDateAsTime.month
                            fileDateTimeMonth = photoFileDateAsTime.strftime(K.DateTimeConstants.MONTH_SHORTCUT)
                            if minYearFound is None:
                                minYearFound = fileDateTimeYear
                            if minMonthFound is None:
                                minMonthFound = fileDateTimeMonth
                                minMonthFoundAsNumber = fileDateTimeMonthAsNumber
                            if fileDateTimeYear < minYearFound:
                                minYearFound = fileDateTimeYear
                                minMonthFound = fileDateTimeMonth
                                minMonthFoundAsNumber = fileDateTimeMonthAsNumber
                        else:
                            if fileDateTimeYear is not None and fileDateTimeYear < minYearFound and fileDateTimeMonthAsNumber is not None and fileDateTimeMonthAsNumber < minMonthFoundAsNumber:
                                minMonthFound = fileDateTimeMonth
                                minMonthFoundAsNumber = fileDateTimeMonthAsNumber 
                    

                        album.pics.append(photoFile)
                        totalPicsFound+=1 
                except IOError:
                    logger.error("IOERROR %s",filename)  
                    
            #must set album year and month   
            album.year =  minYearFound
            album.month = minMonthFound
            listYearValue = yearDictionary.get(album.year)
            piter = None
            if listYearValue is None:
                if album.year is not None:
                    piter = treestore.append(None, ['%s' % album.year])
                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)
                yearDictionary[album.year] = piter
            
            listMonthValue = monthDictionary.get(str(album.year)+"-"+str(album.month)) 
            if listMonthValue is None:
                piter = treestore.append(yearDictionary[album.year], ['%s' % album.month])
                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)
                monthDictionary[str(album.year)+"-"+str(album.month)] = piter
            
            if len(album.pics) >0 :           
                albumCollection.albums.append(album) 
                album.totalPics = len(album.pics)
                
                #add to tree --> album title
                piter = treestore.append(monthDictionary[str(album.year)+"-"+str(album.month)], ['%s' % album.title])
                imageMap[album.title] = None
                subImageMap = {}
                for photo in album.pics:
                    subImageMap[photo.fileName] = photo
                    photoDictionary[album.title + os.sep + photo.fileName] = photo
                    treestore.append(piter, ['%s' %album.title + os.sep + photo.fileName])
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
                
                
    logger.debug("***Final count:Total pics found:%d"%totalPicsFound)  
    logger.debug("***Final count:Albums found:%d"%len(albumCollection.albums))
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
            try:
                exifinfo = img._getexif()
                if exifinfo != None:
                    for tag, value in exifinfo.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "GPSInfo":
                            lat,longit = geoUtil.extractCoordinates(value)
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
            except Exception :
                print("Unexpected error: can't extract exif data")
                                    
                
    except IOError:
        logger.error("IOERROR %s",fname)
    return photoFile
