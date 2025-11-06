from ast import main
import threading
import time
import math
from collections import deque
from icm20948 import ICM20948  # type: ignore


class Orientation:
    waitTime = 50  # ms

    class orientationData:
        def __init__(self, ax=0, ay=0, az=0, gx=0, gy=0, gz=0, mx=0, my=0, mz=0):
            self.ax = ax
            self.ay = ay
            self.az = az
            self.gx = gx
            self.gy = gy
            self.gz = gz
            self.mx = mx
            self.my = my
            self.mz = mz

        def __repr__(self):
            return (
                f"orientationData(ax={self.ax!r}, ay={self.ay!r}, az={self.az!r}, "
                f"gx={self.gx!r}, gy={self.gy!r}, gz={self.gz!r}, "
                f"mx={self.mx!r}, my={self.my!r}, mz={self.mz!r})"
            )

    def __init__(self, mag_cal_seconds=5, gx_window_size=50, init_retries=6, retry_delay=0.5):
        print("Initializing ICM20948 IMU...")
        self.imu = None
        # retry loop: le capteur peut répondre de façon intermittente, faire plusieurs tentatives
        for attempt in range(1, init_retries + 1):
            try:
                self.imu = ICM20948()
                break
            except OSError as e:
                print(f"ICM20948 init attempt {attempt}/{init_retries} failed (OSError): {e}")
            except Exception as e:
                print(f"ICM20948 init attempt {attempt}/{init_retries} failed: {e}")
            time.sleep(retry_delay)

        if self.imu is None:
            # échec d'init : lève une erreur claire avec conseils
            raise RuntimeError(
                "Impossible d'initialiser ICM20948 après plusieurs tentatives. "
                "Vérifie : alimentation 3.3V, GND commun, SDA/SCL, bus i2c correct, "
                "pas d'autres processus utilisant le bus. Lance `sudo i2cdetect -y <bus>` "
                "et `dmesg | grep -i i2c`."
            )

        # small delay to let device settle before first reads
        time.sleep(0.05)

        # calibration / bias
        self.calibrating = threading.Event()
        self.calibrationDone = False
        self.mx_offset = 0.0
        self.my_offset = 0.0
        self.mz_offset = 0.0

        self.gx_window = deque(maxlen=gx_window_size)
        # stored in same units as gx (deg/s if gyro_in_deg_per_s True)
        self.gx_bias = 0.0
        # orientation states
        self.estImmobile = threading.Event()
        self.yaw = 0.0  # relative integrated yaw (radians)
        self.mag_heading = 0.0  # heading from magnetometer (radians)

        # thread control
        self._stop = threading.Event()
        self._last_time = None
        self._thread = threading.Thread(target=self._main_loop, daemon=True)

        # calibrate magnetometer at startup
        self._calibrate_magnetometer(seconds=mag_cal_seconds)
        self._thread.start()

    def _read_imu(self):
        imuwork = False
        magwork = False
        ax = ay = az = gx = gy = gz = mx = my = mz = 0
        try:
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            imuwork = True
        except Exception as e:
            print(e)

        time.sleep(0.01)  # small delay to allow I2C bus to recover

        try:
            mx, my, mz = self.imu.read_magnetometer_data()
            magwork = True
        except Exception as e:
            print(e)

        if imuwork and magwork:
            return Orientation.orientationData(ax, ay, az, gx, gy, gz, mx, my, mz)
        elif imuwork:
            return Orientation.orientationData(ax, ay, az, gx, gy, gz, 0, 0, 0)
        elif magwork:
            return Orientation.orientationData(0, 0, 0, 0, 0, 0, mx, my, mz)
        # fallback: zeros
        return Orientation.orientationData()

    def _calibrate_magnetometer(self, seconds=5):
        self.calibrating.set()
        t_end = time.perf_counter() + seconds
        min_mx = min_my = min_mz = float("inf")
        max_mx = max_my = max_mz = float("-inf")
        while time.perf_counter() < t_end:
            d = self._read_imu()
            mx, my, mz = d.mx, d.my, d.mz
            if mx is None or my is None or mz is None:
                time.sleep(0.05)
                continue
            min_mx = min(min_mx, mx)
            max_mx = max(max_mx, mx)
            min_my = min(min_my, my)
            max_my = max(max_my, my)
            min_mz = min(min_mz, mz)
            max_mz = max(max_mz, mz)
            time.sleep(0.05)
        # center offsets
        self.mx_offset = (min_mx + max_mx) / 2.0 if max_mx > min_mx else 0.0
        self.my_offset = (min_my + max_my) / 2.0 if max_my > min_my else 0.0
        self.mz_offset = (min_mz + max_mz) / 2.0 if max_mz > min_mz else 0.0
        self.calibrating.clear()
        self.calibrationDone = True

    def set_immobile(self, immobile: bool):
        if immobile:
            self.estImmobile.set()
            self.gx_window.clear()
        else:
            self.estImmobile.clear()

    def _compute_mag_heading(self, mx, my):
        mx_c = mx - self.mx_offset
        my_c = my - self.my_offset
        return math.atan2(my_c, mx_c)

    def _main_loop(self):
        while not self._stop.is_set():
            now = time.perf_counter()
            dt = (now - self._last_time) if self._last_time is not None else 0.0
            self._last_time = now

            d = self._read_imu()

            # Always compute magnetometer heading (radians)
            try:
                self.mag_heading = self._compute_mag_heading(d.mx, d.my)
            except Exception as e:
                print(e)

            if self.estImmobile:
                # windowed average to compute gx bias
                try:
                    self.gx_window.append(d.gx)
                    if len(self.gx_window) > 0:
                        self.gx_bias = sum(self.gx_window) / len(self.gx_window)
                except Exception as e:
                    print(e)
            else:
                # integrate gx (corrected by bias) to update relative orientation (yaw)
                try:
                    gx = d.gx
                    gx_corrected = gx - self.gx_bias  # same units as input
                    gx_corrected_rad = math.radians(gx_corrected)

                    # integrate: yaw in radians
                    if dt > 0:
                        self.yaw += gx_corrected_rad * dt
                except Exception as e:
                    print(e)

            time.sleep(max(0.0, self.waitTime / 1000.0))

    def stop(self):
        self._stop.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=1.0)
