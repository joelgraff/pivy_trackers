# -*- coding: utf-8 -*-
#***********************************************************************
#*                                                                     *
#* Copyright (c) 2018 Joel Graff <monograff76@gmail.com>               *
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
MessageTypes class
"""

import types

from inspect import getmro

from ..support.const import Const
from ..support.singleton import Singleton

class MessageTypes(metaclass=Singleton):

    class INTERNAL(Const):
        """
        INTERNAL message category
        """

        GEOMETRY = 2
        USER_INTERFACE = 4

    CUSTOM = types.SimpleNamespace()

    @staticmethod
    def create(message_type_name):
        """
        Generate a new custom message type and assign it a value
        """

        _val = 1 + 2 **(len(list(MessageTypes.CUSTOM.keys()))+1)

        setattr(MessageTypes.CUSTOM, message_type_name, _val)
