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
Widget updating services
"""

from ..support.message_types import MessageTypes as Messages

from .publish import Publish
from .subscribe import Subscribe

from ..support import message_data

class Widget():
    """
    Widget updating services
    """

    @staticmethod
    def formatter_default(widget):
        """
        Default formatter function
        """

        return widget.text()

    def __init__(self):
        """
        Constructor
        """
        
        super().__init__()

        self.trackers = {}
        self.widgets = {}
        self.formatters = {}

    def add_widget(self, widget, tracker):
        """
        Add a widget keyed to the tracker
        """

        if not self.widgets.get(tracker):
            self.widgets[tracker] = []

        self.widgets[tracker].append(widget)

    def add_formatter(self, widget, formatter=Widget.formatter_default)
        """
        Add a widget and corresponding formatter function
        """

        _cb = (lambda wdg: lambda: self.widget_updated(wdg))(widget)
        widget.editing_finished.connect(_cb)

        self.formatters[widget] = formatter

    def notify(self, event, message):
        """
        Update the widget
        """

        if event != Messages.INTERNAL._GEOMETRY:
            self.trackers[message.sender]

        _widget = self.widgets[message.sender]

        self.widgets.setText(self.formatters[_widget](_widget))

    def widget_updated(self, widget):
        """
        Callback for widget signals for updates
        """

        #Override in inheriting class


    def finish(self):
        """
        Cleanup
        """

        Publish.finish(self)
        Subscribe.finish(self)
        Messages.finish(Messages)
