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

import unittest

from tellive.livemessage import LiveMessageToken


class Test(unittest.TestCase):
    def assert_invalid(self, token):
        self.assertIs(token.value, None)

    def assert_int(self, token, expected):
        self.assertIs(type(token.value), int)
        self.assertEqual(token.value, expected)

    def assert_string(self, token, expected):
        self.assertIs(type(token.value), str)
        self.assertEqual(token.value, expected)

    def assert_base64(self, token, expected):
        self.assertIs(type(token.value), bytes)
        self.assertEqual(token.value, expected)

    def assert_list(self, token, expected):
        self.assertIs(type(token.value), list)
        self.assertListEqual(token.value, expected)

    def assert_dict(self, token, expected):
        self.assertIs(type(token.value), dict)
        self.assertDictEqual(token.value, expected)

    def test_empty_token(self):
        self.assert_invalid(LiveMessageToken())

    def test_int(self):
        token = LiveMessageToken(10)
        self.assert_int(token, 10)
        self.assertEqual(token.serialize(), b'iAs')

    def test_string(self):
        a_ring = b'\xc3\xa5'.decode('utf-8')
        token = LiveMessageToken("foobar123456" + a_ring)
        self.assert_string(token, "foobar123456" + a_ring)
        self.assertEqual(token.serialize(), b'E:foobar123456\xc3\xa5')

    def test_base64(self):
        token = LiveMessageToken(b'foobar123456')
        self.assert_base64(token, b'foobar123456')
        self.assertEqual(token.serialize(), b'u10:Zm9vYmFyMTIzNDU2')

    def test_empty_list(self):
        token = LiveMessageToken([])
        self.assert_list(token, [])
        self.assertEqual(token.serialize(), b'ls')

    def test_list(self):
        token = LiveMessageToken([1, "foo"])
        self.assert_list(token, [1, "foo"])
        self.assertEqual(token.serialize(), b'li1s3:foos')

    def test_empty_dict(self):
        token = LiveMessageToken({})
        self.assert_dict(token, {})
        self.assertEqual(token.serialize(), b'hs')

    def test_dict(self):
        token = LiveMessageToken({'1': "foo", '2': 3})
        self.assert_dict(token, {'1': "foo", '2': 3})
        # The order of keys are undefined
        serialized = token.serialize()
        if serialized != b'h1:13:foo1:2i3ss':
            self.assertEqual(serialized, b'h1:2i3s1:13:foos')

    def test_dict_in_list_in_dict(self):
        token = LiveMessageToken({'a': [{'b': 1}, 2]})
        self.assertIs(type(token.value['a']), list)
        self.assertEqual(token.serialize(), b'h1:alh1:bi1ssi2sss')

    def test_deserialize_empty(self):
        self.assertIs(None, LiveMessageToken.deserialize(b'')[0])

    def test_deserialize_invalid(self):
        self.assertIs(None, LiveMessageToken.deserialize(b'i')[0])
        self.assertIs(None, LiveMessageToken.deserialize(b'l')[0])
        self.assertIs(None, LiveMessageToken.deserialize(b'h')[0])
        self.assertIs(None, LiveMessageToken.deserialize(b'hi1s')[0])
        self.assertIs(None, LiveMessageToken.deserialize(b'u')[0])
        self.assertIs(None, LiveMessageToken.deserialize(b'u7:YWxpdmU')[0])

    def test_deserialize_int(self):
        (token, rest) = LiveMessageToken.deserialize(b'i1A2s')
        self.assert_int(token, 0x1a2)
        self.assertFalse(rest)

    def test_deserialize_empty_list(self):
        (token, rest) = LiveMessageToken.deserialize(b'ls')
        self.assert_list(token, [])
        self.assertFalse(rest)

    def test_deserialize_list(self):
        (token, rest) = LiveMessageToken.deserialize(b'li1siAss')
        self.assert_list(token, [1, 10])
        self.assertFalse(rest)

    def test_deserialize_empty_dict(self):
        (token, rest) = LiveMessageToken.deserialize(b'hs')
        self.assert_dict(token, {})
        self.assertFalse(rest)

    def test_deserialize_dict(self):
        (token, rest) = LiveMessageToken.deserialize(b'h1:13:foo1:26:foobars')
        self.assert_dict(token, {'1': "foo", '2': "foobar"})
        self.assertFalse(rest)

    def test_deserialize_dict_with_list(self):
        (token, rest) = LiveMessageToken.deserialize(
            b'h1:1li1Es1:Alss1:2h1:3hsss')
        self.assert_dict(token, {'1': [0x1e, "A", []], '2': {'3': {}}})
        self.assertFalse(rest)

    def test_deserialize_empty_base64(self):
        (token, rest) = LiveMessageToken.deserialize(b'u0:')
        self.assert_base64(token, b'')
        self.assertFalse(rest)

    def test_deserialize_base64(self):
        (token, rest) = LiveMessageToken.deserialize(b'u8:YWxpdmU=')
        self.assert_base64(token, b'alive')
        self.assertFalse(rest)

    def test_deserialize_empty_string(self):
        (token, rest) = LiveMessageToken.deserialize(b'0:')
        self.assert_string(token, "")
        self.assertFalse(rest)

    def test_deserialize_string(self):
        (token, rest) = LiveMessageToken.deserialize(b'10:123456789abcdefP')
        self.assert_string(token, "123456789abcdefP")
        self.assertFalse(rest)


if __name__ == '__main__':
    unittest.main()
