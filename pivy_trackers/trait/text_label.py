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
Font / Text graph class for label-style text
"""

from types import SimpleNamespace

from collections.abc import Iterable
from ..support.tuple_math import TupleMath

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin import coin_utils as utils

class TextLabel:
    """
    Font / Text graph class for label-style text
    """

    def __init__(
        self, text, name=None, has_transform=True, has_font=True, parent=None):
        """
        Constructor

        trait_name - Name of trait.  Assumed 'label' and indexed if already
        exists in parent
        """

        _idx = 1
        _index = ''

        if name is None:
            name = ''

        _name = name + '__LABEL'

        while hasattr(self, _name + _index):
            _index = str(_idx)
            _idx += 1

        _name += str(_index)

        self.offset = (0.0, 0.0, 0.0)
        self.font = None
        self.transform = None

        self.group = CoinGroup(
            is_separated=True, is_switched=False, switch_first=False,
            parent=parent, name=_name)

        if has_transform:
            self.transform = self.group.add_node(Nodes.TRANSFORM)

        if has_font:
            self.font = self.group.add_node(Nodes.FONT)
            print('setting font...')
            self.set_font('', '', 100.0)

        self.text = self.group.add_node(Nodes.TEXT)
        self.set_text(text)

        super().__init__()

    def set_size(self, size):
        """
        Set the size of the text
        """

        if self.font:
            self.font.size.setValue(size)

    def get_size(self):
        """
        Get the size of the text
        """

        if self.font:
            return self.font.size.getValue()

        return -1.0

    def set_text(self, text):
        """
        Set the node text.
        Text - string or an iterable
        """

        if isinstance(text, str):
            self.text.string.setValue(text)
        
        elif isinstance(text, Iterable):
            self.text.string.setValues(0, len(text), text)

    def get_text(self):
        """
        Return the text stored in the text.string attribute as a string
        or iterable of strings
        """

        _result = self.text.string.getValues()

        if len(_result) == 1:
            _result = result[0]

        return _result

    def set_font(self, font_name, font_style, font_size):
        """
        Set the font based on the passed name

        font_name - string name of the font installed on the system
        font_style - style of the font (see coin_enums.FontStyles)
        font_size - font size in screen pixels (integer or float)
        """

        if not self.font:
            return

        self.font.name.setValue(font_name)
        self.font.size.setValue(font_size)

    def get_font(self):
        """
        Return the current font, style, and size as a SimpleNamespace
        """

        _result = SimpleNamespace(name='', style='', size=-1.0)

        if not self.font:
            return _result

        _name = self.font.name.getValue().split(':')
        
        _result.name = _name[0]

        if len(_name) == 2:
            _result.style = _name[1]

        _result.size = self.font.size.getValue()

        return _result

    def get_translation(self):
        """
        Return the translation of the text object
        """

        if not self.transform:
            return ()

        return self.transform.translation.getValue()
    
    def set_translation(self, translation):
        """
        Set the translation of the text object as a 3-coordiante tuple
        """

        if self.transform:
            _xlate = TupleMath.add(translation, self.offset)
            self.transform.translation.setValue(_xlate)

    def set_rotation(self, angle, center=None):
        """
        Set the rotation angle of the label
        """

        print('setting rotation', angle)

        if not self.transform:
            return

        _rot = utils.get_rotation(angle)

        print('rotation quat:', _rot.getValue())
        self.transform.rotation = _rot

        print(self.transform.rotation.getValue().getValue())
        print(self.transform.center.getValue().getValue())

        if center is not None:
            self.transform.rotation.center.setValue(center)

    def get_rotation(self):
        """
        Get the rotation angle of the label
        """

        _result = self.transform.rotation.getValue().getAxisAngle()

        return [_result[0].getValue(), _result[1]]