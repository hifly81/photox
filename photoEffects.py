'''
Created on Mar 21, 2013

@author: hifly
'''

import StringIO
from gi.repository import Gtk,GdkPixbuf,Gdk,GObject
from PIL import Image,ImageOps,ImageFilter,ImageEnhance,ImageDraw

class BasicDeformer:
    def getmesh(self, im):
        x, y = im.size
        return [((0, 0, x, y), (0, 0, x, 0, x, y, y, 0))]

def apply_border(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.expand(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ) ,border=5,fill='red')
    return fromImageToPixbuf(y)

def apply_unborder(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.crop(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ),1)
    return fromImageToPixbuf(y)

def apply_autocontrast(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.autocontrast(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ) ,cutoff=0)
    return fromImageToPixbuf(y)

def apply_deformer(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    deformer = BasicDeformer()
    y = ImageOps.deform(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ) ,deformer)
    return fromImageToPixbuf(y)

def apply_equalizer(pixbuf):    
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.equalize(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_greyscale(pixbuf):    
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.convert('L')
    return fromImageToPixbuf(y)

def apply_invert(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.invert(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_mirror(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.mirror(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_posterize(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.posterize(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ),4)
    return fromImageToPixbuf(y)

def apply_solarize(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.solarize(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_blur(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.BLUR)
    return fromImageToPixbuf(y)

def apply_contour(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.CONTOUR)
    return fromImageToPixbuf(y)

def apply_edge(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.FIND_EDGES)
    return fromImageToPixbuf(y)

def apply_emboss(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.EMBOSS)
    return fromImageToPixbuf(y)

def apply_smooth(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.SMOOTH)
    return fromImageToPixbuf(y)

def apply_sharpen(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.SHARPEN)
    return fromImageToPixbuf(y)

'''
Effect based on a range of values --> brightness,contrast
'''

def apply_brightness(pixbuf,brightness=3.0):
    #0.0 black - 1.0 leaves image unchanged
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    enhancer = ImageEnhance.Brightness(y)
    y = enhancer.enhance(brightness)
    return fromImageToPixbuf(y)

def apply_contrast(pixbuf,contrast=1.3):
    #0.0 solid grey image - 1.0 leaves image unchanged
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    enhancer = ImageEnhance.Contrast(y)
    y = enhancer.enhance(contrast)
    return fromImageToPixbuf(y)

def apply_sharpness(pixbuf,sharpness=2.0):
    #0.0 blurred image - 1.0 leaves image unchanged - 2.0 sharpened image
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    enhancer = ImageEnhance.Sharpness(y)
    y = enhancer.enhance(sharpness)
    return fromImageToPixbuf(y)

def apply_color(pixbuf,color=1.5):
    #0.0 black & white image - 1.0 leaves image unchanged -
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    enhancer = ImageEnhance.Color(y)
    y = enhancer.enhance(color)
    return fromImageToPixbuf(y)

def apply_polaroid(pixbuf,imageText):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    frameSize = (300,320)  
    imageOutputSize = (270,245) 
    imgModified = Image.open('images/frame.jpg')
    #cropped image to the requested framesize
    imgModified = ImageOps.fit(imgModified, frameSize, Image.ANTIALIAS, 0, (0.5,0.5))
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels()) 
    #cropped image to the requested size
    y = ImageOps.fit(y, imageOutputSize, Image.ANTIALIAS, 0, (0.5,0.5))
    y = ImageOps.autocontrast(y, cutoff=2)
    y = ImageEnhance.Sharpness(y).enhance(2.0)
    
    boxOnImage = (12,18) 
    imgModified.paste(y, boxOnImage)
    
    #text on image
    textWidget = ImageDraw.Draw(imgModified).textsize(imageText)
    fontxy = (frameSize[0]/2 - textWidget[0]/2, 278)
    ImageDraw.Draw(imgModified).text(fontxy, imageText,fill=(40,40,40))
    
    imgOutput = Image.new(imgModified.mode, (300,320))
    imgOutput.paste(imgModified, (imgOutput.size[0]/2-imgModified.size[0]/2, imgOutput.size[1]/2-imgModified.size[1]/2))
 
    return fromImageToPixbuf(imgOutput)

    
def fromImageToPixbuf(y):
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