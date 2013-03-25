'''
Created on Mar 21, 2013

@author: hifly
'''

import StringIO
from gi.repository import Gtk,GdkPixbuf,Gdk,GObject
from PIL import Image,ImageOps

class BasicDeformer:
    def getmesh(self, im):
        x, y = im.size
        return [((0, 0, x, y), (0, 0, x, 0, x, y, y, 0))]

def apply_border(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply border to the pil image
    y = ImageOps.expand(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ) ,border=5,fill='red')
    #must build again the pixbuf from the image
    if y.mode != 'RGB':         
        y = y.convert('RGB')
    buff = StringIO.StringIO()
    y.save(buff, 'ppm')
    contents = buff.getvalue()
    buff.close()
    loader = GdkPixbuf.PixbufLoader.new_with_type('pnm')
    loader.write(contents)
    pixbuf = loader.get_pixbuf()
    loader.close()
    
    return pixbuf

def apply_autocontrast(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = ImageOps.autocontrast(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ) ,cutoff=0)
    #must build again the pixbuf from the image
    if y.mode != 'RGB':         
        y = y.convert('RGB')
    buff = StringIO.StringIO()
    y.save(buff, 'ppm')
    contents = buff.getvalue()
    buff.close()
    loader = GdkPixbuf.PixbufLoader.new_with_type('pnm')
    loader.write(contents)
    pixbuf = loader.get_pixbuf()
    loader.close()
    
    return pixbuf

def apply_deformer(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    deformer = BasicDeformer()
    #apply deform to the pil image
    y = ImageOps.deform(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ) ,deformer)
    #must build again the pixbuf from the image
    if y.mode != 'RGB':         
        y = y.convert('RGB')
    buff = StringIO.StringIO()
    y.save(buff, 'ppm')
    contents = buff.getvalue()
    buff.close()
    loader = GdkPixbuf.PixbufLoader.new_with_type('pnm')
    loader.write(contents)
    pixbuf = loader.get_pixbuf()
    loader.close()
    
    return pixbuf