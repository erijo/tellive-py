Python wrapper for Telldus Live
===============================

.. image:: https://badge.fury.io/py/tellive-py.png
    :target: https://pypi.python.org/pypi/tellive-py/

.. image:: https://secure.travis-ci.org/erijo/tellive-py.png?branch=master
    :target: http://travis-ci.org/erijo/tellive-py

tellive-py is a Python wrapper for `Telldus Live <http://live.telldus.com/>`_,
"a user friendly service for automating your TellStick connected gear using the
Internet".

* Official home page: https://github.com/erijo/tellive-py
* Python package index: https://pypi.python.org/pypi/tellive-py

Please report any problem as a `GitHub issue report
<https://github.com/erijo/tellive-py/issues/new>`_.

Features
--------

* Includes the script `tellive_core_connector
  <https://github.com/erijo/tellive-py/blob/master/bin/tellive_core_connector>`_
  for connecting a e.g. a Tellstick Duo to Telldus Live without needing Telldus
  Center. Supports both devices and sensors.
* Open source (`GPLv3+
  <https://github.com/erijo/tellive-py/blob/master/LICENSE.txt>`_).

Requirements
------------

* Python 3.2+
* `tellcore-py <https://github.com/erijo/tellcore-py>`_

Installation
------------

.. code-block:: bash

    $ pip install tellcore-py tellive-py

Example
-------

To run the included program for connecting a TellStick to Telldus Live:

.. code-block:: bash

    $ tellive_core_connector ~/.config/tellive.conf

The API can also be used by your own program. This how you would connect to
Telldus Live and register the client (with PUBLIC_KEY and PRIVATE_KEY from
`here <http://api.telldus.com/keys/index>`_):

.. code-block:: python

    client = TellstickLiveClient(PUBLIC_KEY, PRIVATE_KEY)
    (server, port) = client.connect_to_first_available_server()
    client.register(version="0.1")
