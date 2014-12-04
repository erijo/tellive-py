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
* On Mac OS X, `appnope <https://pypi.python.org/pypi/appnope>`_ is
  recommended.

Installation
------------

.. code-block:: bash

    $ pip install tellive-py

Example
-------

To run the included program for connecting a TellStick to Telldus Live:

.. code-block:: bash

    $ tellive_core_connector ~/.config/tellive.conf

The first time you run the program (with a particular config file), it will
exit and ask you to visit a given URL to give the program access to your
account.

When you have done so, you can then edit the config file
(``~/.config/tellive.conf`` in this example) and add a name to the sensors that
you wish to send to Telldus Live. You can also disable devices that you don't
want to be controllable via Telldus Live (see ``tellive_core_connector --help``
for more info). Then start the program again as above.

The program runs well as a background process in e.g. `screen
<http://www.gnu.org/software/screen/>`_. To have it automatically start after
boot, you can add the following to your crontab (``crontab -e``). The two lines
that set ``PYTHONPATH`` and ``PATH`` are only needed if you haven't installed
the modules, only cloned the repositories or unpacked the tar ball (replace
``/home/erik`` with the correct path):

.. code-block:: bash

    PYTHONPATH = /home/erik/tellive-py:/home/erik/tellcore-py
    PATH = /home/erik/tellive-py/bin:/usr/bin:/bin

    @reboot screen -dmS tellive tellive_core_connector ~/tellive.conf

API example
-----------

The API can also be used by your own program. This how you would connect to
Telldus Live and register the client (with PUBLIC_KEY and PRIVATE_KEY from
`here <http://api.telldus.com/keys/index>`_):

.. code-block:: python

    client = TellstickLiveClient(PUBLIC_KEY, PRIVATE_KEY)
    (server, port) = client.connect_to_first_available_server()
    client.register(version="0.1")
