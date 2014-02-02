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

from .livemessage import LiveMessage

import http.client as http
import logging
import socket
import ssl
import xml.parsers.expat as expat


class TellstickLiveClient(object):
    # dict(supportedMethods)
    SUBJECT_REGISTERD = "registered"
    # dict(uuid, url)
    SUBJECT_NOT_REGISTERED = "notregistered"
    # dict(id, action, [value, ACK])
    SUBJECT_COMMAND = "command"
    # <no parameters>
    SUBJECT_PONG = "pong"
    # <no parameters>
    SUBJECT_DISCONNECT = "disconnect"

    def __init__(self, public_key, private_key):
        super(TellstickLiveClient, self).__init__()
        self.socket = None
        self.public_key = public_key
        self.private_key = private_key
        self.hash_method = "sha1"

    def ssl_context(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_REQUIRED
        context.set_default_verify_paths()
        return context

    def servers(self, server='api.telldus.com', port=http.HTTPS_PORT):
        """Fetch list of servers that can be connected to.

        :return: list of (address, port) tuples
        """
        logging.debug("Fetching server list from %s:%d", server, port)

        conn = http.HTTPSConnection(server, port, context=self.ssl_context())
        conn.request('GET', "/server/assign?protocolVersion=2")

        response = conn.getresponse()
        if response.status != http.OK:
            raise ConnectionError("Could not connect to {}:{}: {} {}".format(
                    server, port, response.status, response.reason))

        servers = []

        def extract_servers(name, attributes):
            if name == "server":
                servers.append((attributes['address'],
                                int(attributes['port'])))

        parser = expat.ParserCreate()
        parser.StartElementHandler = extract_servers
        parser.ParseFile(response)

        logging.debug("Found %d available servers", len(servers))
        return servers

    def connect(self, address, timeout=5):
        sock = self.ssl_context().wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sock.settimeout(timeout)
        sock.connect(address)
        ssl.match_hostname(sock.getpeercert(), address[0])
        self.socket = sock

    def connect_to_first_available_server(self, **kwargs):
        for server in self.servers():
            try:
                logging.debug("Connecting to %s:%d", server[0], server[1])
                self.connect(server, **kwargs)
                return server
            except:
                pass
        raise ConnectionError("Could not connect to any available server")

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send_message(self, message):
        envelope = message.create_signed_message(
            self.private_key, self.hash_method)

        data = envelope.serialize()
        logging.debug("Sending: %s", data)
        self.socket.write(data)

    def receive_message(self):
        data = self.socket.read(1024)
        logging.debug("Received: %s", data)

        envelope = LiveMessage.deserialize(data)
        if not envelope.verify_signature(self.private_key, self.hash_method):
            raise ValueError("Signature verification failed")

        return LiveMessage.deserialize(envelope.parameter(0).encode('utf-8'))

    def register(self, version, uuid=""):
        message = LiveMessage("Register")
        message.append({'key': self.public_key, 'uuid': uuid,
                        'hash': self.hash_method})
        message.append({'protocol': 2, 'version': str(version),
                        'os': "linux", 'os-version': "unknown"})
        self.send_message(message)

    def ping(self):
        message = LiveMessage("Ping")
        self.send_message(message)

    def acknowledge(self, cookie):
        message = LiveMessage("ACK")
        message.append(cookie)
        self.send_message(message)

    def report_devices(self, devices, supported_methods):
        dev_list = []
        for device in devices:
            dev = {'id': device.id, 'name': device.name}
            dev['methods'] = device.methods(supported_methods)
            dev['state'] = device.last_sent_command(supported_methods)
            dev['stateValue'] = device.last_sent_value()
            dev_list.append(dev)
        message = LiveMessage("DevicesReport")
        message.append(dev_list)
        self.send_message(message)

    def report_device_event(self, device_id, method, data):
        message = LiveMessage("DeviceEvent")
        message.append(device_id)
        message.append(method)
        message.append(data)
        self.send_message(message)

    def _sensor(self, sensor):
        value_list = []
        for datatype in sensor.DATATYPES.values():
            if not sensor.has_value(datatype):
                continue
            value = sensor.value(datatype)
            value_list.append({'type': datatype, 'value': value.value,
                               'lastUp': value.timestamp})
            s = {'protocol': sensor.protocol, 'model': sensor.model,
                 'sensor_id': sensor.id}
        return s, value_list

    def report_sensors(self, sensors):
        sensor_list = []
        for sensor in sensors:
            s, value_list = self._sensor(sensor)
            s['name'] = ''
            sensor_list.append([s, value_list])

        message = LiveMessage("SensorsReport")
        message.append(sensor_list)
        self.send_message(message)

    def report_sensor_values(self, sensor):
        s, value_list = self._sensor(sensor)
        message = LiveMessage("SensorEvent")
        message.append(s)
        message.append(value_list)
        self.send_message(message)
