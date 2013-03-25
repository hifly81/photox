'''
Created on Mar 21, 2013

@author: hifly
'''

import StringIO
from gi.repository import Gtk,GdkPixbuf,Gdk,GObject
from PIL import Image,ImageOps,ImageFilter

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

def apply_unborder(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply border to the pil image
    y = ImageOps.crop(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ),1)
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

def apply_equalizer(pixbuf):    
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = ImageOps.equalize(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
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

def apply_greyscale(pixbuf):    
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.convert('L')
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

def apply_invert(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = ImageOps.invert(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
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

def apply_mirror(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = ImageOps.mirror(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
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

def apply_posterize(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = ImageOps.posterize(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ),4)
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

def apply_solarize(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = ImageOps.solarize(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
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

def apply_blur(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.BLUR)
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

def apply_contour(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.CONTOUR)
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

def apply_edge(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.FIND_EDGES)
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

def apply_emboss(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.EMBOSS)
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

def apply_smooth(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.SMOOTH)
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

def apply_sharpen(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    #apply autocontrast to the pil image
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.SHARPEN)
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