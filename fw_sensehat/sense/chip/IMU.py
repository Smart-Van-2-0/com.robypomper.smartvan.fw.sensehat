#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import smbus
import math

# define QMI8658 and AK09918 Device I2C address
I2C_ADD_IMU_QMI8658 = 0x6B
I2C_ADD_IMU_AK09918 = 0x0C

Ki = 1.0
Kp = 4.50

# define QMI8658 Register
QMI8658_CTRL7_ACC_ENABLE = 0x01
QMI8658_CTRL7_GYR_ENABLE = 0x02

QMI8658Register_Ctrl1 = 0x02  # SPI Interface and Sensor Enable
QMI8658Register_Ctrl2 = 0x03  # Accelerometer control.
QMI8658Register_Ctrl3 = 0x04  # Gyroscope control.
QMI8658Register_Ctrl5 = 0x06  # Data processing settings.
QMI8658Register_Ctrl7 = 0x08  # Sensor enabled status.

QMI8658Register_Ax_L = 0x35  # Accelerometer X axis least significant byte.
QMI8658Register_Ax_H = 0x36  # Accelerometer X axis most significant byte.
QMI8658Register_Ay_L = 0x37  # Accelerometer Y axis least significant byte.
QMI8658Register_Ay_H = 0x38  # Accelerometer Y axis most significant byte.
QMI8658Register_Az_L = 0x39  # Accelerometer Z axis least significant byte.
QMI8658Register_Az_H = 0x3A  # Accelerometer Z axis most significant byte.
QMI8658Register_Gx_L = 0x3B  # Gyroscope X axis least significant byte.
QMI8658Register_Gx_H = 0x3C  # Gyroscope X axis most significant byte.
QMI8658Register_Gy_L = 0x3D  # Gyroscope Y axis least significant byte.
QMI8658Register_Gy_H = 0x3E  # Gyroscope Y axis most significant byte.
QMI8658Register_Gz_L = 0x3F  # Gyroscope Z axis least significant byte.
QMI8658Register_Gz_H = 0x40  # Gyroscope Z axis most significant byte.

QMI8658Register_Tempearture_L = 0x33  # tempearture low.
QMI8658Register_Tempearture_H = 0x34  # tempearture high.

QMI8658AccRange_2g = 0x00 << 4  # !< \brief +/- 2g range
QMI8658AccRange_4g = 0x01 << 4  # !< \brief +/- 4g range
QMI8658AccRange_8g = 0x02 << 4  # !< \brief +/- 8g range
QMI8658AccRange_16g = 0x03 << 4  # !< \brief +/- 16g range

QMI8658AccOdr_8000Hz = 0x00  # !< \brief High resolution 8000Hz output rate.
QMI8658AccOdr_4000Hz = 0x01  # !< \brief High resolution 4000Hz output rate.
QMI8658AccOdr_2000Hz = 0x02  # !< \brief High resolution 2000Hz output rate.
QMI8658AccOdr_1000Hz = 0x03  # !< \brief High resolution 1000Hz output rate.
QMI8658AccOdr_500Hz = 0x04  # !< \brief High resolution 500Hz output rate.
QMI8658AccOdr_250Hz = 0x05  # !< \brief High resolution 250Hz output rate.
QMI8658AccOdr_125Hz = 0x06  # !< \brief High resolution 125Hz output rate.
QMI8658AccOdr_62_5Hz = 0x07  # !< \brief High resolution 62.5Hz output rate.
QMI8658AccOdr_31_25Hz = 0x08  # !< \brief High resolution 31.25Hz output rate.
QMI8658AccOdr_LowPower_128Hz = 0x0C  # !< \brief Low power 128Hz output rate.
QMI8658AccOdr_LowPower_21Hz = 0x0D  # !< \brief Low power 21Hz output rate.
QMI8658AccOdr_LowPower_11Hz = 0x0E  # !< \brief Low power 11Hz output rate.
QMI8658AccOdr_LowPower_3Hz = 0x0F  # !< \brief Low power 3Hz output rate.

QMI8658GyrRange_16dps = 0 << 4  # !< \brief +-16 degrees per second.
QMI8658GyrRange_32dps = 1 << 4  # !< \brief +-32 degrees per second.
QMI8658GyrRange_64dps = 2 << 4  # !< \brief +-64 degrees per second.
QMI8658GyrRange_128dps = 3 << 4  # !< \brief +-128 degrees per second.
QMI8658GyrRange_256dps = 4 << 4  # !< \brief +-256 degrees per second.
QMI8658GyrRange_512dps = 5 << 4  # !< \brief +-512 degrees per second.
QMI8658GyrRange_1024dps = 6 << 4  # !< \brief +-1024 degrees per second.
QMI8658GyrRange_248dps = 7 << 4  # !< \brief +-2048 degrees per second.

QMI8658GyrOdr_8000Hz = 0x00  # !< \brief High resolution 8000Hz output rate.
QMI8658GyrOdr_4000Hz = 0x01  # !< \brief High resolution 8000Hz output rate.
QMI8658GyrOdr_2000Hz = 0x02  # !< \brief High resolution 8000Hz output rate.
QMI8658GyrOdr_1000Hz = 0x03  # !< \brief High resolution 8000Hz output rate.
QMI8658GyrOdr_500Hz = 0x04  # !< \brief High resolution 8000Hz output rate.
QMI8658GyrOdr_250Hz = 0x05  # !< \brief High resolution 8000Hz output rate.
QMI8658GyrOdr_125Hz = 0x06  # !< \brief High resolution 8000Hz output rate.
QMI8658GyrOdr_62_5Hz = 0x07  # !< \brief High resolution 8000Hz output rate.
QMI8658GyrOdr_31_25Hz = 0x08  # !< \brief High resolution 8000Hz output rate.

# define QMI8658 Register  end

# define AK09918 Register
AK09918_WIA1 = 0x00     # Company ID
AK09918_WIA2 = 0x01     # Device ID
AK09918_RSV1 = 0x02     # Reserved 1
AK09918_RSV2 = 0x03     # Reserved 2
AK09918_ST1 = 0x10      # DataStatus 1
AK09918_HXL = 0x11      # X-axis data
AK09918_HXH = 0x12
AK09918_HYL = 0x13      # Y-axis data
AK09918_HYH = 0x14
AK09918_HZL = 0x15      # Z-axis data
AK09918_HZH = 0x16
AK09918_TMPS = 0x17     # Dummy
AK09918_ST2 = 0x18      # Datastatus 2
AK09918_CNTL1 = 0x30    # Dummy
AK09918_CNTL2 = 0x31    # Control settings
AK09918_CNTL3 = 0x32    # Control settings

AK09918_SRST_BIT = 0x01     # Soft Reset
AK09918_HOFL_BIT = 0x08     # Sensor Over Flow
AK09918_DOR_BIT = 0x02      # Data Over Run
AK09918_DRDY_BIT = 0x01     # Data Ready

AK09918_POWER_DOWN = 0x00
AK09918_NORMAL = 0x01
AK09918_CONTINUOUS_10HZ = 0x02
AK09918_CONTINUOUS_20HZ = 0x04
AK09918_CONTINUOUS_50HZ = 0x06
AK09918_CONTINUOUS_100HZ = 0x08
AK09918_SELF_TEST = 0x10  # ignored by switchMode() and initialize(), call selfTest() to use this mode


# define AK09918 Register  end
class IMU(object):
    def __init__(self, address_qmi=I2C_ADD_IMU_QMI8658,
                 address_ak=I2C_ADD_IMU_AK09918):
        self._address_qmi = address_qmi
        self._address_ak = address_ak
        self._bus = smbus.SMBus(1)
        if self._read_byte(self._address_qmi, 0x00) != 0x05:
            raise IOError("Can't init QMI8658 via I2C on address '{}'".format(
                self._address_qmi))

        self.MotionVal = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.Gyro = [0, 0, 0]
        self.Accel = [0, 0, 0]
        self.Mag = [0, 0, 0]
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        self.pu8data = [0, 0, 0, 0, 0, 0, 0, 0]
        self.U8tempX = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.U8tempY = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.U8tempZ = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.GyroOffset = [0, 0, 0]
        self.q0 = 1.0
        self.q1 = self.q2 = self.q3 = 0.0
        self.temp = 0.0

        self._write_byte(self._address_qmi, QMI8658Register_Ctrl1, 0x60)
        # Set acceleration mode 2g 1000Hz
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl2,
                         QMI8658AccRange_2g | QMI8658AccOdr_1000Hz)
        # Set gyro mode 512dps 500Hz
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl3,
                         QMI8658GyrRange_512dps | QMI8658GyrOdr_500Hz)
        # Sensor data processing settings
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl5,
                         0x00)
        # Enable acceleration and gyroscope sensors
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl7,
                         QMI8658_CTRL7_ACC_ENABLE | QMI8658_CTRL7_GYR_ENABLE | 0x80)
        self.QMI8658_GyroOffset()

        if self._read_byte(self._address_ak, AK09918_WIA2) != 0x0C:
            raise IOError("Can't init AK09918 via I2C on address '{}'".format(
                self._address_ak))

        self._write_byte(self._address_ak, AK09918_CNTL3, AK09918_SRST_BIT)  #  Reset AK09918
        self._write_byte(self._address_ak, AK09918_CNTL2, AK09918_CONTINUOUS_20HZ)  # Set magnetometer mode

    def _read_byte(self, address, cmd):
        return self._bus.read_byte_data(address, cmd)

    def _read_block(self, address, reg, length=1):
        return self._bus.read_i2c_block_data(address, reg, length)

    def _read_u16(self, address, cmd):
        LSB = self._bus.read_byte_data(address, cmd)
        MSB = self._bus.read_byte_data(address, cmd + 1)
        return (MSB << 8) + LSB

    def _write_byte(self, address, cmd, val):
        self._bus.write_byte_data(address, cmd, val)
        time.sleep(0.0001)

    def QMI8658_Gyro_Accel_Read(self):
        data = self._read_block(self._address_qmi, QMI8658Register_Ax_L, 12)
        self.Accel[0] = (data[1] << 8) | data[0]
        self.Accel[1] = (data[3] << 8) | data[2]
        self.Accel[2] = (data[5] << 8) | data[4]
        self.Gyro[0] = ((data[7] << 8) | data[6]) - self.GyroOffset[0]
        self.Gyro[1] = ((data[9] << 8) | data[8]) - self.GyroOffset[1]
        self.Gyro[2] = ((data[11] << 8) | data[10]) - self.GyroOffset[2]
        # Solve the problem that Python shift will not overflow
        if self.Accel[0] >= 32767:
            self.Accel[0] = self.Accel[0] - 65535
        elif self.Accel[0] <= -32767:
            self.Accel[0] = self.Accel[0] + 65535
        if self.Accel[1] >= 32767:
            self.Accel[1] = self.Accel[1] - 65535
        elif self.Accel[1] <= -32767:
            self.Accel[1] = self.Accel[1] + 65535
        if self.Accel[2] >= 32767:
            self.Accel[2] = self.Accel[2] - 65535
        elif self.Accel[2] <= -32767:
            self.Accel[2] = self.Accel[2] + 65535
        if self.Gyro[0] >= 32767:
            self.Gyro[0] = self.Gyro[0] - 65535
        elif self.Gyro[0] <= -32767:
            self.Gyro[0] = self.Gyro[0] + 65535
        if self.Gyro[1] >= 32767:
            self.Gyro[1] = self.Gyro[1] - 65535
        elif self.Gyro[1] <= -32767:
            self.Gyro[1] = self.Gyro[1] + 65535
        if self.Gyro[2] >= 32767:
            self.Gyro[2] = self.Gyro[2] - 65535
        elif self.Gyro[2] <= -32767:
            self.Gyro[2] = self.Gyro[2] + 65535

    def AK09918_MagRead(self):
        counter = 20
        while (counter > 0):
            time.sleep(0.01)
            u8Data = self._read_byte(self._address_ak, AK09918_ST1)
            if ((u8Data & 0x01) != 0):
                break
            counter -= 1

        if counter != 0:
            for i in range(0, 8):
                pu8data = self._read_block(self._address_ak, AK09918_HXL, 8)
                self.U8tempX[i] = (pu8data[1] << 8) | pu8data[0]
                self.U8tempY[i] = (pu8data[3] << 8) | pu8data[2]
                self.U8tempZ[i] = (pu8data[5] << 8) | pu8data[4]
            self.Mag[0] = (self.U8tempX[0] + self.U8tempX[1] + self.U8tempX[2] + self.U8tempX[3] +
                      self.U8tempX[4] + self.U8tempX[5] + self.U8tempX[6] + self.U8tempX[7]) / 8
            self.Mag[1] = (self.U8tempY[0] + self.U8tempY[1] + self.U8tempY[2] + self.U8tempY[3] +
                      self.U8tempY[4] + self.U8tempY[5] + self.U8tempY[6] + self.U8tempY[7]) / 8
            self.Mag[2] = (self.U8tempZ[0] + self.U8tempZ[1] + self.U8tempZ[2] + self.U8tempZ[3] +
                      self.U8tempZ[4] + self.U8tempZ[5] + self.U8tempZ[6] + self.U8tempZ[7]) / 8
        # Solve the problem that Python shift will not overflow
        if self.Mag[0] >= 32767:
            self.Mag[0] = self.Mag[0] - 65535
        elif self.Mag[0] <= -32767:
            self.Mag[0] = self.Mag[0] + 65535
        if self.Mag[1] >= 32767:
            self.Mag[1] = self.Mag[1] - 65535
        elif self.Mag[1] <= -32767:
            self.Mag[1] = self.Mag[1] + 65535
        if self.Mag[2] >= 32767:
            self.Mag[2] = self.Mag[2] - 65535
        elif self.Mag[2] <= -32767:
            self.Mag[2] = self.Mag[2] + 65535

    def QMI8658_readTemp(self):
        temp = self._read_block(self._address_qmi,
                                QMI8658Register_Tempearture_L, 2)
        return float((temp[1] << 8) | temp[0]) / 256.0

    def QMI8658_GyroOffset(self):
        s32TempGx = 0
        s32TempGy = 0
        s32TempGz = 0
        for i in range(0, 32):
            self.QMI8658_Gyro_Accel_Read()
            s32TempGx += self.Gyro[0]
            s32TempGy += self.Gyro[1]
            s32TempGz += self.Gyro[2]
            time.sleep(0.01)
        self.GyroOffset[0] = s32TempGx >> 5
        self.GyroOffset[1] = s32TempGy >> 5
        self.GyroOffset[2] = s32TempGz >> 5

    def imuAHRSupdate(self):
        gx = self.MotionVal[0] * 0.0175
        gy = self.MotionVal[1] * 0.0175
        gz = self.MotionVal[2] * 0.0175
        ax = self.MotionVal[3]
        ay = self.MotionVal[4]
        az = self.MotionVal[5]
        mx = self.MotionVal[6]
        my = self.MotionVal[7]
        mz = self.MotionVal[8]

        norm = 0.0
        hx = hy = hz = bx = bz = 0.0
        vx = vy = vz = wx = wy = wz = 0.0
        exInt = eyInt = ezInt = 0.0
        ex = ey = ez = 0.0
        halfT = 0.024
        l_q0 = self.q0
        l_q1 = self.q1
        l_q2 = self.q2
        l_q3 = self.q3
        q0q0 = l_q0 * l_q0
        q0q1 = l_q0 * l_q1
        q0q2 = l_q0 * l_q2
        q0q3 = l_q0 * l_q3
        q1q1 = l_q1 * l_q1
        q1q2 = l_q1 * l_q2
        q1q3 = l_q1 * l_q3
        q2q2 = l_q2 * l_q2
        q2q3 = l_q2 * l_q3
        q3q3 = l_q3 * l_q3

        norm = float(1 / math.sqrt(ax * ax + ay * ay + az * az))
        ax = ax * norm
        ay = ay * norm
        az = az * norm

        norm = float(1 / math.sqrt(mx * mx + my * my + mz * mz))
        mx = mx * norm
        my = my * norm
        mz = mz * norm

        # compute reference direction of flux
        hx = 2 * mx * (0.5 - q2q2 - q3q3) + 2 * my * (q1q2 - q0q3) + 2 * mz * (q1q3 + q0q2)
        hy = 2 * mx * (q1q2 + q0q3) + 2 * my * (0.5 - q1q1 - q3q3) + 2 * mz * (q2q3 - q0q1)
        hz = 2 * mx * (q1q3 - q0q2) + 2 * my * (q2q3 + q0q1) + 2 * mz * (0.5 - q1q1 - q2q2)
        bx = math.sqrt((hx * hx) + (hy * hy))
        bz = hz

        # estimated direction of gravity and flux (v and w)
        vx = 2 * (q1q3 - q0q2)
        vy = 2 * (q0q1 + q2q3)
        vz = q0q0 - q1q1 - q2q2 + q3q3
        wx = 2 * bx * (0.5 - q2q2 - q3q3) + 2 * bz * (q1q3 - q0q2)
        wy = 2 * bx * (q1q2 - q0q3) + 2 * bz * (q0q1 + q2q3)
        wz = 2 * bx * (q0q2 + q1q3) + 2 * bz * (0.5 - q1q1 - q2q2)

        # error is sum of cross product between reference direction of fields and direction measured by sensors
        ex = (ay * vz - az * vy) + (my * wz - mz * wy)
        ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
        ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

        if (ex != 0.0 and ey != 0.0 and ez != 0.0):
            exInt = exInt + ex * Ki * halfT
            eyInt = eyInt + ey * Ki * halfT
            ezInt = ezInt + ez * Ki * halfT

            gx = gx + Kp * ex + exInt
            gy = gy + Kp * ey + eyInt
            gz = gz + Kp * ez + ezInt

        l_q0 = l_q0 + (-l_q1 * gx - l_q2 * gy - l_q3 * gz) * halfT
        l_q1 = l_q1 + (l_q0 * gx + l_q2 * gz - l_q3 * gy) * halfT
        l_q2 = l_q2 + (l_q0 * gy - l_q1 * gz + l_q3 * gx) * halfT
        l_q3 = l_q3 + (l_q0 * gz + l_q1 * gy - l_q2 * gx) * halfT

        norm = float(1 / math.sqrt(l_q0 * l_q0 + l_q1 * l_q1 + l_q2 * l_q2 + l_q3 * l_q3))
        self.q0 = l_q0 * norm
        self.q1 = l_q1 * norm
        self.q2 = l_q2 * norm
        self.q3 = l_q3 * norm

    def icm20948CalAvgValue(self):
        self.MotionVal[0] = self.Gyro[0] / 32.8
        self.MotionVal[1] = self.Gyro[1] / 32.8
        self.MotionVal[2] = self.Gyro[2] / 32.8
        self.MotionVal[3] = self.Accel[0]
        self.MotionVal[4] = self.Accel[1]
        self.MotionVal[5] = self.Accel[2]
        self.MotionVal[6] = self.Mag[0]
        self.MotionVal[7] = self.Mag[1]
        self.MotionVal[8] = self.Mag[2]

    def refreshAll(self):
        self.QMI8658_Gyro_Accel_Read()
        self.AK09918_MagRead()
        self.icm20948CalAvgValue()
        self.imuAHRSupdate()
        self.temp = self.QMI8658_readTemp()

    def getPitchRollYaw(self) -> (float, float, float):
        q0 = self.q0
        q1 = self.q1
        q2 = self.q2
        q3 = self.q3

        pitch = math.asin(-2 * q1 * q3 + 2 * q0 * q2) * 57.3
        roll = math.atan2(2 * q2 * q3 + 2 * q0 * q1,
                          -2 * q1 * q1 - 2 * q2 * q2 + 1) * 57.3
        yaw = math.atan2(-2 * q1 * q2 - 2 * q0 * q3,
                         2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3

        return round(pitch, 2), round(roll, 2), round(yaw, 2)

    def getAccel(self) -> (int, int, int):
        return self.Accel[0], self.Accel[1], self.Accel[2]

    def getGyro(self) -> (int, int, int):
        return self.Gyro[0], self.Gyro[1], self.Gyro[2]

    def getMag(self) -> (int, int, int):
        return self.Mag[0], self.Mag[1], self.Mag[2]

    def getTemp(self) -> float:
        return round(self.temp, 2)


if __name__ == '__main__':
    print("\nSense HAT Test Program ...\n")

    imu = IMU()
    while True:
        try:
            imu.refreshAll()

            print("\r\n /-------------------------------------------------------------/")
            print('\r\n Roll = %.2f , Pitch = %.2f , Yaw = %.2f' % (imu.getPitchRollYaw()))
            print('\r\nAcceleration:  X = %d , Y = %d , Z = %d\r\n' % (imu.getAccel()))
            print('\r\nGyroscope:     X = %d , Y = %d , Z = %d\r\n' % (imu.getGyro()))
            print('\r\nMagnetic:      X = %d , Y = %d , Z = %d\r\n' % (imu.getMag()))
            print("QMITemp=%.2f C\r\n" % imu.getTemp())
            time.sleep(0.1)
        except(KeyboardInterrupt):
            print("\n")
            break
