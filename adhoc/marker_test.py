import FreeCADGui as Gui
import DraftTools

from ..tracker.base_tracker import BaseTracker
from ..tracker.marker_tracker import MarkerTracker


class MyMarkerTracker(BaseTracker):

    def __init__(self):

        super().__init__('MyMarkerTracker', Gui.ActiveDocument.ActiveView)

        self.marker_tracker = \
            MarkerTracker('mt', (0.0, 0.0, 0.0), self.base)

        self.set_visibility()

        self.insert_into_scenegraph(True)