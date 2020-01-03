# -*- coding: utf-8 -*-
#***********************************************************************
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

class SelectDragTracker(ContextTracker, Drag):
    """
    Select Drag Tracker example
    """

    def __init__(self, view, is_linked=False, has_markers=True):
        """
        Constructor
        """

        super().__init__(
            name='document.object.select_drag_linked_tracker', view=view)

        #generate initial node trackers and wire trackers for mouse interaction
        #and add them to the scenegraph
        self.lines = []
        self.markers = []
        self.build_trackers(is_linked, has_markers)

        self.set_visibility(True)

    def build_trackers(self, is_linked, has_markers):
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

        _prev = _model[0]

        if has_markers:
            self.build_markers(_model)

        self.build_lines(_model)

        if not is_linked:
            return

        if has_markers:
            self.link_markers()

        else:
            self.link_lines()

    def build_lines(self, model):
        """
        Build line trackers
        """

        #create the line trackers
        for _i, _v in enumerate(model):

            if _i > 0:
                self.lines.append(
                    LineTracker(
                        name='LINE-' + str(_i),
                        points=[_prev, _v],
                        parent=self.base
                    )
                )

            _prev = _v

        #connect back to the start
        self.lines.append(
            LineTracker(
                name='LINE-4', points=[model[3], model[0]], parent=self.base)
        )

    def build_markers(self, model):
        """
        Build marker trackers
        """

        #create the marker trackers
        for _i, _v in enumerate(model):

            self.markers.append(
                MarkerTracker(
                    name='MARKER-' + str(_i),
                    point=_v,
                    parent=self.base
                )
            )

    def link_lines(self):
        """
        Link lines to each other
        """

        _model = [
            (100.0, 100.0, 0.0),
            (-100.0, 100.0, 0.0),
            (-100.0, -100.0, 0.0),
            (100.0, -100.0, 0.0)
        ]

        self.lines[0].link_geometry(self.lines[1], 1, 0)
        self.lines[0].link_geometry(self.lines[3], 0, 1)
        self.lines[1].link_geometry(self.lines[2], 1, 0)
        self.lines[2].link_geometry(self.lines[3], 1, 0)

    def link_markers(self):
        """
        Link markes to lines
        """

        #link the nodes with their corresponding lines.
        _idx = 0

        for _v in self.lines:

            _v.link_marker(self.markers[_idx], 0)
            _idx += 1

            if _idx > 3:
                _idx = 0

            _v.link_marker(self.markers[_idx], 1)


    def finish(self, node=None, parent=None):
        """
        Cleanup the tracker
        """

        for _t in self.trackers:
            _t.finalize()

        ContextTracker.finish(self)
        Drag.finish(self)
