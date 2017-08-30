import sys
from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from nio.block.terminals import DEFAULT_TERMINAL


class TestSparkFun9DOF(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['mraa'] = MagicMock()
        sys.modules['numpy'] = MagicMock()
        from ..sparkfun_9dof_block import SparkFun9DOF
        global SparkFun9DOF

    def test_process_signals(self):
        blk = SparkFun9DOF()
        with patch(SparkFun9DOF.__module__ + '.LSM9DS0') as mock_9dof:
            mock_9dof().read_accelerometer.return_value = (0, 1, 2)
            mock_9dof().read_magnetometer.return_value = (3, 4, 5)
            mock_9dof().read_gyroscope.return_value = (6, 7, 8)
            mock_9dof().read_temperature.return_value = 9
            self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), {
                'accelerometer': (0, 1, 2),
                'magnetometer': (3, 4, 5),
                'gyroscope': (6, 7, 8),
                'temperature': 9,
            })
