# coding: latin-1

'''
Created on Mar 21, 2013

@author: hifly
'''

'''
The Python Imaging Library is:

Copyright © 1997-2005 by Secret Labs AB
Copyright © 1995-2005 by Fredrik Lundh
By obtaining, using, and/or copying this software and/or its associated documentation, you agree that you have read, understood, and will comply with the following terms and conditions:

Permission to use, copy, modify, and distribute this software and its associated documentation for any purpose and without fee is hereby granted, provided that the above copyright notice appears in all copies, and that both that copyright notice and this permission notice appear in supporting documentation, and that the name of Secret Labs AB or the author not be used in advertising or publicity pertaining to distribution of the software without specific, written prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

import StringIO
from gi.repository import Gtk,GdkPixbuf,Gdk,GObject
from PIL import Image,ImageOps,ImageFilter,ImageEnhance,ImageDraw,ImageFont

class BasicDeformer:
    def getmesh(self, im):
        x, y = im.size
        return [((0, 0, x, y), (0, 0, x, 0, x, y, y, 0))]

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

def apply_sepia(pixbuf):    
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    y = y.convert('L')
    y = ImageOps.autocontrast(y)
    sepia = []
    r,g,b = (255, 240, 192)
    for value in range(255):
        sepia.extend((r*value/255, g*value/255, b*value/255))
    y.putpalette(sepia)
    y = y.convert("RGB")
    return fromImageToPixbuf(y)

def apply_invert(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.invert(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_mirror(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.mirror(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ))
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

def apply_darkViolet(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    r,g,b = y.split()
    y = Image.merge('RGB',(r,r,b))
    return fromImageToPixbuf(y)

def apply_lightGreen(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    r,g,b = y.split()
    y = Image.merge('RGB',(g,b,g))
    return fromImageToPixbuf(y)

def apply_white(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    r,g,b = y.split()
    y = Image.merge('RGB',(b,b,r))
    return fromImageToPixbuf(y)

def apply_green(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    r,g,b = y.split()
    y = Image.merge('RGB',(b,g,g))
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

'''
Effect based on a range of values --> brightness,contrast
'''

def apply_border(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.expand(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ) ,border=5,fill='red')
    return fromImageToPixbuf(y)

def apply_unborder(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.crop(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ),1)
    return fromImageToPixbuf(y)

def apply_posterize(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.posterize(Image.fromstring("RGB",(width,height),pixbuf.get_pixels() ),4)
    return fromImageToPixbuf(y)

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

def apply_watermarkSignature(pixbuf,textSignature="text",inputFont="/usr/share/fonts/gnu-free/FreeMono.ttf",rotation=25, opacity=0.25):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    textImage = Image.new('RGBA', y.size, (0,0,0,0))
    fontSize = 2
    fontImage = ImageFont.truetype(inputFont, fontSize)
    fontWidth, fontHeight = fontImage.getsize(textSignature)
    while (fontWidth+fontHeight < textImage.size[0]):
        fontSize += 2
        fontImage = ImageFont.truetype(inputFont, fontSize)
        fontWidth, fontHeight = fontImage.getsize(textSignature)
    textDraw = ImageDraw.Draw(textImage, 'RGBA')
    textDraw.text(((textImage.size[0] - fontWidth) / 2,
              (textImage.size[1] - fontHeight) / 2),
              textSignature, font=fontImage)
    textImage = textImage.rotate(rotation,Image.BICUBIC)
    splittedImage = textImage.split()[3]
    splittedImage = ImageEnhance.Brightness(splittedImage).enhance(opacity)
    textImage.putalpha(splittedImage)
    return fromImageToPixbuf(Image.composite(textImage, y, textImage))

def scaleImageFromPixbuf(pixbuf):
    orig_width =  pixbuf.get_width()
    orig_height = pixbuf.get_height()
    if orig_width >= orig_height:
        if orig_width > 700:
            orig_width = 700
        if orig_height > 600:
            orig_height = 600  
    if orig_width < orig_height:
        if orig_width > 600:
            orig_width = 600
        if orig_height > 700:
            orig_height = 700
    scaled_buf = pixbuf.scale_simple(orig_width,orig_height,GdkPixbuf.InterpType.BILINEAR)
    return scaled_buf

def createImageHistogram(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring("RGB",(width,height),pixbuf.get_pixels() )
    histogram = y.histogram()
    #create new image with histogram
    histogramImage = Image.new("RGBA", (300, 200))   
    histogramLineImage = ImageDraw.Draw(histogramImage)
    
    #draw histogram lines  
    red = (255,0,0)              
    green = (0,255,0)             
    blue = (0,0,255) 
    xAxis=0 
    yAxis=0
    scalingFactor = float((200)*1.5)/max(histogram)
    for value in histogram:
        if (value > 0):
            rgb = red
            if (yAxis > 255): 
                rgb = green
            if (yAxis > 511): 
                rgb = blue
            histogramLineImage.line((xAxis, 200, xAxis, 200-(value*scalingFactor)), fill=rgb)        
            if (xAxis > 255): 
                xAxis=0
            else: 
                xAxis+=1
            yAxis+=1
    
    return fromImageToPixbuf(histogramImage)

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