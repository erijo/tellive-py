# Copyright (c) 2014 Erik Johansson <erik@ejohansson.se>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import tellcore.constants as const

class TelldusLive(object):
    def __init__(self, client):
        super().__init__()
        self._client = client

    def devices(self, supported_methods=None):
        if supported_methods is None:
            supported_methods = const.TELLSTICK_TURNON \
                | const.TELLSTICK_TURNOFF \
                | const.TELLSTICK_BELL \
                | const.TELLSTICK_TOGGLE \
                | const.TELLSTICK_DIM \
                | const.TELLSTICK_LEARN \
                | const.TELLSTICK_EXECUTE \
                | const.TELLSTICK_UP \
                | const.TELLSTICK_DOWN \
                | const.TELLSTICK_STOP
        params = {'supportedMethods': supported_methods,
                  'extras': 'coordinate,timezone,tzoffset'}
        values = self._client.request("devices/list", params)
        return [Device(self._client, p['id'], p) for p in values['device']]


class Device(object):
    def __init__(self, client, id, params={}):
        super().__init__()
        super().__setattr__('_client', client)
        super().__setattr__('id', id)
        self._update(params)

    def _update(self, params):
        for name in ['name', 'state', 'statevalue']:
            if name in params:
                super().__setattr__(name, params[name])

    def __getattr__(self, name):
        for attempt in range(2):
            try:
                return self.__dict__[name]
            except KeyError:
                if attempt == 0:
                    self.refresh()
                    continue
                raise AttributeError(name) from None

    def refresh(self, supported_methods=None):
        if supported_methods is None:
            supported_methods = const.TELLSTICK_TURNON \
                | const.TELLSTICK_TURNOFF \
                | const.TELLSTICK_BELL \
                | const.TELLSTICK_TOGGLE \
                | const.TELLSTICK_DIM \
                | const.TELLSTICK_LEARN \
                | const.TELLSTICK_EXECUTE \
                | const.TELLSTICK_UP \
                | const.TELLSTICK_DOWN \
                | const.TELLSTICK_STOP
        params = {'id': self.id, 'supportedMethods': supported_methods,
                  'extras': 'coordinate,timezone,tzoffset'}
        values = self._client.request("device/info", params)
        self._update(values)

    def turn_on(self):
        params = {'id': self.id}
        self._client.request("device/turnOn", params)

    def turn_off(self):
        params = {'id': self.id}
        self._client.request("device/turnOff", params)

    def last_sent_command(self):
        return self.state

    def last_sent_value(self):
        return self.statevalue
