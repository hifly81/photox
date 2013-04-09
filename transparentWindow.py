'''
Created on Apr 9, 2013

@author: hifly
'''

import cairo
from gi.repository import Gtk, Gdk

class TransparentWindow (Gtk.Window):
    def __init__(self):
        super(TransparentWindow, self).__init__()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(30)
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        self.set_decorated(False)
        if self.visual != None and self.screen.is_composited():
            self.set_visual(self.visual)

        self.set_app_paintable(True)
        self.connect("draw", self.area_draw)

    def area_draw(self, widget, cr):
        cr.set_source_rgba(.2, .2, .2, 0.9)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
