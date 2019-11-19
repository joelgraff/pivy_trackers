import FreeCADGui as Gui

from pivy import coin

from pivy_trackers.trait.base import Base
from pivy_trackers.trait.timer import Timer

class MyTimerTracker(Base, Timer):

    def __init__(self):

        super().__init__('MyTimerTracker', Gui.ActiveDocument.ActiveView)

        self.insert_into_scenegraph(True)

    def on_insert(self):
        """
        Base callback method override, called after insert into scenegraph
        """

        self.add_timer(1.0, 'my timer data')

    def timer_callback(self, data, sensor):

        print('MyTimerTracker.timer_callback sensor data:', data.data)
