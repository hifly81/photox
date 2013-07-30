# coding: latin-1

'''
Created on Jul 25, 2013

@author: hifly
'''


class DateTimeConstants:
    MONTH_SHORTCUT = "%B"
    FULL_DATE_US_SHORTCUT = "%a %b %d %H:%M:%S %Y"


class LoggerConstants:
    DEFAULT_LOGGER_NAME = "photoOrganizer"
    DEFAULT_LOGGING_CONF = "config/logging.conf"


class GladeConstants:
    MAIN_GUI_FILE = "glade/photoOrganizerGui.glade"
    ROOT_OBJECT = "PhotoOrganizer"
    TREEVIEW_ALBUM = "treeviewAlbum"
    STATUSBAR = "statusbar1"
    LEFTPANEL = "leftPanel"
    NOTEBOOK = "notebook1"
    IMAGE_PANEL = "imagePanel"
    EFFECTS_SUB_MENU = "submainFunctionalitiesMenu"
    ACTION_GROUP = "my_actions"
    POPUP_MENU = "/PopupMenu"


class GUIEventsConstants:
    KEY_PRESS = "key_press_event"
    CURSOR_CHANGED =  'cursor-changed'
    BUTTON_PRESS = "button_press_event"
    BUTTON_RELEASE = "button-release-event"
    BUTTON_CLICKED = "clicked"
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
    SAVE_IMAGE = "Save your image"
    UNTITLED_DOC = "Untitled document"
    ALL_FILES = "All files"

class GUIWidgetConstants:
    BUTTON_ROTATE_RIGHT = "Rotate Right"
    BUTTON_ROTATE_LEFT = "Rotate Left"
    BUTTON_MIRROR = "Mirror"
    BUTTON_FLIP = "Flip"
    BUTTON_CROP = "Crop"
    BUTTON_RESIZE = "Resize"
    BUTTON_SHARPNESS = "Sharpness"
    BUTTON_DEFORM = "Deform"
    BUTTON_BORDER = "Border"
    BUTTON_UNBORDER = "Unborder"
    BUTTON_POLAROID = "Polaroid"
    BUTTON_FRAME = "Frame"
    BUTTON_WATERMARK = "Watermark"
    BUTTON_HISTOGRAM = "Histogram"
    BUTTON_DETAIL = "Detail"
    BUTTON_ORIGINAL_SIZE = "Original size"
    BUTTON_TAG_PEOPLE = "Tag people"
    BUTTON_WEBCAM = "Webcam"
    BUTTON_GRAB_DESKTOP = "Grab desktop"

class SizeConstants:
    DIALOG_DEFAULT_SIZE = (800,400)


class ImageConstants:
    PNG_EXT = "PNG"
    RGB_SHORT_NAME = "RGB"
    IMAGE_MODE_L = "L"