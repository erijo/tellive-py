Changelog
=========

0.5.1 (TBD)
-----------

* Don't try to start browser automatically during first run. In many cases it
  doesn't work and may hide the URL.


0.5.0 (2014-11-19)
------------------

* Disable appnap on Mac OS X if appnope module is available (issue #2).
* Report new/changed/removed devices to Telldus live.
* Release socket(s) before waiting to re-connect.
* Require tellcore-py >= v1.1.0.


0.4.2 (2014-02-25)
------------------

* Fixed problem that could occur after disconnect from server.
* Fixed tellive_core_connector problem on Mac OS X (issue #1).


0.4.1 (2014-02-06)
------------------

* Add all sensors and devices to the config on the first run.


0.4.0 (2014-02-06)
------------------

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
