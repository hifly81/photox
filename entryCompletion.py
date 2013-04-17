'''
Created on Apr 9, 2013

@author: hifly
'''

from gi.repository import Gtk, Gdk

COL_TEXT = 0

class EntryCompletion(Gtk.Entry):
     def __init__(self):
         Gtk.Entry.__init__(self)
         completion = Gtk.EntryCompletion()
         completion.set_match_func(self.match_func,None)
         completion.connect("match-selected",self.on_completion_match)
         completion.set_model(Gtk.ListStore(str))
         completion.set_text_column(COL_TEXT)
         self.set_completion(completion)

     def match_func(self, completion, key, iter,column):
         model = completion.get_model()
         return model[iter][COL_TEXT].startswith(self.get_text())

     def on_completion_match(self, completion, model, iter):
         self.set_text(model[iter][COL_TEXT])
         self.set_position(-1)

     def add_words(self, words):
         model = self.get_completion().get_model()
         for word in words:
             model.append([word])
