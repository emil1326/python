import struct
import numpy as np  # type: ignore
import serial as ser  # type: ignore
import time
import threading
import re


class RadioNavigationDep:
    def __init__(self):
        # configurer le serial
        serial = ser.Serial()
        serial.port = "/dev/ttyACM0"
        serial.baudrate = 115200
        serial.bytesize = ser.EIGHTBITS
        serial.parity = ser.PARITY_NONE
        serial.stopbits = ser.STOPBITS_ONE
        serial.timeout = 1

        serial.open()

        # dwm_upd_rate_set TLV request
        # Type = 0x03
        # Length = 0x04 (two 16-bit values: moving_rate, stationary_rate)
        # Value = [0x64, 0x00, 0x64, 0x00] → 100 ms for both
        # (0x0064 = 100 decimal, units are milliseconds)

        request = bytes([0x03, 0x04, 0x64, 0x00, 0x64, 0x00])

        # Send the request
        serial.write(request)

        # Read the response (expect 3 bytes: Type=0x40, Length=0x01, Value=0x00 for success)
        response = serial.read(3)
        print("Response:", response)

        self.__serial = serial

    def demarrer(self):
        try:
            self.__serial.write(b"\r\r")

            time.sleep(1)

            self.__serial.write(b"lep\r")
            return True
        except Exception as e:
            print("Impossible de demarrer la radio navigation", e)
            return False

    def arreter(self):
        self.__serial.close()

    def get_position(self) -> np.ndarray:
        time.sleep(0.1)
        data = str(self.__serial.readline())

        POS = data.split(",")

        print("POS: ", POS)
        print("data: ", data)

        return np.array([0.0, 0.0])


class RadioNavigationV2:
    """Improved RadioNavigation wrapper.

    - configurable serial port and baudrate
    - safe open/close
    - `demarrer()` which verifies response when possible
    - `get_position()` attempts to parse two floats from the device output
    - context manager support

    The exact device response format is unknown, so `get_position` will
    extract numeric tokens from the serial line and return the first two
    as a numpy array. If parsing fails, it returns `None`.
    """

    def __init__(
        self, port: str = "/dev/ttyACM0", baudrate: int = 115200, timeout: float = 0
    ):
        import re

        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._re_float = re.compile(r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")

        try:
            self._serial = ser.Serial()
            self._serial.port = self._port
            self._serial.baudrate = self._baudrate
            self._serial.bytesize = ser.EIGHTBITS
            self._serial.parity = ser.PARITY_NONE
            self._serial.stopbits = ser.STOPBITS_ONE
            self._serial.timeout = self._timeout

            # open only when requested to avoid exceptions during import
            if not self._serial.is_open:
                self._serial.open()
                # Type = 0x03
                # Length = 0x04 (two 16-bit values: moving_rate, stationary_rate)
                # Value = [0x64, 0x00, 0x64, 0x00] → 100 ms for both
                # (0x0064 = 100 decimal, units are milliseconds)

                request = bytes([0x03, 0x04, 0x64, 0x00, 0x64, 0x00])

                # Send the request
                self._serial.write(request)

                # Read the response (expect 3 bytes: Type=0x40, Length=0x01, Value=0x00 for success)
                response = self._serial.read(3)
                print("Response:", response)

                if self._serial is None:
                    raise RuntimeError(
                        f"Serial port {self._port} not open after initialization"
                    )

        except Exception as e:
            # if open failed, leave _serial as None and raise a descriptive error
            self._serial = None
            raise RuntimeError(f"Failed to open serial port {self._port}: {e}") from e

    def is_open(self) -> bool:
        return self._serial is not None and getattr(self._serial, "is_open", False)

    def close(self) -> None:
        try:
            if self._serial is not None and self._serial.is_open:
                self._serial.close()
        except Exception:
            pass

    def send_cmd(
        self,
        cmd: bytes,
        expect_response: bool = False,
        read_timeout: float | None = None,
    ) -> str | None:
        """Send raw bytes to the radio and optionally read one response line."""
        if not self.is_open():
            raise RuntimeError("Serial port not open")

        # flush input to avoid stale data
        try:
            self._serial.reset_input_buffer()
        except Exception:
            pass

        self._serial.write(cmd)
        if expect_response:
            # temporary override timeout if requested
            old_to = self._serial.timeout
            if read_timeout is not None:
                self._serial.timeout = read_timeout
            try:
                raw = self._serial.readline()
                return raw.decode(errors="replace").strip()
            finally:
                if read_timeout is not None:
                    self._serial.timeout = old_to
        return None

    def demarrer(self) -> bool:
        """Start / configure the radio navigation device. Returns True on likely success."""
        if not self.is_open():
            raise RuntimeError("Serial port not open")

        try:
            # wake device
            self._serial.write(b"\r\r")
            time.sleep(0.5)
            # request position mode (device-specific command used previously: 'lep')
            self._serial.write(b"lep\r")
            # read any immediate response
            resp = self._serial.readline()
            if resp:
                try:
                    s = resp.decode(errors="replace").strip()
                    # a simple heuristic: if we get ascii response, assume ok
                    if len(s) > 0:
                        return True
                except Exception:
                    return True
            # if no response, still return True (best-effort)
            return True
        except Exception as e:
            print("Impossible de demarrer la radio navigation", e)
            return False

    def get_raw(self, timeout: float | None = None) -> str | None:
        """Read one raw line from the device as a decoded string (or None on timeout)."""
        if not self.is_open():
            raise RuntimeError("Serial port not open")
        old_to = self._serial.timeout
        if timeout is not None:
            self._serial.timeout = timeout
        try:
            raw = self._serial.readline()
            if not raw:
                return None
            return raw.decode(errors="replace").strip()
        finally:
            if timeout is not None:
                self._serial.timeout = old_to

    def get_position(self) -> np.ndarray | None:
        """Attempt to read a position from the radio and parse two floats (lat, lon).

        Returns a numpy array [f1, f2] on success, or None if parsing fails.
        """
        if not self.is_open():
            raise RuntimeError("Serial port not open")

        raw = self.get_raw(timeout=self._timeout)
        if raw is None:
            return None

        # extract floats
        found = self._re_float.findall(raw)
        # re.findall returns tuples when capture groups present; use finditer for robust extraction
        import re

        floats = [float(m.group(0)) for m in re.finditer(self._re_float, raw)]
        if len(floats) >= 2:
            return np.array([floats[0], floats[1]])
        return None

    # context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            self.close()
        except Exception:
            pass


class RadioNavigation:
    """Simple, readable radio navigation class with a background reader thread.

    - Reader thread calls blocking `readline()` with a short timeout and caches
      the latest parsed position.
    - `get_position()` returns the cached value immediately (or None if stale).
    - Use `send_cmd()` to trigger a response from the device if it supports that.
    """

    def __init__(
        self, port: str = "/dev/ttyACM0", baudrate: int = 115200, timeout: float = 0.1
    ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._serial = None
        self._thread = None
        self._stop = threading.Event()
        self._lock = threading.Lock()

        # cache
        self.last_line = None
        self.last_position = None
        self.last_time = 0.0

        # regex to find floats
        self._float_re = re.compile(r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?")

        try:
            self._serial = ser.Serial()
            self._serial.port = self.port
            self._serial.baudrate = self.baudrate
            self._serial.bytesize = ser.EIGHTBITS
            self._serial.parity = ser.PARITY_NONE
            self._serial.stopbits = ser.STOPBITS_ONE
            self._serial.timeout = self.timeout
            if not self._serial.is_open:
                self._serial.open()

            # set le reader thread
            self._thread = threading.Thread(target=self._reader, daemon=True)

        except Exception as e:
            raise RuntimeError(f"Failed to open serial port {self.port}: {e}") from e

    def _reader(self):
        while not self._stop.is_set() and self._serial is not None:
            try:
                raw = self._serial.readline()
            except Exception:
                raw = b""

            if raw:
                try:
                    line = raw.decode(errors="replace").strip()
                except Exception as e:
                    print("reader en erreur:", e)
                    line = None

                if line:
                    pos = self._parse_line(line)
                    with self._lock:
                        self.last_line = line
                        if pos is not None:
                            self.last_position = pos
                            self.last_time = time.time()

            time.sleep(0.01)

    def _parse_line(self, line: str):
        # return numpy array of first two floats if present
        vals = [m.group(0) for m in self._float_re.finditer(line)]
        if len(vals) >= 2:
            try:
                return np.array([float(vals[0]), float(vals[1])])
            except Exception:
                return None
        return None

    def is_open(self) -> bool:
        return self._serial is not None and getattr(self._serial, "is_open", False)

    def get_position(self, max_age=0.05):
        with self._lock:
            pos = self.last_position
            ts = self.last_time
        return pos

    def demarrer(self):
        try:
            if self._serial is None:
                raise RuntimeError("Serial port not open")
            if self._thread is None:
                raise RuntimeError("Reader thread not initialized")

            data = str(self._serial.readline())

            print("demarrer data", data, "len", len(data))

            time.sleep(1)

            if len(data) == 7:
                self._serial.write(b"\r\r")

                time.sleep(1)

                self._serial.write(b"lep\r")

                time.sleep(1)

            self._thread.start()

            return True
        except Exception as e:
            print("Impossible de demarrer la radio navigation", e)
            return False

    def arreter(self):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=0.5)
        try:
            if self._serial is not None and self._serial.is_open:
                self._serial.close()
                print("serial ferme", not self._serial.is_open)
        except Exception as ex:
            print("impossible de fermer le serial", ex)
            pass

class DWM1001Tag:
    def __init__(self, port="/dev/ttyACM0", baudrate=115200, poll_interval=0.1):
        self.port = port
        self.baudrate = baudrate
        self.poll_interval = poll_interval  # seconds between polls
        self._serial = None
        self._thread = None
        self._running = False
        self._lock = threading.Lock()
        self._last_position = None

    def connect(self):
        """Open the serial port if not already open."""
        if self._serial is None or not getattr(self._serial, "is_open", False):
            # Construct Serial with explicit args to avoid ambiguous initialization
            self._serial = ser.Serial(self.port, self.baudrate, timeout=1)

    def disconnect(self):
        """Close the serial port if open."""
        try:
            if self._serial and getattr(self._serial, "is_open", False):
                self._serial.close()
        except Exception:
            pass
        finally:
            self._serial = None

    def _poll_position(self):
        """Internal loop to poll dwm_loc_get (TLV Type=0x0A)."""
        while self._running:
            try:
                if not self._serial or not getattr(self._serial, "is_open", False):
                    time.sleep(self.poll_interval)
                    continue

                # TLV request: Type=0x0A, Length=0x00
                request = bytes([0x0A, 0x00])
                self._serial.write(request)

                # Read response header first (Type + Length)
                header = self._serial.read(2)
                if len(header) < 2:
                    time.sleep(self.poll_interval)
                    continue

                resp_type, resp_len = header[0], header[1]
                payload = self._serial.read(resp_len)

                # dwm_loc_get response contains position in first 12 bytes (X,Y,Z as int32)
                if resp_type == 0x40 and resp_len >= 12 and len(payload) >= 12:
                    x, y, z = struct.unpack("<iii", payload[:12])
                    pos = np.array([x / 1000.0, y / 1000.0, z / 1000.0])
                    with self._lock:
                        self._last_position = pos
                    print(f"Position: X={x/1000:.2f} m, Y={y/1000:.2f} m, Z={z/1000:.2f} m")

            except Exception as e:
                print("Error polling position:", e)

            time.sleep(self.poll_interval)

    def start(self) -> bool:
        """Start continuous position polling in background thread (compat wrapper: demarrer)."""
        try:
            # ensure serial is open
            self.connect()

            if not self._running:
                self._running = True
                self._thread = threading.Thread(target=self._poll_position, daemon=True)
                self._thread.start()

            print("Started position polling.")
            return True
        except Exception as e:
            print("Impossible de demarrer DWM1001Tag:", e)
            return False

    def stop(self) -> bool:
        """Stop continuous position polling (compat wrapper: arreter)."""
        try:
            self._running = False
            if self._thread:
                self._thread.join(timeout=1.0)
                self._thread = None
            self.disconnect()
            print("Stopped position polling.")
            return True
        except Exception as e:
            print("Impossible d'arreter DWM1001Tag:", e)
            return False

    def get_position(self):
        """Perform a single dwm_loc_get request and return position as numpy array [x,y,z] in meters or None.

        If device is being polled in background, returns the most recently cached position.
        """
        try:
            # If background polling is active, return cached value immediately
            with self._lock:
                if self._last_position is not None:
                    return self._last_position

            # one-shot request
            self.connect()
            request = bytes([0x0A, 0x00])
            self._serial.write(request)

            header = self._serial.read(2)
            if len(header) < 2:
                return None

            resp_type, resp_len = header[0], header[1]
            payload = self._serial.read(resp_len)

            if resp_type == 0x40 and resp_len >= 12 and len(payload) >= 12:
                x, y, z = struct.unpack("<iii", payload[:12])
                return np.array([x / 1000.0, y / 1000.0, z / 1000.0])
            return None
        except Exception as e:
            print("Error getting DWM1001Tag position:", e)
            return None

    # Compatibility methods matching other classes in this file
    def demarrer(self) -> bool:
        return self.start()

    def arreter(self) -> bool:
        return self.stop()

    def is_open(self) -> bool:
        return self._serial is not None and getattr(self._serial, "is_open", False)

    def close(self) -> None:
        self.disconnect()