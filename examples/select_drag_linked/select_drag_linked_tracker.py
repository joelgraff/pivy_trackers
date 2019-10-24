
from ...trait.base import Base

from ...tracker.marker_tracker import MarkerTracker
from ...tracker.line_tracker import LineTracker

class SelectDragLinkedTracker(Base):

    def __init__(self, view):
        """
        Constructor
        """

        super().__init__(name='linked_tracker', view=view)

        self.marker_trackers = [
            MarkerTracker('marker_1', (-100.0, -100.0, 0.0), self.base),
            MarkerTracker('marker_2', (100.0, 100.0, 0.0), self.base)
        ]

        self.line_tracker = LineTracker('line', [
            self.marker_trackers[0].point,
            self.marker_trackers[1].point],
            self.base
        )

        self.set_visibility()

    def finalize(self, node=None, parent=None):
        """
        Cleanup the tracker
        """

        for _t in self.marker_trackers:
            _t.finalize()

        self.line_tracker.finalize()

        super().finalize(node, parent)
