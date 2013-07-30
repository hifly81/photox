# coding: latin-1

'''
Created on Mar 21, 2013

@author: hifly
'''

import StringIO
import cv2
import cv2.cv as cv
import os
from gi.repository import Gtk,GdkPixbuf,Gdk,GObject
from PIL import Image,ImageOps,ImageFilter,ImageEnhance,ImageDraw,ImageFont
import cairo

#constants
RGB = "RGB"
IMAGE_MODE_L = "L"
MAX_VALUE_COLOR = 255
SEPIA_RGB = (255, 240, 192)


class CustomGuassianBlur(ImageFilter.Filter):
    def __init__(self, radius=5):
        self.radius = radius
    
    def filter(self, image):
        return image.gaussian_blur(self.radius)


class BasicDeformer:
    def getmesh(self, im):
        x, y = im.size
        return [((0, 0, x, y), (0, 0, x, 0, x, y, y, 0))]

def apply_deformer(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    deformer = BasicDeformer()
    y = ImageOps.deform(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ) ,deformer)
    return fromImageToPixbuf(y)

def apply_equalizer(pixbuf):    
    '''
    creates a uniform distribution of grayscale values in the output image
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.equalize(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_greyscale(pixbuf):  
    '''
    image to grayscale
    '''  
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.convert(IMAGE_MODE_L)
    return fromImageToPixbuf(y)

def apply_sepia(pixbuf):    
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.convert(IMAGE_MODE_L)
    y = ImageOps.autocontrast(y)
    sepia = []
    r,g,b = SEPIA_RGB
    for value in range(MAX_VALUE_COLOR):
        sepia.extend((r*value/MAX_VALUE_COLOR, g*value/MAX_VALUE_COLOR, b*value/MAX_VALUE_COLOR))
    y.putpalette(sepia)
    y = y.convert(RGB)
    return fromImageToPixbuf(y)

def apply_invert(pixbuf):
    '''
    negative of an image (darkest-->lightest | lightest-->darkest)
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.invert(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_mirror(pixbuf):
    '''
    image left to right
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.mirror(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_flip(pixbuf):
    '''
    image top to bottom
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.flip(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ))
    return fromImageToPixbuf(y)

def apply_blur(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.BLUR)
    return fromImageToPixbuf(y)

def apply_contour(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.CONTOUR)
    return fromImageToPixbuf(y)

def apply_edge(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.FIND_EDGES)
    return fromImageToPixbuf(y)

def apply_emboss(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.EMBOSS)
    return fromImageToPixbuf(y)

def apply_smooth(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.SMOOTH)
    return fromImageToPixbuf(y)

def apply_sharpen(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.filter(ImageFilter.SHARPEN)
    return fromImageToPixbuf(y)

def apply_darkViolet(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    r,g,b = y.split()
    y = Image.merge(RGB,(r,r,b))
    return fromImageToPixbuf(y)

def apply_lightGreen(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    r,g,b = y.split()
    y = Image.merge(RGB,(g,b,g))
    return fromImageToPixbuf(y)

def apply_white(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    r,g,b = y.split()
    y = Image.merge(RGB,(b,b,r))
    return fromImageToPixbuf(y)

def apply_green(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    r,g,b = y.split()
    y = Image.merge(RGB,(b,g,g))
    return fromImageToPixbuf(y)

def apply_light(pixbuf,tilesize=50):
    #TODO
    return pixbuf

def apply_frame(pixbuf):
    '''
    adds a border at all four edges
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.expand(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ) ,border=22,fill='black')
    y = ImageOps.expand(y ,border=42,fill='silver')
    y = ImageOps.expand(y ,border=4,fill='black')
    return fromImageToPixbuf(y)

def apply_polaroid(pixbuf,imageText):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    frameSize = (300,320)  
    imageOutputSize = (270,245) 
    imgModified = Image.open('images/frame.jpg')
    #cropped image to the requested framesize
    imgModified = ImageOps.fit(imgModified, frameSize, Image.ANTIALIAS, 0, (0.5,0.5))
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels()) 
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
Effect based on a range of values
'''

def apply_solarize(pixbuf,threshold):
    '''
    inverts all the pixel under the threshold
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.solarize(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ),threshold)
    return fromImageToPixbuf(y)

def apply_autocontrast(pixbuf,cutoff):
    '''
    autoconstrast removes cutoff % of lightest and darkest pixels and then
    remaps the image so the darkest pixel becomes black and the lightest white
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.autocontrast(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ) ,cutoff)
    return fromImageToPixbuf(y)

def apply_border(pixbuf,borderSize,borderColor):
    '''
    adds a border at all four edges
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.expand(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ) ,border=borderSize,fill=borderColor)
    return fromImageToPixbuf(y)

def apply_unborder(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.crop(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ),1)
    return fromImageToPixbuf(y)

def apply_posterize(pixbuf,bitsReduction):
    '''
    for each color channel reduces the number of bits
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = ImageOps.posterize(Image.fromstring(RGB,(width,height),pixbuf.get_pixels() ),bitsReduction)
    return fromImageToPixbuf(y)

def apply_brightness(pixbuf,brightness=3.0):
    #0.0 black - 0.0 <= value <1.0 darker - 1.0 leaves image unchanged - >1.0 lighter
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    enhancer = ImageEnhance.Brightness(y)
    y = enhancer.enhance(brightness)
    return fromImageToPixbuf(y)

def apply_contrast(pixbuf,contrast=1.3):
    #0.0 solid grey,black image - 1.0 leaves image unchanged
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    enhancer = ImageEnhance.Contrast(y)
    y = enhancer.enhance(contrast)
    return fromImageToPixbuf(y)

def apply_sharpness(pixbuf,sharpness=2.0):
    #0.0 blurred image - 1.0 leaves image unchanged - 2.0 sharpened image
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    enhancer = ImageEnhance.Sharpness(y)
    y = enhancer.enhance(sharpness)
    return fromImageToPixbuf(y)

def apply_color(pixbuf,color=1.5):
    #0.0 black & white image - 1.0 leaves image unchanged -
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    enhancer = ImageEnhance.Color(y)
    y = enhancer.enhance(color)
    return fromImageToPixbuf(y)

def apply_gaussian_blur(pixbuf,radius):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    y = y.filter(CustomGuassianBlur(radius))
    return fromImageToPixbuf(y)

def apply_colorize(pixbuf,colorSubForBlack,colorSubForWhite):
    '''
    colorize is applied to a grayscale image and substitutes all the black pixels with the
    color specified in colorSubForBlack and the white pixels with the color specified in colorSubForWhite
    '''
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    #must be converted to grayscale
    y = ImageOps.grayscale(y)
    y = ImageOps.colorize(y, colorSubForBlack, colorSubForWhite)
    return fromImageToPixbuf(y)

def apply_watermarkSignature(pixbuf,textSignature="text",inputFont="/usr/share/fonts/liberation/LiberationMono-Regular.ttf",rotation=25, opacity=0.25):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
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

def scaleImageFromPixbuf(pixbuf,interpType):
    orig_width =  pixbuf.get_width()
    orig_height = pixbuf.get_height()
    if orig_width >= orig_height:
        if orig_width > 1000:
            orig_width = 1000
        if orig_height > 800:
            orig_height = 800  
    if orig_width < orig_height:
        if orig_width > 800:
            orig_width = 800
        if orig_height > 1000:
            orig_height = 1000
    
    '''
    filter could be applied (increasing order of quality):
        - NEAREST
        - TILES
        - BILINEAR
        - HYPER
    '''
    scaled_buf = pixbuf.scale_simple(orig_width,orig_height,interpType)
    return scaled_buf

def createImageHistogram(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
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
    if y.mode != RGB:         
        y = y.convert(RGB)
    buff = StringIO.StringIO()
    y.save(buff, 'ppm')
    contents = buff.getvalue()
    buff.close()
    loader = GdkPixbuf.PixbufLoader.new_with_type('pnm')
    loader.write(contents)
    pixbuf = loader.get_pixbuf()
    loader.close()
    return pixbuf

def fromPixbufToPilImage(pixbuf):
    width,height = pixbuf.get_width(),pixbuf.get_height() 
    y = Image.fromstring(RGB,(width,height),pixbuf.get_pixels() )
    return y

def buildFacesCoordinates(imagePil):
    faces = []
    im = cv.CreateImageHeader(imagePil.size, cv.IPL_DEPTH_8U, 3)
    cv.SetData(im, imagePil.tostring())
    storage = cv.CreateMemStorage()
    #it looks like the xml closest
    haar=cv.Load("config/haarcascade_frontalface_alt_tree.xml")
    detected = cv.HaarDetectObjects(im, haar, storage, 1.1, 2,cv.CV_HAAR_DO_CANNY_PRUNING,(10,10))
    if detected:
        for face in detected:
            faces.append(face)
    return faces;

def captureWebcamImage():
    camera_port = 0
    ramp_frames = 30
    camera = cv2.VideoCapture(camera_port)
    #time to adjust camera
    for i in xrange(ramp_frames):
        camera.read()
    retval, data = camera.read()
    #tmp file
    file = "/tmp/photoOrganizer.png"
    
    cv2.imwrite(file, data)
    pi = Image.open(file) 

    #remove tmp file
    os.remove(file)
    #close camera
    del(camera)
    
    return fromImageToPixbuf(pi)

def captureDesktopImage():
    #capture entire desktop
    root_win = Gdk.get_default_root_window()
    width = root_win.get_width()
    height = root_win.get_height()
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    pb = Gdk.pixbuf_get_from_window(root_win, 0, 0, width, height)
    cr = cairo.Context(ims)
    Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
    cr.paint()
    return pb