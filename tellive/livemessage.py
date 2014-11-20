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

import base64
import hashlib


class LiveMessageToken(object):
    def __init__(self, value=None):
        super().__init__()

        if type(value) in (int, str, bytes, list, dict):
            self.value = value
        else:
            self.value = None

    def serialize(self):
        """Serialize the token and return it as bytes."""
        if type(self.value) == int:
            return "i{:X}s".format(self.value).encode('ascii')

        if type(self.value) == str:
            value = self.value.encode('utf-8')
            return "{:X}:".format(len(value)).encode('ascii') + value

        if type(self.value) == bytes:
            value = base64.standard_b64encode(self.value)
            return "u{:X}:".format(len(value)).encode('ascii') + value

        if type(self.value) == list:
            items = [LiveMessageToken(m).serialize() for m in self.value]
            return b'l' + b''.join(items) + b's'

        if type(self.value) == dict:
            items = []
            for key, value in self.value.items():
                items.append(LiveMessageToken(str(key)).serialize())
                items.append(LiveMessageToken(value).serialize())
            return b'h' + b''.join(items) + b's'

        raise RuntimeError("Unknown type %s" % type(self.value))

    @staticmethod
    def deserialize(data):
        def _find(data, needle):
            needle = ord(needle)
            index = 0
            while index < len(data):
                if data[index] == needle:
                    return index
                index += 1
            raise ValueError

        def deserialize_int(data):
            end = _find(data, 's')
            return (LiveMessageToken(int(data[:end], 16)), data[end + 1:])

        def deserialize_list(data):
            result = []
            while data[0] != ord('s'):
                token, data = LiveMessageToken.deserialize(data)
                result.append(token.value)
            return (LiveMessageToken(result), data[1:])

        def deserialize_dict(data):
            result = {}
            while data[0] != ord('s'):
                key, data = LiveMessageToken.deserialize(data)
                value, data = LiveMessageToken.deserialize(data)
                result[str(key.value)] = value.value
            return (LiveMessageToken(result), data[1:])

        def deserialize_string(data, is_base64=False):
            end = _find(data, ':')
            value_end = end + 1 + int(data[:end], 16)
            value = data[end + 1:value_end]
            if is_base64:
                value = base64.standard_b64decode(value)
            else:
                value = value.decode('utf-8')
            return (LiveMessageToken(value), data[value_end:])

        try:
            if data[0] == ord('i'):
                return deserialize_int(data[1:])
            elif data[0] == ord('l'):
                return deserialize_list(data[1:])
            elif data[0] == ord('h'):
                return deserialize_dict(data[1:])
            elif data[0] == ord('u'):
                return deserialize_string(data[1:], is_base64=True)
            else:
                return deserialize_string(data)
        except:
            return (None, None)


class LiveMessage(object):
    def __init__(self, subject=None):
        super().__init__()
        self.tokens = []
        if subject:
            self.append(subject)

    def append(self, value):
        self.tokens.append(value)

    def subject(self):
        return self.tokens[0].lower()

    def parameter(self, index):
        return self.tokens[index + 1]

    def create_signed_message(self, private_key, hash_method):
        data = self.serialize()
        signature = LiveMessage.signature(data, private_key, hash_method)

        envelope = LiveMessage(signature)
        envelope.append(data.decode('utf-8'))
        return envelope

    def verify_signature(self, private_key, hash_method):
        data = self.parameter(0).encode('utf-8')
        signature = LiveMessage.signature(data, private_key, hash_method)
        return self.subject() == signature

    def serialize(self):
        tokens = [LiveMessageToken(t).serialize() for t in self.tokens]
        return b''.join(tokens)

    @staticmethod
    def deserialize(data):
        message = LiveMessage()
        while data:
            token, data = LiveMessageToken.deserialize(data)
            if not token:
                break
            message.append(token.value)
        return message

    @staticmethod
    def signature(data, private_key, hash_method):
        if hash_method == "sha512":
            signature = hashlib.sha512()
        elif hash_method == "sha256":
            signature = hashlib.sha256()
        else:
            signature = hashlib.sha1()

        signature.update(data)
        signature.update(private_key.encode('ascii'))
        return signature.hexdigest().lower()
