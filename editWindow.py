'''
Created on Apr 9, 2013

@author: hifly
'''

from transparentWindow import TransparentWindow
from gi.repository import Gtk, Gdk,GdkPixbuf

class EditWindow (TransparentWindow):
    def __init__(self,imagePath):
        super(EditWindow, self).__init__()
        self.set_size_request(600, 400)
        pimage = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(imagePath)
        scaled_buf = pixbuf.scale_simple(500,300,GdkPixbuf.InterpType.HYPER)
        pimage.set_from_pixbuf(scaled_buf)
        eventBox = Gtk.EventBox()
        eventBox.add(pimage)
        #main box
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        boxBottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
        buttonRotateLeft = Gtk.Button("Rotate Left")
        buttonRotateLeft.set_size_request(50,20)
        buttonRotateRight = Gtk.Button("Rotate Right")
        buttonRotateRight.set_size_request(50,20)
        buttonMirror = Gtk.Button("Mirror")
        buttonMirror.set_size_request(50,20)
        buttonFlip = Gtk.Button("Flip")
        buttonFlip.set_size_request(50,20)
        buttonCrop = Gtk.Button("Crop")
        buttonCrop.set_size_request(50,20)
        buttonResize = Gtk.Button("Resize")
        buttonResize.set_size_request(50,20)
        boxBottom.pack_start(buttonRotateLeft, False, False, 0)
        boxBottom.pack_start(buttonRotateRight, False, False, 0)
        boxBottom.pack_start(buttonMirror, False, False, 0)
        boxBottom.pack_start(buttonFlip, False, False, 0)
        boxBottom.pack_start(buttonCrop, False, False, 0)
        boxBottom.pack_start(buttonResize, False, False, 0)
        box.pack_start(eventBox, False, False, 0)
        box.pack_start(boxBottom, False, False, 0)
        self.add(box)
        pimage.show()
        self.show_all()