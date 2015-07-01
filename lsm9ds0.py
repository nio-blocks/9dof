import mraa
import numpy


class LSM9DS0():
    ''' Used for i2c communication with LSM9DS0 chip

    All config settings information found in datasheet:
    http://www.adafruit.com/datasheets/LSM9DS0.pdf

    Code inspired by https://github.com/smoyerman/9dofBlock
    '''

    WHO_AM_I = 0x0F

    # Gyroscope
    G = 0x6B
    CTRL_REG1_G = 0x20
    CTRL_REG4_G = 0x23

    # Acceleromter/Magnetometer/Temperature
    XM = 0x1D
    CTRL_REG1_XM = 0x20
    CTRL_REG2_XM = 0x21
    CTRL_REG5_XM = 0x24
    CTRL_REG6_XM = 0x25
    CTRL_REG7_XM = 0x26

    def __init__(self, i2c_port=1):
        self._i2c = mraa.I2c(i2c_port)
        self._check_connection()
        self._enable_sensors()
        self._configure_sensors()

    def _check_connection(self):
        WHO_AM_I_G_RESP = 0xD4
        WHO_AM_I_XM_RESP = 0x49
        # Check connection to XM
        resp = self._i2c.address(self.XM)
        if resp is not 0:
            raise Exception('Not connected to acceleromter/magnetometer.')
        resp = self._i2c.readReg(self.WHO_AM_I)
        if resp is not WHO_AM_I_XM_RESP:
            raise Exception('Bad connection to acceleromter/magnetometer.')
        # Check connection to G
        resp = self._i2c.address(self.G)
        if resp is not 0:
            raise Exception('Not connected to gyroscope.')
        resp = self._i2c.readReg(self.WHO_AM_I)
        if resp is not WHO_AM_I_G_RESP:
            raise Exception('Bad connection to gyroscope.')

    def _enable_sensors(self):
        self._enable_accelerometer()
        self._enable_magnetometer()
        self._enable_gyroscope()
        self._enable_temperature()

    def _configure_sensors(self):
        self._configure_accelerometer()
        self._configure_magnetometer()
        self._configure_gyroscope()

    def _enable_accelerometer(self):
        # 0x67: 100 Hz
        self._i2c.address(self.XM)
        self._i2c.writeReg(self.CTRL_REG1_XM, 0x67)

    def _enable_magnetometer(self):
        # 0x00: Continuous-conversion mode
        self._i2c.address(self.XM)
        self._i2c.writeReg(self.CTRL_REG7_XM, 0x00)

    def _enable_gyroscope(self):
        # 0x0F: 95 Hz at 12.5 Cutoff
        self._i2c.address(self.G)
        self._i2c.writeReg(self.CTRL_REG1_G, 0x0F)

    def _enable_temperature(self):
        ## 0xF0: Enabled, high res, 100 Hz
        self._i2c.address(self.XM)
        self._i2c.writeReg(self.CTRL_REG5_XM, 0xF0)

    def _configure_accelerometer(self):
        # 0x00: +/- 2 g (default)
        self._i2c.address(self.XM)
        self._i2c.writeReg(self.CTRL_REG2_XM, 0x00)

    def _configure_magnetometer(self):
        # 0x00: +/- 2 gauss (default)
        self._i2c.address(self.XM)
        self._i2c.writeReg(self.CTRL_REG6_XM, 0x00)

    def _configure_gyroscope(self):
        # 0x00: +/- 245 dps (default)
        self._i2c.address(self.G)
        self._i2c.writeReg(self.CTRL_REG4_G, 0x00)

    def _read_xyz(self, address, register, calibration_factor=1):
        """
        Read the x, y and z registers.

        address: i2c address
        register: register of x-axis
        calibration_factor: the positive range divided by the maximum 
            positive 2-byte signed integer

        From datasheet:  If the MSb of the SUB field is ‘1’, the SUB
        (register address) will be automatically increased to allow
        multiple data read/writes.
        """
        self._i2c.address(address)
        # Read the x-axis register (2 bytes) along with the next 4 bytes.
        data = self._i2c.readBytesReg(0x80 | register, 6)
        # Each axis is 16 bit as two's compliment left justified.
        x = numpy.int16(data[0] | (data[1] << 8)) * calibration_factor
        y = numpy.int16(data[2] | (data[3] << 8)) * calibration_factor
        z = numpy.int16(data[4] | (data[5] << 8)) * calibration_factor
        return (x, y, z)

    def read_accelerometer(self):
        OUT_X_L_A = 0x28
        # This calibration factor is only for default 2 g
        calibration_factor = (2.0/32768.0)
        (x, y, z) = self._read_xyz(self.XM, OUT_X_L_A, calibration_factor)
        return (x, y, z)

    def read_magnetometer(self):
        OUT_X_L_M = 0x08
        # This calibration factor is only for default 2 gauss
        calibration_factor = (2.0/32768.0)
        (x, y, z) = self._read_xyz(self.XM, OUT_X_L_M, calibration_factor)
        return (x, y, z)

    def read_gyroscope(self):
        OUT_X_L_G = 0x28
        # This calibration factor is only for default 245 dps
        calibration_factor = (245.0/32768.0)
        (x, y, z) = self._read_xyz(self.G, OUT_X_L_G, calibration_factor)
        return (x, y, z)

    def read_temperature(self):
        OUT_TEMP_L_XM = 0x05
        self._i2c.address(self.XM)
        data = self._i2c.readBytesReg(0x80 | OUT_TEMP_L_XM, 2)
        # Two’s complement data in 12-bit format, right justified
        temp = numpy.int16(data[0] | (data[1] << 8))
        return temp


if __name__ == '__main__':
    nine = LSM9DS0()
    from time import sleep
    while True:
        a = nine.read_accelerometer()
        m = nine.read_magnetometer()
        g = nine.read_gyroscope()
        t = nine.read_temperature()
        print('Accel: {}'.format(a))
        print('Mag:   {}'.format(m))
        print('Gyro:  {}'.format(g))
        print('Temp:  {}'.format(t))
        sleep(1)
