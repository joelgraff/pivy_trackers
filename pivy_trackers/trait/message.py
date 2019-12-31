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
Message services for Python object intercommunication
"""

from ..support.message_types import MessageTypes as Messages

from .publish import Publish
from .subscribe import Subscribe

from ..support import message_data

class Message(Publish, Subscribe): # lgtm[py/missing-call-to-init] lgtm[py/conflicting-attributes]
    """
    Message services for Python object intercommunication
    """

    def __init__(self):
        """
        Constructor
        """
        
        self.is_valid_notify = False
        self.ignore_notify = False

        super().__init__()

    def dispatch_geometry(self, data, verbose=False):
        """
        Dispatch a geometry update using the passed data
        """

        self.dispatch(
            message_data.geometry_message(self, data),
            Messages.INTERNAL._GEOMETRY, verbose
        )

    def dispatch_widget(self, data, verbose=False):
        """
        Dispatch a widget update using the passed data
        """

        _message = data

        if not isinstance(data, message_data.MessageData):
            _message = message_data.ui_message(self, data)

        self.dispatch(_message, Messages.INTERNAL._WIDGET, verbose)

    def notify(self, event, message):
        """
        Generic overridable motification callback
        """

        #invalid if ignoring notifications
        self.is_valid_notify = not self.ignore_notify

        #abort if receiving it's own message
        if self.is_valid_notify:
            self.is_valid_notify = message.sender is not self

        print(
            '{}.notify() - valid? {} - message = \n{}\n'.format(self.name, str(self.is_valid_notify), str(message))
        )

    def notify_geometry(self, event, message):
        """
        Overridable notification callback for geometry updates
        """

        self.notify(event, message)

    def notify_widget(self, event, message):
        """
        Overridable notification callback for user interface updates
        """

        print(
            '{}.Message.notify_widget() message = {}'.format(self.name, str(message))
        )

    def register_geometry(self, who, duplex=False):
        """
        Register a python object for geometry messages.
        Must implement notify_geometry()
        Duplex - True = register self and who as subscribers to each other
        """

        self.register(who, Messages.INTERNAL._GEOMETRY, who.notify_geometry)

        if duplex:
            who.register(
                self, Messages.INTERNAL._GEOMETRY, self.notify_geometry)

    def register_widget(self, who, duplex=False):
        """
        Register a python object for geometry messages.
        Must implement notify_geometry()
        Duplex - True = register self and who as subscribers to each other
        """

        self.register(
            who, Messages.INTERNAL._WIDGET, who.notify_geometry)

        if duplex:
            who.register(
                self, Messages.INTERNAL._WIDGET, self.notify_geometry)

    def unregister_geometry(self, who):
        """
        Unregister an object from geometry messages
        """

        self.unregister(who, Messages.INTERNAL._GEOMETRY)

    def unregister_widget(self, who):
        """
        Unregister an object from user interface messages
        """

        self.unregister(who, Messages.INTERNAL._WIDGET)

    def finish(self):
        """
        Cleanup
        """

        Publish.finish(self)
        Subscribe.finish(self)
        Messages.finish(Messages)
