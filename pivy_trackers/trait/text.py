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
from support.tuple_math import TupleMath

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_text import CoinText
from ..coin import coin_utils as utils

class Text():
    """
    Font / Text graph class for label-style text
    """

    #prototypes
    base = None
    name = ''

    def __init__(self):
        """
        Constructor

        trait_name - Name of trait.  Assumed 'label' and indexed if already
        exists in parent
        """

        CoinText
        _idx = 1
        _index = ''

        self.text = None
        self.text_base = None
        self.text_nodes = []
        self.text_offset = (0.0, 0.0, 0.0)
        self.text_center = (0.0, 0.0, 0.0)

        super().__init__()

    def _add_top_node(self):
        """
        Add the top node to the node graph on-demand
        """

        _base = self.text_base
        _name = self.name + '_TEXT_GROUP'

        if _base is None:
            _base = self.base

        self.text = CoinGroup(
            is_separated=True, is_switched=False, parent=_base, name=_name)

        self.text.transform = self.text.add_node(Nodes.TRANSFORM)
        self.text.font = self.text.add_node(Nodes.FONT)

    def add_text(
        self, name=None, text=None, has_transform=False, has_font=False):
        """
        Add a new text nodegraph
        """

        if self.text is None:
            self._add_top_node()

        self.text.text = CoinText(
            self.name + '_TEXT', text, has_transform, has_font, self.text.top)

        self.text_nodes.append(self.text.text)

    def set_text_size(self, size):
        """
        Set the size of the text
        """

        if self.text.font:
            self.text.font.size.setValue(size)

    def get_text_size(self):
        """
        Get the size of the text
        """

        if self.text.font:
            return self.text.font.size.getValue()

        return -1.0

    def set_text(self, text):
        """
        Set the node text.
        Text - string or an iterable
        """

        if isinstance(text, str):
            node.string.setValue(text)
        
        elif isinstance(text, Iterable):
            node.string.setValues(0, len(text), text)

    def get_text(self):
        """
        Return the text stored in the text.string attribute as a string
        or iterable of strings
        """

        _result = self.text.string.getValues()

        if len(_result) == 1:
            _result = result[0]

        return _result

    def set_text_font(self, font_node, font_name, font_style, font_size):
        """
        Set the font based on the passed name

        font_name - string name of the font installed on the system
        font_style - style of the font (see coin_enums.FontStyles)
        font_size - font size in screen pixels (integer or float)
        """

        font_node.name.setValue(font_name)
        font_node.size.setValue(font_size)

    def get_text_font(self):
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

    def set_text_matrix(self, matrix):
        """
        Set the matrix for the CoinText node
        """

        self.text.set_matrix(matrix)

    def get_text_matrix(self):
        """
        Return the matrix transformation on the text node
        """

        return self.view_state.get_matrix(self.text.text)

    def get_text_translation(self):
        """
        Return the translation of the text object
        """

        if not self.text.transform:
            return ()

        return self.text.transform.translation.getValue()

    def set_text_translation(self, translation, accumulate = False):
        """
        Set the translation, overriding existing unless accumulate=True
        """

        if not self.text or not self.text.transform:
            return

        _xlate = TupleMath.add(
            [translation, self.text_offset, self.text_center]
        )

        if accumulate:
            _xlate = TupleMath.add(self.get_text_translation(), _xlate)

        self.text.transform.translation.setValue(_xlate)

    def set_text_rotation(self, angle, center=None):
        """
        Set the rotation angle of the label
        """

        if not self.text.transform:
            return

        _rot = utils.get_rotation(angle)

        self.text.transform.rotation = _rot

        if center is not None:
            self.text.transform.rotation.center.setValue(center)

    def get_text_rotation(self):
        """
        Get the rotation angle of the label
        """

        _result = self.text.transform.rotation.getValue().getAxisAngle()

        return [_result[0].getValue(), _result[1]]
