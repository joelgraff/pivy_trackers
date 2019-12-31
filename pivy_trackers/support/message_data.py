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
Message data class for the Message trait
"""

from ..support.message_types import MessageTypes as Messages

def geometry_message(sender, data):
    """
    Factory method for geometry message types
    """

    return MessageData(sender, Messages.INTERNAL._GEOMETRY, data)

def ui_message(sender, data):
    """
    Factory method for widget message types
    """

    return MessageData(sender, Messages.INTERNAL._WIDGET, data)

class MessageData():
    """
    Message data class for the Message trait
    """

    def __init__(self, sender, message_type, data):
        """
        Constructor
        """

        self.sender = sender
        self.message_type = message_type
        self.data = data

    def __str__(self):
        """
        Stringify
        """

        _type = self.message_type

        if not isinstance(_type, list):
            _type = [_type]

        _type = '[' + ', '.join([Messages.NAMES[_v] for _v in _type]) + ']'

        return 'sender: {}\ntype(s): {}\ndata: {}'\
            .format(
                self.sender.name,
                _type,
                str(self.data)
            )

    def __repr__(self):
        """
        Repr
        """

        return self.__str__()
