Changelog
=========

NEXT (TBD)
----------

* Fixed tellive_core_connector to not wake up two times every second, but
  instead only wake up when there is work to do.


0.3.0 (2014-02-04)
------------------

* Removed reload message as it is not supposed to be sent to clients.
* Better values for os and os-version in register message.
* Support marking devices as disabled to not show up in Telldus Live.


0.2.0 (2014-02-02)
------------------

* tellive_core_connector now uses official keys from Telldus, so you no longer
  need to use private tokens.
* Log using the standard logging module.
* Reconnect if connection is lost for some reason.
* Fixed problem with Python 3.2.
* Added support for reload request from server.
* Only report sensors that are named in the config file.


0.1.1 (2014-01-28)
------------------

* Fix some packaging issues.


0.1.0 (2014-01-28)
------------------

* Initial release.
