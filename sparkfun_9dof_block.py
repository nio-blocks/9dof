from nio.block.base import Block
from nio.signal.base import Signal
from nio.properties import VersionProperty

from .lsm9ds0 import LSM9DS0


class SparkFun9DOF(Block):

    """ Read from SparkFun 9 Degrees of Freedom Edison board """

    version = VersionProperty("0.1.0")

    def __init__(self):
        super().__init__()
        self._lsdm9ds0 = None

    def configure(self, context):
        super().configure(context)
        try:
            self._lsm9ds0 = LSM9DS0()
        except:
            self.logger.exception('Failed to connect to to LSM9DS.'
                                  ' Try running with root privelages.')

    def process_signals(self, signals, input_id='default'):
        out_sigs = []
        for signal in signals:
            a = self._lsm9ds0.read_accelerometer()
            m = self._lsm9ds0.read_magnetometer()
            g = self._lsm9ds0.read_gyroscope()
            t = self._lsm9ds0.read_temperature()
            out_sigs.append(Signal({'accelerometer': a,
                                    'magnetometer': m,
                                    'gyroscope': g,
                                    'temperature': t}))
        if out_sigs:
            self.notify_signals(out_sigs)
