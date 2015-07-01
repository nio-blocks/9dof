from unittest.mock import patch
from collections import defaultdict
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase
from ..sparkfun_9dof_block import SparkFun9DOF


@patch(SparkFun9DOF.__module__ + '.LSM9DS0')
class TestiSparkFun9DOF(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def patch_reads(self, blk):
        blk._lsm9ds0.read_accelerometer.return_value = (0, 1, 2)
        blk._lsm9ds0.read_magnetometer.return_value = (3, 4, 5)
        blk._lsm9ds0.read_gyroscope.return_value = (6, 7, 8)
        blk._lsm9ds0.read_temperature.return_value = 9

    def test_process_signals(self, lsm9ds0):
        blk = SparkFun9DOF()
        self.configure_block(blk, {})
        self.patch_reads(blk)
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(self.last_notified['default'][0].to_dict(), 
                             {
                              'accelerometer': (0, 1, 2),
                              'magnetometer': (3, 4, 5),
                              'gyroscope': (6, 7, 8),
                              'temperature': 9
                             })
