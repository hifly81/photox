'''
Created on Apr 9, 2013

@author: hifly
'''

from gi.repository import Gtk,GdkPixbuf,Gdk


class LoadingWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        load_image = Gtk.Image()
        pix_buf_animation = GdkPixbuf.PixbufAnimation.new_from_file("images/load.gif")
        load_image.set_from_animation(pix_buf_animation)
        #no title bar
        self.set_decorated(False)
        self.add(load_image)
        #center the window
        self.set_position(Gtk.WindowPosition.CENTER)
        self.show_all()

    def close_window(self):
        self.destroy()
