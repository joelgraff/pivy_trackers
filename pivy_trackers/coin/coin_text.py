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
Class for creating Coin3D text node structures
"""

from collections.abc import Iterable

from . import coin_utils as utils
from .coin_enums import NodeTypes as Nodes

class CoinText(object):
    """
    Class for creating Coin3D text node structures
    """

    def __init__(
        self, name, text, has_font=False, has_transform=False, parent=None):
        """
        Constructor
        """

        self.name = name + '_TEXT_NODE'
        self.root = utils.add_child(Nodes.SEPARATOR, None, self.name)
        self.top = self.root

        self.offset = (0.0, 0.0, 0.0)

        self.transform = None
        self.font = None
        self.text = None

        if has_transform:
            self.transform = utils.add_child(
                Nodes.TRANSFORM, self.top, self.name + '_TRNSFORM')

        if has_font:
            self.font = utils.add_child(
                Nodes.FONT, self.top, self.name + '_FONT')

            self.set_font(_group.font, '', '', 100.0)

        self.text = utils.add_child(
            Nodes.TEXT, self.top, self.name + '_TEXT')

        if parent:
            utils.insert_child(self.text, parent)

        self.set_text(text)

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
            _result = _result[0]

        return _result

    def set_font(self, font_style, font_size):
        """
        Set the font based on the passed name

        font_name - string name of the font installed on the system
        font_style - style of the font (see coin_enums.FontStyles)
        font_size - font size in screen pixels (integer or float)
        """

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

    def set_matrix(self, matrix):
        """
        Apply matrix to the transform node
        """

        self.transform.setMatrix(matrix)

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

        if not self.transform:
            return

        _rot = utils.get_rotation(angle)

        self.transform.rotation = _rot

        if center is not None:
            self.transform.rotation.center.setValue(center)

    def get_rotation(self):
        """
        Get the rotation angle of the label
        """

        _result = self.transform.rotation.getValue().getAxisAngle()

        return [_result[0].getValue(), _result[1]]
