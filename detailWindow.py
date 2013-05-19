'''
Created on Apr 9, 2013

@author: hifly
'''

from transparentWindow import TransparentWindow
from gi.repository import Gtk, Gdk,GdkPixbuf

class DetailWindow (TransparentWindow):
    def __init__(self,imagePath,detailText):
        super(DetailWindow, self).__init__()
        self.set_size_request(600, 400)
        pimage = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(imagePath)
        scaled_buf = pixbuf.scale_simple(500,300,GdkPixbuf.InterpType.HYPER)
        pimage.set_from_pixbuf(scaled_buf)
        eventBox = Gtk.EventBox()
        eventBox.add(pimage)
        textview = Gtk.TextView()
        textview.get_buffer().set_text(detailText)
        #main box
        buttonClose = Gtk.Button("Close")
        buttonClose.connect("clicked", lambda w: self.destroy())
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        box.pack_start(buttonClose, False, False, 0)
        box.pack_start(eventBox, False, False, 0)
        box.pack_start(textview, False, False, 0)
        self.add(box)
        pimage.show()
        #center the window
        self.set_position(Gtk.WindowPosition.CENTER) 
        self.show_all()
