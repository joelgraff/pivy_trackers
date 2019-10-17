import FreeCADGui as Gui

from ..tracker.context_tracker import ContextTracker
from ..tracker.marker_tracker import MarkerTracker


class MyMarkerTracker(ContextTracker):

    def __init__(self):

        super().__init__('MyMarkerTracker', Gui.ActiveDocument.ActiveView)

        self.marker_tracker = \
            MarkerTracker('mt', (0.0, 0.0, 0.0), self.base)

        self.set_visibility()

        self.insert_into_scenegraph(True)