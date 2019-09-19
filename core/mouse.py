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
Mouse services for Tracker objects
"""

class Mouse():
    """
    Mouse services for Tracker objects
    """

    #view_state is provided in Base
    view_state = None

    def __init__(self):
        """
        Constructor
        """

        if not self.view_state:
            return

        self.mouse_cb = self.view_state.addEventCallback(
            'SoLocation2Event', self.mouse_event)

        self.button_cb = self.view_state.addEventCallback(
            'SoMouseButtonEvent', self.button_event)

        super().__init__()

    def mouse_event(self, arg):
        """
        Base mouse event implementation
        """

        pass

    def button_event(self, arg):
        """
        Base button event implementation
        """

        pass
