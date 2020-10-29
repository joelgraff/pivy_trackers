# -*- coding: utf-8 -*-
#***********************************************************************
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
Mouse state class
"""

from pivy import coin
from PySide.QtGui import QCursor

from ..support.core.singleton import Singleton
from ..support.core.tuple_math import TupleMath

from ..state.button_state import ButtonState

class MouseState(metaclass=Singleton):
    """
    Class to track the current state of the mouse based on
    passed Coin3D SoEvent parameters
    """

    def __init__(self):
        """
        MouseState construction
        """

        self.screen_position = ()
        self.world_position = ()
        self.prev_position = ()

        self.button1 = ButtonState()
        self.button2 = ButtonState()
        self.button3 = ButtonState()
        self.buttons = [self.button1, self.button2, self.button3]

        self.alt_down = False
        self.ctrl_down = False
        self.shift_down = False

        self.vector = ()

        self.object = None
        self.component = ''

        self.state = [
            self.button1, self.button2, self.button3,
            self.world_position, self.screen_position
        ]

        self.callbacks = []

    def _update_button_state(self, arg, view_state):
        """
        Process mouse clicks
        """

        _btn = self.buttons[int(arg['Button'][-1]) - 1]
        _btn.pressed = arg['State'] == 'DOWN'

        if not _btn.pressed:
            _btn.dragging = False

        _btn.screen_position = self.screen_position
        _btn.world_position = self.world_position

    def _update_state(self, arg, view_state):
        """
        Update the positions and key states
        """

        self.prev_position = self.world_position
        self.screen_position = arg['Position']

        self.world_position = view_state.getPoint(self.screen_position)

        if not self.prev_position:
            self.vector = self.world_position

        else:
            self.vector = TupleMath.subtract(
                self.world_position, self.prev_position)

        self.alt_down = arg['AltDown']
        self.ctrl_down = arg['CtrlDown']
        self.shift_down = arg['ShiftDown']

        #continue drag unless button is released
        if self.button1.dragging:
            self.button1.dragging = self.button1.pressed

        #if button is still pressed and the position has changed,
        #begin drag operation
        elif self.button1.pressed:

            if self.button1.screen_position != self.screen_position:

                self.button1.dragging = True
                self.button1.drag_start = self.button1.world_position

        else:
            self.button1.drag_start = ()

    def _update_component_state(self, info):
        """
        Update the component / object data
        """

        #clear state, no info exists
        if not info:

            self.object = None
            self.component = ''
            return

        self.object = info.get('Object')
        self.component = info.get('Component')

    def update(self, arg, view_state):
        """
        Update the current mouse state
        """

        _arg = arg

        if isinstance(arg, coin.SoEventCallback):
            _evt = arg.getEvent()
            _arg = {
                'Type': _evt.getTypeId().getName().getString(),
                'Time': float(_evt.getTime().getValue()),
                'Position': _evt.getPosition().getValue(),
                'ShiftDown': _evt.wasShiftDown(),
                'AltDown': _evt.wasAltDown(),
                'CtrlDown': _evt.wasCtrlDown()
            }

            if isinstance(_evt, coin.SoMouseButtonEvent):

                _arg['Button'] = 'BUTTON' + str(_evt.getButton())
                _arg['State'] = 'DOWN'

                if not _evt.isButtonPressEvent(_evt, _evt.getButton()):
                    _arg['State'] = 'UP'

        #update position/state information
        self._update_state(_arg, view_state)

        #process button events
        if _arg['Type'] == 'SoMouseButtonEvent':
            self._update_button_state(_arg, view_state)

        #return if dragging to preserve component / object data
        if self.button1.dragging:
            return

        self._update_component_state(
            view_state.getObjectInfo(self.screen_position))

        for _cb in self.callbacks:
            _cb(self)

    def set_mouse_position(self, view_state, coord=None):
        """
        Update the mouse cursor position independently
        coord - position in world coordinates
        """

        if not coord:
            coord = self.world_position

        _new_pos = view_state.getPointOnScreen(coord)

        #set the mouse position at the updated screen coordinate
        _delta = TupleMath.subtract(_new_pos, self.screen_position)

        #get screen position by adding offset to the new window position
        _pos = TupleMath.add((_delta[0], -_delta[1]), QCursor.pos().toTuple())

        QCursor.setPos(_pos[0], _pos[1])

        self.world_position = coord

    def finish(self):
        """
        Cleanup
        """

        self.screen_position = None
        self.world_position = None
        self.prev_position = None

        self.buttons = None

        if self.button1:

            self.button1.finish()
            self.button1 = None

            self.button2.finish()
            self.button2 = None

            self.button3.finish()
            self.button3 = None

        self.alt_down = False
        self.ctrl_down = False
        self.shift_down = False

        self.vector = None

        self.object = None
        self.component = ''

        self.state = None

        Singleton.finish(MouseState)
