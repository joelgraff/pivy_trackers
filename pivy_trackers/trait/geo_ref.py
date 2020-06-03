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
Provides SoKeyboardEvent support for tracker classes
"""

from pivy import coin

from ..coin.coin_enums import NodeTypes as Nodes

class GeoRef():
    """
    Provides SoGeo node support
    """

    #Base prototypes
    name = None
    names = []
    base = None

    def __init__(self):
        """
        Constructor
        """
        #Pylint doesn't see self.base members...
        #pylint: disable=no-member

        assert(self.names), """
        Keyboard.__init__(): No names defined.  Is Base inherited?
        """

        assert(self.event), """
        Keyboard.__init__(): No event node defined.  Is Event inherited?
        """

        self.handle_keyboard_events = False
        self.keybaord_event_cb = None
        self.keydown_callbacks = {}
        self.keyup_callbacks = {}

        super().__init__()
