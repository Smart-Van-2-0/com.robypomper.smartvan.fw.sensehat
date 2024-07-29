#!/usr/bin/python
# -*- coding:utf-8 -*-
import smbus
import math
import time

# i2c address
I2C_ADD_IMU_QMI8658 = 0x6B
I2C_ADD_IMU_AK09918 = 0x0C

Gyro = [0, 0, 0]
Accel = [0, 0, 0]
Mag = [0, 0, 0]
pitch = 0.0
roll = 0.0
yaw = 0.0
pu8data = [0, 0, 0, 0, 0, 0, 0, 0]
U8tempX = [0, 0, 0, 0, 0, 0, 0, 0, 0]
U8tempY = [0, 0, 0, 0, 0, 0, 0, 0, 0]
U8tempZ = [0, 0, 0, 0, 0, 0, 0, 0, 0]
GyroOffset = [0, 0, 0]
Ki = 1.0
Kp = 4.50
q0 = 1.0
q1 = q2 = q3 = 0.0
angles = [0.0, 0.0, 0.0]
true = 0x01
false = 0x00

# define QMI8658 Register
QMI8658_CTRL7_ACC_ENABLE = 0x01
QMI8658_CTRL7_GYR_ENABLE = 0x02

# SPI Interface and Sensor Enable
QMI8658Register_Ctrl1 = 0x02
# Accelerometer control.
QMI8658Register_Ctrl2 = 0x03
# Gyroscope control.
QMI8658Register_Ctrl3 = 0x04
# Data processing settings.
QMI8658Register_Ctrl5 = 0x06
# Sensor enabled status.
QMI8658Register_Ctrl7 = 0x08

# Accelerometer X axis the least significant byte.
QMI8658Register_Ax_L = 0x35
# Accelerometer X axis most significant byte.
QMI8658Register_Ax_H = 0x36
# Accelerometer Y axis the least significant byte.
QMI8658Register_Ay_L = 0x37
# Accelerometer Y axis most significant byte.
QMI8658Register_Ay_H = 0x38
# Accelerometer Z axis the least significant byte.
QMI8658Register_Az_L = 0x39
# Accelerometer Z axis most significant byte.
QMI8658Register_Az_H = 0x3A
# Gyroscope X axis the least significant byte.
QMI8658Register_Gx_L = 0x3B
# Gyroscope X axis most significant byte.
QMI8658Register_Gx_H = 0x3C
# Gyroscope Y axis the least significant byte.
QMI8658Register_Gy_L = 0x3D
# Gyroscope Y axis most significant byte.
QMI8658Register_Gy_H = 0x3E
# Gyroscope Z axis the least significant byte.
QMI8658Register_Gz_L = 0x3F
# Gyroscope Z axis most significant byte.
QMI8658Register_Gz_H = 0x40

# temperature low.
QMI8658Register_Temperature_L = 0x33
# temperature high.
QMI8658Register_Temperature_H = 0x34

# +/- 2g range
QMI8658AccRange_2g = 0x00 << 4
# +/- 4g range
QMI8658AccRange_4g = 0x01 << 4
# +/- 8g range
QMI8658AccRange_8g = 0x02 << 4
# +/- 16g range
QMI8658AccRange_16g = 0x03 << 4

# High resolution 8000Hz output rate.
QMI8658AccOdr_8000Hz = 0x00
# High resolution 4000Hz output rate.
QMI8658AccOdr_4000Hz = 0x01
# High resolution 2000Hz output rate.
QMI8658AccOdr_2000Hz = 0x02
# High resolution 1000Hz output rate.
QMI8658AccOdr_1000Hz = 0x03
# High resolution 500Hz output rate.
QMI8658AccOdr_500Hz = 0x04
# High resolution 250Hz output rate.
QMI8658AccOdr_250Hz = 0x05
# High resolution 125Hz output rate.
QMI8658AccOdr_125Hz = 0x06
# High resolution 62.5Hz output rate.
QMI8658AccOdr_62_5Hz = 0x07
# High resolution 31.25Hz output rate.
QMI8658AccOdr_31_25Hz = 0x08
# Low power 128Hz output rate.
QMI8658AccOdr_LowPower_128Hz = 0x0C
# Low power 21Hz output rate.
QMI8658AccOdr_LowPower_21Hz = 0x0D
# Low power 11Hz output rate.
QMI8658AccOdr_LowPower_11Hz = 0x0E
# Low power 3Hz output rate.
QMI8658AccOdr_LowPower_3Hz = 0x0F

# +-16 degrees per second.
QMI8658GyrRange_16dps = 0 << 4
# +-32 degrees per second.
QMI8658GyrRange_32dps = 1 << 4
# +-64 degrees per second.
QMI8658GyrRange_64dps = 2 << 4
# +-128 degrees per second.
QMI8658GyrRange_128dps = 3 << 4
# +-256 degrees per second.
QMI8658GyrRange_256dps = 4 << 4
# +-512 degrees per second.
QMI8658GyrRange_512dps = 5 << 4
# +-1024 degrees per second.
QMI8658GyrRange_1024dps = 6 << 4
# +-2048 degrees per second.
QMI8658GyrRange_248dps = 7 << 4

# High resolution 8000Hz output rate.
QMI8658GyrOdr_8000Hz = 0x00
# High resolution 8000Hz output rate.
QMI8658GyrOdr_4000Hz = 0x01
# High resolution 8000Hz output rate.
QMI8658GyrOdr_2000Hz = 0x02
# High resolution 8000Hz output rate.
QMI8658GyrOdr_1000Hz = 0x03
# High resolution 8000Hz output rate.
QMI8658GyrOdr_500Hz = 0x04
# High resolution 8000Hz output rate.
QMI8658GyrOdr_250Hz = 0x05
# High resolution 8000Hz output rate.
QMI8658GyrOdr_125Hz = 0x06
# High resolution 8000Hz output rate.
QMI8658GyrOdr_62_5Hz = 0x07
# High resolution 8000Hz output rate.
QMI8658GyrOdr_31_25Hz = 0x08
# define QMI8658 Register  end

# define AK09918 Register
# Company ID
AK09918_WIA1 = 0x00
# Device ID
AK09918_WIA2 = 0x01
# Reserved 1
AK09918_RSV1 = 0x02
# Reserved 2
AK09918_RSV2 = 0x03
# DataStatus 1
AK09918_ST1 = 0x10
# X-axis data
AK09918_HXL = 0x11
AK09918_HXH = 0x12
# Y-axis data
AK09918_HYL = 0x13
AK09918_HYH = 0x14
# Z-axis data
AK09918_HZL = 0x15
AK09918_HZH = 0x16
# Dummy
AK09918_TMPS = 0x17
# Datastatus 2
AK09918_ST2 = 0x18
# Dummy
AK09918_CNTL1 = 0x30
# Control settings
AK09918_CNTL2 = 0x31
# Control settings
AK09918_CNTL3 = 0x32

# Soft Reset
AK09918_SRST_BIT = 0x01
# Sensor Over Flow
AK09918_HOFL_BIT = 0x08
# Data Over Run
AK09918_DOR_BIT = 0x02
# Data Ready
AK09918_DRDY_BIT = 0x01

AK09918_POWER_DOWN = 0x00
AK09918_NORMAL = 0x01
AK09918_CONTINUOUS_10HZ = 0x02
AK09918_CONTINUOUS_20HZ = 0x04
AK09918_CONTINUOUS_50HZ = 0x06
AK09918_CONTINUOUS_100HZ = 0x08
# ignored by switchMode() and initialize(), call selfTest() to use this mode
AK09918_SELF_TEST = 0x10


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

        # Set up for I2C communication
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl1, 0x60)
        # Set acceleration mode 2g 1000Hz
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl2,
                         QMI8658AccRange_2g | QMI8658AccOdr_1000Hz)
        # Set gyro mode 512dps 500Hz
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl3,
                         QMI8658GyrRange_512dps | QMI8658GyrOdr_500Hz)
        # Sensor data processing settings
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl5, 0x00)
        # Enable acceleration and gyroscope sensors
        self._write_byte(self._address_qmi, QMI8658Register_Ctrl7,
                         QMI8658_CTRL7_ACC_ENABLE | QMI8658_CTRL7_GYR_ENABLE |
                         0x80)
        self.QMI8658_GyroOffset()

        if self._read_byte(self._address_ak, AK09918_WIA2) != 0x0C:
            raise IOError("Can't init AK09918 via I2C on address '{}'".format(
                self._address_ak))

        # Reset AK09918
        self._write_byte(self._address_ak, AK09918_CNTL3, AK09918_SRST_BIT)
        # Set magnetometer mode
        self._write_byte(self._address_ak, AK09918_CNTL2,
                         AK09918_CONTINUOUS_20HZ)

    def _read_byte(self, address, cmd):
        return self._bus.read_byte_data(address, cmd)

    def _read_block(self, address, reg, length=1):
        return self._bus.read_i2c_block_data(address, reg, length)

    def _read_u16(self, address, cmd):
        lsb = self._bus.read_byte_data(address, cmd)
        msb = self._bus.read_byte_data(address, cmd + 1)
        return (msb << 8) + lsb

    def _write_byte(self, address, cmd, val):
        self._bus.write_byte_data(address, cmd, val)
        time.sleep(0.0001)

    def QMI8658_Gyro_Accel_Read(self):
        data = self._read_block(self._address_qmi, QMI8658Register_Ax_L, 12)
        Accel[0] = (data[1] << 8) | data[0]
        Accel[1] = (data[3] << 8) | data[2]
        Accel[2] = (data[5] << 8) | data[4]
        Gyro[0] = ((data[7] << 8) | data[6]) - GyroOffset[0]
        Gyro[1] = ((data[9] << 8) | data[8]) - GyroOffset[1]
        Gyro[2] = ((data[11] << 8) | data[10]) - GyroOffset[2]
        # Solve the problem that Python shift will not overflow
        if Accel[0] >= 32767:
            Accel[0] = Accel[0] - 65535
        elif Accel[0] <= -32767:
            Accel[0] = Accel[0] + 65535
        if Accel[1] >= 32767:
            Accel[1] = Accel[1] - 65535
        elif Accel[1] <= -32767:
            Accel[1] = Accel[1] + 65535
        if Accel[2] >= 32767:
            Accel[2] = Accel[2] - 65535
        elif Accel[2] <= -32767:
            Accel[2] = Accel[2] + 65535
        if Gyro[0] >= 32767:
            Gyro[0] = Gyro[0] - 65535
        elif Gyro[0] <= -32767:
            Gyro[0] = Gyro[0] + 65535
        if Gyro[1] >= 32767:
            Gyro[1] = Gyro[1] - 65535
        elif Gyro[1] <= -32767:
            Gyro[1] = Gyro[1] + 65535
        if Gyro[2] >= 32767:
            Gyro[2] = Gyro[2] - 65535
        elif Gyro[2] <= -32767:
            Gyro[2] = Gyro[2] + 65535

    def AK09918_MagRead(self):
        counter = 20
        while counter > 0:
            time.sleep(0.01)
            u8_data = self._read_byte(self._address_ak, AK09918_ST1)
            if (u8_data & 0x01) != 0:
                break
            counter -= 1

        if counter != 0:
            for i in range(0, 8):
                pu8_data = self._read_block(self._address_ak, AK09918_HXL, 8)
                U8tempX[i] = (pu8_data[1] << 8) | pu8_data[0]
                U8tempY[i] = (pu8_data[3] << 8) | pu8_data[2]
                U8tempZ[i] = (pu8_data[5] << 8) | pu8_data[4]
            Mag[0] = (U8tempX[0] + U8tempX[1] + U8tempX[2] + U8tempX[3] +
                      U8tempX[4] + U8tempX[5] + U8tempX[6] + U8tempX[7]) / 8
            Mag[1] = (U8tempY[0] + U8tempY[1] + U8tempY[2] + U8tempY[3] +
                      U8tempY[4] + U8tempY[5] + U8tempY[6] + U8tempY[7]) / 8
            Mag[2] = (U8tempZ[0] + U8tempZ[1] + U8tempZ[2] + U8tempZ[3] +
                      U8tempZ[4] + U8tempZ[5] + U8tempZ[6] + U8tempZ[7]) / 8
        # Solve the problem that Python shift will not overflow
        if Mag[0] >= 32767:
            Mag[0] = Mag[0] - 65535
        elif Mag[0] <= -32767:
            Mag[0] = Mag[0] + 65535
        if Mag[1] >= 32767:
            Mag[1] = Mag[1] - 65535
        elif Mag[1] <= -32767:
            Mag[1] = Mag[1] + 65535
        if Mag[2] >= 32767:
            Mag[2] = Mag[2] - 65535
        elif Mag[2] <= -32767:
            Mag[2] = Mag[2] + 65535

    def QMI8658_readTemp(self):
        temp = self._read_block(I2C_ADD_IMU_QMI8658,
                                QMI8658Register_Temperature_L, 2)
        return float((temp[1] << 8) | temp[0]) / 256.0

    def QMI8658_GyroOffset(self):
        s32_temp_gx = 0
        s32_temp_gy = 0
        s32_temp_gz = 0
        for i in range(0, 32):
            self.QMI8658_Gyro_Accel_Read()
            s32_temp_gx += Gyro[0]
            s32_temp_gy += Gyro[1]
            s32_temp_gz += Gyro[2]
            time.sleep(0.01)
        GyroOffset[0] = s32_temp_gx >> 5
        GyroOffset[1] = s32_temp_gy >> 5
        GyroOffset[2] = s32_temp_gz >> 5

    @staticmethod
    def imu_ahrs_update(gx, gy, gz, ax, ay, az, mx, my, mz):
        ex_int = ey_int = ez_int = 0.0
        half_t = 0.024
        global q0
        global q1
        global q2
        global q3
        q0q0 = q0 * q0
        q0q1 = q0 * q1
        q0q2 = q0 * q2
        q0q3 = q0 * q3
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q3q3 = q3 * q3

        norm = float(1 / math.sqrt(ax * ax + ay * ay + az * az))
        ax = ax * norm
        ay = ay * norm
        az = az * norm

        norm = float(1 / math.sqrt(mx * mx + my * my + mz * mz))
        mx = mx * norm
        my = my * norm
        mz = mz * norm

        # compute reference direction of flux
        hx = 2 * mx * (0.5 - q2q2 - q3q3) + 2 * my * (q1q2 - q0q3) + 2 * mz * (
                q1q3 + q0q2)
        hy = 2 * mx * (q1q2 + q0q3) + 2 * my * (0.5 - q1q1 - q3q3) + 2 * mz * (
                q2q3 - q0q1)
        hz = 2 * mx * (q1q3 - q0q2) + 2 * my * (q2q3 + q0q1) + 2 * mz * (
                0.5 - q1q1 - q2q2)
        bx = math.sqrt((hx * hx) + (hy * hy))
        bz = hz

        # estimated direction of gravity and flux (v and w)
        vx = 2 * (q1q3 - q0q2)
        vy = 2 * (q0q1 + q2q3)
        vz = q0q0 - q1q1 - q2q2 + q3q3
        wx = 2 * bx * (0.5 - q2q2 - q3q3) + 2 * bz * (q1q3 - q0q2)
        wy = 2 * bx * (q1q2 - q0q3) + 2 * bz * (q0q1 + q2q3)
        wz = 2 * bx * (q0q2 + q1q3) + 2 * bz * (0.5 - q1q1 - q2q2)

        # error is sum of cross product between reference direction of fields
        # and direction measured by sensors
        ex = (ay * vz - az * vy) + (my * wz - mz * wy)
        ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
        ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

        if ex != 0.0 and ey != 0.0 and ez != 0.0:
            ex_int = ex_int + ex * Ki * half_t
            ey_int = ey_int + ey * Ki * half_t
            ez_int = ez_int + ez * Ki * half_t

            gx = gx + Kp * ex + ex_int
            gy = gy + Kp * ey + ey_int
            gz = gz + Kp * ez + ez_int

        q0 = q0 + (-q1 * gx - q2 * gy - q3 * gz) * half_t
        q1 = q1 + (q0 * gx + q2 * gz - q3 * gy) * half_t
        q2 = q2 + (q0 * gy - q1 * gz + q3 * gx) * half_t
        q3 = q3 + (q0 * gz + q1 * gy - q2 * gx) * half_t

        norm = float(1 / math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3))
        q0 = q0 * norm
        q1 = q1 * norm
        q2 = q2 * norm
        q3 = q3 * norm

    @staticmethod
    def icm20948CalAvgValue(motion_val):
        motion_val[0] = Gyro[0] / 32.8
        motion_val[1] = Gyro[1] / 32.8
        motion_val[2] = Gyro[2] / 32.8
        motion_val[3] = Accel[0]
        motion_val[4] = Accel[1]
        motion_val[5] = Accel[2]
        motion_val[6] = Mag[0]
        motion_val[7] = Mag[1]
        motion_val[8] = Mag[2]


if __name__ == '__main__':
    print("\nSense HAT Test Program ...\n")
    MotionVal = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    imu = IMU()
    while True:
        try:
            imu.QMI8658_Gyro_Accel_Read()
            imu.AK09918_MagRead()
            imu.icm20948CalAvgValue(MotionVal)
            imu.imu_ahrs_update(MotionVal[0] * 0.0175, MotionVal[1] * 0.0175,
                                MotionVal[2] * 0.0175,
                                MotionVal[3], MotionVal[4], MotionVal[5],
                                MotionVal[6], MotionVal[7], MotionVal[8])
            pitch = math.asin(-2 * q1 * q3 + 2 * q0 * q2) * 57.3
            roll = math.atan2(2 * q2 * q3 + 2 * q0 * q1,
                              -2 * q1 * q1 - 2 * q2 * q2 + 1) * 57.3
            yaw = math.atan2(-2 * q1 * q2 - 2 * q0 * q3,
                             2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3
            print("\r\n /----------------------------"
                  "---------------------------------/ \r\n")
            print('\r\n Roll = %.2f , Pitch = %.2f , Yaw = %.2f\r\n' % (
                roll, pitch, yaw))
            print('\r\nAcceleration:  X = %d , Y = %d , Z = %d\r\n' % (
                Accel[0], Accel[1], Accel[2]))
            print('\r\nGyroscope:     X = %d , Y = %d , Z = %d\r\n' % (
                Gyro[0], Gyro[1], Gyro[2]))
            print('\r\nMagnetic:      X = %d , Y = %d , Z = %d\r\n' % (
                (Mag[0]), Mag[1], Mag[2]))
            print("QMITemp=%.2f C\r\n" % imu.QMI8658_readTemp())
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n")
            break
