# coding: latin-1

'''
Created on Mar 21, 2013

@author: hifly
'''

from PIL.ExifTags import GPSTAGS


def extractCoordinates(exifValue):
    latRef = None
    longitRef = None
    lat = None
    longit = None

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

    if latRef is not None and latRef != "N":
        lat = 0 - lat
    if longitRef is not None and longitRef != "E":
        longit = 0 - longit

    return lat,longit

def decimalCoordinatesToDegress(coord):
    dec = float(coord[0][0])/float(coord[0][1])
    minut = float(coord[1][0])/float(coord[1][1])
    sec = float(coord[2][0])/float(coord[2][1])
    return dec+(minut/60.0)+(sec/3600.0)