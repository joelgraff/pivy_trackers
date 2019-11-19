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
Timer support for tracker objects
"""

from pivy import coin

class Timer():
    """
    Timer support for tracker objects
    """

    class TimerSensor(coin.SoTimerSensor):
        """
        Custom override to provide callback and id attributes
        """

        def __init__(self, timer_id, data, interval, schedule, callback=None):
            """
            Constructor
            """

            self.data = data
            self.id = timer_id

            _cb = callback

            if not _cb:
                _cb = lambda x, y: print('default timer callback')

            super().__init__(_cb, self)

            self.setInterval(interval)

            if schedule:
                self.schedule()

    def __init__(self):
        """
        Constructor
        """

        self.timers = {}

        super().__init__()

    def add_timer(self, interval, data,
                  callback=None, timer_id=None, start=True):

        """
        Add a timer to the dict of the specified duration.
        Optional id for retrieval
        """

        if timer_id is None:
            timer_id = str(len(self.timers))

        _cb = callback

        if _cb is None:
            _cb = self.timer_callback

        self.timers[timer_id] =\
            Timer.TimerSensor(timer_id, data, interval, start, _cb)

    def timer_callback(self, data, sensor):
        """
        Default callback to override
        """

        TimerSensor.default_callback(data, sensor)

    def remove_timer(self, timer_id):
        """
        Remove an existing timer
        """

        if not self.timers.get(timer_id):
            return

        del(self.timers[timer_id])

    def stop_timer(self, timer_id):
        """
        Stop a running timer
        """

        _t = self.timers.get(timer_id)

        if not _t or not _t.isScheduled():
            return

        _t.unschedule()

    def start_timer(self, timer_id):
        """
        Start an existing (stopped) timer
        """

        _t = self.timers.get(timer_id)

        if not _t or _t.isScheduled():
            return

        _t.schedule()

    def finish(self):
        """
        Cleanup
        """

        for _t in self.timers:
            del _t

        self.timers.clear()
