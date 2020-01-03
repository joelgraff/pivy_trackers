import FreeCADGui as Gui

from ..tracker.context_tracker import ContextTracker
from ..tracker.line_tracker import LineTracker

class CoordReset(ContextTracker):

    def __init__(self):

        super().__init__('MyTracker', Gui.ActiveDocument.ActiveView)

        _list = [(0.0, 0.0, 0.0), (10.0, 10.0, 0.0), (-10.0, 10.0, 0.0), (-10.0, -10.0, 0.0), (10.0, -10.0, 0.0)]

        self.line_tracker = LineTracker('lt', _list, self.base)

        self.set_visibility()

        self.insert_into_scenegraph(True)

    def reset(self):
        """
        Reset
        """

        self.line_tracker.geometry.coordinate.point.setValue([1,1,0])

    def rebuild(self):
        _list = [(0.0, 0.0, 0.0), (0.0, 10.0, 0.0), (-10.0, 0.0, 0.0), (0.0, -10.0, 0.0), (10.0, 0.0, 0.0)]

        self.line_tracker = LineTracker('lt', _list, self.base)
