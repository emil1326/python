from icm20948 import ICM20948

icm = ICM20948()

try:
    mx, my, mz = self.imu.read_magnetometer_data()
    magwork = True
    print("mx", mx, "my", my, "mz", mz)
except Exception as e:
    print(e)