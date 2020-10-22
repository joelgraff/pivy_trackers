import FreeCADGui as Gui

from pivy_trackers.coin import coin_utils as utils
from pivy_trackers.examples.select_drag.select_drag_tracker import SelectDragTracker

def dump_graph():

    utils.dump_node(Gui.ActiveDocument.ActiveView.getSceneGraph())

def gen_tracker():

    _t = SelectDragTracker(Gui.ActiveDocument.ActiveView)
    _t.insert_into_scenegraph()

    return _t

def generate():

    print ('\n################# BEFORE ################\n')
    dump_graph()

    return gen_tracker()

def finish(tracker):

    tracker.finish()

    print ('\n################ AFTER #################\n')
    dump_graph()