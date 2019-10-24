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
Message services for Python object intercommunication
"""

from .publisher import Publisher
from .subscriber import Subscriber
from ..support.message_types import MessageTypes as Messages

class Message(Publisher, Subscriber):
    """
    Message services for Python obeject intercommunication
    """

    def __init__(self):
        """
        Constructor
        """
        
        super().__init__()

    def notify(self, message):
        """
        Generic overridable motification callback
        """

        print(
            '{}.notify() message = {}'.format(self.name, str(message))
        )

    def notify_geometry(self, message):
        """
        Overrideable notification callback for geometry udpates
        """

        print(
            '{}.notify_geometry() message = {}'.format(self.name, str(message))
        )

    def notify_ui(self, message):
        """
        Overrideable notification callback for user interface updates
        """

        print(
            '{}.notify_ui() message = {}'.format(self.name, str(message))
        )

    def register_geometry(self, who, duplex=False):
        """
        Register a python object for geometry messages.
        Must implement notify_geometry()
        Duplex - True = register self and who as subscribers to each other
        """

        self.register(who, Messages.INTERNAL.GEOMETRY, who.notify_geometry)

        if duplex:
            who.register(self, Messages.INTERNAL.GEOMETRY, who.notify_geometry)
    def register_user_interface(self, who, duplex=False):
        """
        Register a python object for geometry messages.
        Must implement notify_geometry()
        Duplex - True = register self and who as subscribers to each other
        """

        self.register(
            who, Messages.INTERNAL.USER_INTERFACE, who.notify_geometry)

        if duplex:
            who.register(
                self, Messages.INTERNAL.USER_INTERFACE, who.notify_geometry)

    def unregister_geometry(self, who):
        """
        Unregister an object from geometry messages
        """

        self.unregister(who, Messages.INTERNAL.GEOMETRY)

    def unregister_user_interface(self, who):
        """
        Unregister an object from user interface messages
        """

        self.unregister(who, Messages.INTERNAL.USER_INTERFACE)
