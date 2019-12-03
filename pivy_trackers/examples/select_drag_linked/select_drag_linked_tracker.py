# -*- coding: utf-8 -*-
#**************************************************************************
#*                                                                     *
#* Copyright (c) 2019 Joel Graff <monograff76@gmail.com>               *
#*                                                                     *
#* This program is free software; you can redistribute it and/or modify*
#* it under the terms of the GNU Lesser General Public License (LGPL)  *
#* as published by the Free Software Foundation; either version 2 of   *
#* the License, or (at your option) any later version.                 *
#* for detail see the LICENCE text file.                               *
#*                                                                     *
#* This program is distributed in the hope that it will be useful,     *
#* but WITHOUT ANY WARRANTY; without even the implied warranty of      *
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       *
#* GNU Library General Public License for more details.                *
#*                                                                     *
#* You should have received a copy of the GNU Library General Public   *
#* License along with this program; if not, write to the Free Software *
#* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
#* USA                                                                 *
#*                                                                     *
#***********************************************************************
"""
Example selection / dragging tracker
"""

from ...tracker.context_tracker import ContextTracker
from ...tracker.marker_tracker import MarkerTracker
from ...tracker.line_tracker import LineTracker

from ...trait.drag import Drag

class SelectDragLinkedTracker(ContextTracker, Drag):
    """
    Select Drag Tracker example
    """

    def __init__(self, view):
        """
        Constructor
        """

        super().__init__(name='dcoument.object.select_drag_linked_tracker', view=view)

        #generate initial node trackers and wire trackers for mouse interaction
        #and add them to the scenegraph
        self.trackers = []
        self.build_trackers()

        self.set_visibility(True)

    def build_trackers(self):
        """
        Build the node and wire trackers that represent the selectable
        portions of the alignment geometry
        """

        #a data model of four tuples, defining the corners of a box
        _model = [
            (100.0, 100.0, 0.0),
            (-100.0, 100.0, 0.0),
            (-100.0, -100.0, 0.0),
            (100.0, -100.0, 0.0)
        ]

        #create the marker trackers
        for _i, _v in enumerate(_model):

            self.trackers.append(
                MarkerTracker(
                    name='MARKER-' + str(_i),
                    point=_v,
                    parent=self.base
                )
            )

        _prev = _model[0]

        #create the line trackers
        for _i, _v in enumerate(_model):

            if _i > 0:
                self.trackers.append(
                    LineTracker(
                        name='LINE-' + str(_i),
                        points=[_prev, _v],
                        parent=self.base
                    )
                )

            _prev = _v

        #connect back to the start
        self.trackers.append(
            LineTracker(
                name='LINE-4', points=[_model[3], _model[0]], parent=self.base)
        )

        #link the nodes with their corresponding lines.
        _tracker_idx = 0

        for _v in self.trackers[4:8]:
            _v.link_marker(self.trackers[_tracker_idx], 0)

            _tracker_idx += 1

            if _tracker_idx > 3:
                _tracker_idx = 0

            _v.link_marker(self.trackers[_tracker_idx], 1)

    def finish(self, node=None, parent=None):
        """
        Cleanup the tracker
        """

        for _t in self.trackers:
            _t.finalize()

        ContextTracker.finish(self)
        Drag.finish(self)
