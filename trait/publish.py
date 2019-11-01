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
Publish base class
"""

from collections.abc import Iterable

class Publish():
    """
    Base class for publisher classes
    """

    counter = 0
    name = 'Publish'

    def __init__(self):
        """
        Constructor
        """

        self.pub_id = Publish.counter
        self.event_callbacks = {}
        self.excluded_subscribers = []

        Publish.counter += 1

        super().__init__()

    def get_subscribers(self, events=None):
        """
        Return subscribers registered for selected event
        """

        _result = []

        #no events specified returns all subscribers
        if not events:

            for _e in self.event_callbacks:
                _result += _e.values()

            return _result

        if not isinstance(events, list):
            events = [events]

        for _e in events:

            _subs = self.event_callbacks.get(_e)

            #filter excluded subscribers
            if _subs:

                _result += [
                    _c for _s, _c in _subs.items()\
                        if _s not in self.excluded_subscribers
                ]

        return _result

    def register(self, who, events, callback=None):
        """
        Callback registration for subscribers
        """

        #A subscriber is registered for an event by storing a reference to the
        #subscriber under the index value of the event. No checks are performed
        #to ensure the event is a valid publisher event.

        if who is self:
            return

        if not isinstance(events, list):
            events = [events]

        if not callback:
            callback = getattr(who, 'notify')

        for _e in events:

            #new event in the dictionary
            if not _e in self.event_callbacks:

                self.event_callbacks[_e] = {who: callback}
                continue

            #new subscriber for and existing event
            if who not in self.event_callbacks[_e]:
                self.event_callbacks[_e][who] = callback

    def unregister(self, who, events):
        """
        Callback unregistration for subscribers
        """

        for _e in events:

            #no event, no subscriber
            if not _e in self.event_callbacks:
                continue

            #subscribver not found for event
            if who not in self.event_callbacks[_e]:
                continue

            #delete and remove empty event, if necessary
            del self.event_callbacks[_e][who]

            if not self.event_callbacks[_e]:
                del self.event_callbacks[_e]

    def dispatch(self, message, event=None, verbose=False):
        """
        Message dispatch
        """

        #don't send empty messages
        if not message:
            return

        _cb_list = self.get_subscribers(event)

        if verbose:
            print('\n{} (#{}): dispatching message \n{}\n'\
                .format(self.name, self.pub_id, message))

        for _cb in _cb_list:
            _cb(event, message)

    def finish(self):
        """
        Cleanup
        """

        Publish.counter = 0
        self.event_callbacks = {}
        self.excluded_subscribers = []
