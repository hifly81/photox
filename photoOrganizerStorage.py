'''
Created on Mar 25, 2012

@author: hifly
'''

try:
    import cPickle as pickle
except:
    import pickle
import sys
import os

class PhotoOrganizerPref:
  def __init__(self,hiddenFolders,lastSearch,albumCollection,peopleTag):
    self.hiddenFolders = hiddenFolders  
    self.lastSearch = lastSearch
    self.albumCollection = albumCollection
    self.peopleTag = peopleTag

def savePref(photoOrganizerPref):
    data = []
    data.append(photoOrganizerPref)
    #check if photo organizer dir exists
    home = os.getenv("HOME")
    try:
        os.makedirs(home + str("/.photorganizer/"))
    except OSError:
        pass

    filename = home + str("/.photorganizer/") + str("phzerpref.ser")
    out_s = open(filename, 'wb')
    try:
        # Write to the stream
        for o in data:
            pickle.dump(o, out_s)
    finally:
        out_s.close()     
        
def loadPref():
    home = os.getenv("HOME")
    filename = home + str("/.photorganizer/") + str("phzerpref.ser")
    if(os.path.isfile(filename)==True):
        in_s = open(filename, 'rb')
        try:
            # Read the data
            while True:
                try:
                    pref = pickle.load(in_s)
                except EOFError:
                    break
                else:
                    return pref   
        finally:
            in_s.close()       