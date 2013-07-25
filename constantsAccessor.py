# coding: latin-1

'''
Created on Jul 25, 2013

@author: hifly
'''


class DateTimeConstants:
    NEW = 1


class LoggerConstants:
    DEFAULT_LOGGER_NAME = "photoOrganizer"
    DEFAULT_LOGGING_CONF = "'config/logging.conf'"


class GladeConstants:
    MAIN_GUI_FILE = "glade/photoOrganizerGui.glade"
    ROOT_OBJECT = "PhotoOrganizer"
    TREEVIEW_ALBUM = "treeviewAlbum"
    STATUSBAR = "statusbar1"
    LEFTPANEL = "leftPanel"
    NOTEBOOK = "notebook1"
    IMAGE_PANEL = "imagePanel"


class GUIEventsConstants:
    KEY_PRESS = "key_press_event"
    CURSOR_CHANGED =  'cursor-changed'
    BUTTON_PRESS = "button_press_event"
    BUTTON_RELEASE = "button-release-event"
    MOUSE_MOTION = "motion_notify_event"
    DRAWING_AREA_DRAW = "draw"
    RETURN = "Return"
    RIGHT = "Right"
    LEFT = "Left"


class GUIMessageConstants:
    FOLDER_CHOOSE = "Please choose a folder"
    FILE_DIR_CHOOSE = "Select"
    ERROR_NO_PICS = "No pics founded"
    ERROR_NEW_FOLDER = "Specify another folder"

class SizeConstants:
    DIALOG_DEFAULT_SIZE = (800,400)


class ImageConstants:
    PNG_EXT = "PNG"
    RGB_SHORT_NAME = "RGB"