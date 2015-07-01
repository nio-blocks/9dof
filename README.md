SparkFun9DOF
============

Read from SparkFun 9 Degrees of Freedom Edison board

Sensors are read and a Signal is notified each time a Signal is processed by the block.

Properties
----------
None

Dependencies
------------

-   [**mraa**](https://github.com/intel-iot-devkit/mraa): Not on PyPI. Follow the install instruction on [sparkfun](https://learn.sparkfun.com/tutorials/installing-libmraa-on-ubilinux-for-edison)
-   [**numpy**](https://pypi.python.org/pypi/numpy)

Commands
--------
None

Input
-----
Any list of signals to trigger sensor read.

Output
------

-   accelerometer: [x, y, z]
-   magnetometer: [x, y, z]
-   gyroscope: [x, y, z]
-   temperature
