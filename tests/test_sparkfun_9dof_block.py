from unittest.mock import patch
from collections import defaultdict
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..sparkfun_9dof_block import SparkFun9DOF
from nio.block.terminals import DEFAULT_TERMINAL


@patch(SparkFun9DOF.__module__ + '.LSM9DS0')
class TestiSparkFun9DOF(NIOBlockTestCase):

    def setUp(self):
        super().setUp()

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
        self.assertDictEqual(self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
                             {
                              'accelerometer': (0, 1, 2),
                              'magnetometer': (3, 4, 5),
                              'gyroscope': (6, 7, 8),
                              'temperature': 9
                             })
