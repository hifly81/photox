'''
Created on Apr 9, 2013

@author: hifly
'''

from gi.repository import Gtk,GdkPixbuf,Gdk


class LoadingWindow(Gtk.Window):
     def __init__(self):
         Gtk.Window.__init__(self)
         loadImage = Gtk.Image()
         pixbufanim = GdkPixbuf.PixbufAnimation.new_from_file("images/load.gif")
         loadImage.set_from_animation(pixbufanim)
         #no title bar
         self.set_decorated(False)
         self.add(loadImage)
         #center the window
         self.set_position(Gtk.WindowPosition.CENTER)  
         self.show_all()
     
     def close_window(self):
         self.destroy()
