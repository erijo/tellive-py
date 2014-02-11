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

import http.client as http
import json
import logging
import oauthlib.oauth1
import urllib.parse

class TelldusLiveError(Exception):
    def __init__(self, error):
        super().__init__(error)


class LiveClient(object):
    def __init__(self, public_key, private_key, server='api.telldus.com',
                 port=http.HTTP_PORT, access_token=None, access_secret=None):
        super().__init__()
        self.public_key = public_key
        self.private_key = private_key
        self.server = server
        self.port = port
        self.host = "http://{}".format(server)
        if port != http.HTTP_PORT:
            self.host += ":{}".format(port)
        self.token = access_token
        self.secret = access_secret

    def _request(self, path, token, secret):
        client = oauthlib.oauth1.Client(
            self.public_key, client_secret=self.private_key,
            resource_owner_key=token, resource_owner_secret=secret)

        uri, headers, body = client.sign(self.host + path)
        conn = http.HTTPConnection(self.server, self.port)
        conn.request('GET', path, body=body, headers=headers)

        response = conn.getresponse()
        if response.status != http.OK:
            raise RuntimeError(
                "Could not get {} from {}:{}: {} {}".format(
                    path, self.server, self.port, response.status,
                    response.reason))
        return response

    def _token(self, path, token=None, secret=None):
        response = self._request(path, token, secret)
        qs = urllib.parse.parse_qs(response.read().decode('utf-8'))
        return qs['oauth_token'][0], qs['oauth_token_secret'][0]

    def request_token(self):
        """ Returns url, request_token, request_secret"""
        logging.debug("Getting request token from %s:%d",
                      self.server, self.port)
        token, secret = self._token("/oauth/requestToken")
        return "{}/oauth/authorize?oauth_token={}".format(self.host, token), \
            token, secret

    def access_token(self, request_token, request_secret):
        """Returns access_token, access_secret"""
        logging.debug("Getting access token from %s:%d",
                      self.server, self.port)
        self.access_token, self.access_secret = \
            self._token("/oauth/accessToken", request_token, request_secret)
        return self.access_token, self.access_secret

    def request(self, method, params):
        path = "/json/{}?{}".format(method, urllib.parse.urlencode(params))
        response = self._request(path, self.token, self.secret)
        values = json.loads(response.read().decode('utf-8'))
        if 'error' in values:
            raise TelldusLiveError(values['error'])
        return values
