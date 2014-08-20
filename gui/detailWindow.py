'''
Created on Apr 9, 2013

@author: hifly
'''

from gi.repository import Gtk, Gdk,GdkPixbuf

from gui.transparentWindow import TransparentWindow


class DetailWindow (TransparentWindow):
    def __init__(self,imagePath,detailText):
        super(DetailWindow, self).__init__()
        self.set_size_request(600, 400)
        p_image = Gtk.Image()
        pix_buf = GdkPixbuf.Pixbuf.new_from_file(imagePath)
        scaled_buf = pix_buf.scale_simple(500,300,GdkPixbuf.InterpType.HYPER)
        p_image.set_from_pixbuf(scaled_buf)
        eventBox = Gtk.EventBox()
        eventBox.add(p_image)
        text_view = Gtk.TextView()
        text_view.get_buffer().set_text(detailText)
        #main box
        buttonClose = Gtk.Button("Close")
        buttonClose.connect("clicked", lambda w: self.destroy())
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        box.pack_start(buttonClose, False, False, 0)
        box.pack_start(eventBox, False, False, 0)
        box.pack_start(text_view, False, False, 0)
        self.add(box)
        p_image.show()
        #center the window
        self.set_position(Gtk.WindowPosition.CENTER) 
        self.show_all()
