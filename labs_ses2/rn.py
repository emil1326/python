import numpy as np
import serial as ser #type: ignore
import time


class RadioNavigation:
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

    def get_position(self) -> np.ndarray:
        time.sleep(0.1)
        data = str(self.__serial.readline())
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

    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 115200, timeout: float = 0.1):
        import re

        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._serial = None
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

    def send_cmd(self, cmd: bytes, expect_response: bool = False, read_timeout: float | None = None) -> str | None:
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
        """Read one raw line from the device as a decoded string (or None on timeout).

        This implementation polls `in_waiting` and consumes available bytes until
        a newline is seen or the timeout elapses. Using a small default timeout
        avoids long blocking waits when the device doesn't immediately send data.
        """
        if not self.is_open():
            raise RuntimeError("Serial port not open")

        to = timeout if timeout is not None else self._timeout
        end = time.time() + to
        buf = bytearray()

        while time.time() < end:
            try:
                n = self._serial.in_waiting  # type: ignore[attr-defined]
            except Exception:
                n = 0

            if n and n > 0:
                try:
                    chunk = self._serial.read(n)
                except Exception:
                    chunk = b""
                if chunk:
                    buf.extend(chunk)
                    if b"\n" in buf:
                        line, _rest = buf.split(b"\n", 1)
                        return line.decode(errors="replace").strip()
            else:
                # try a short non-blocking read of one byte
                try:
                    b = self._serial.read(1)
                except Exception:
                    b = b""
                if b:
                    buf.extend(b)
                    if b == b"\n":
                        return buf.decode(errors="replace").strip()

            time.sleep(0.01)

        # timeout reached
        if buf:
            return buf.decode(errors="replace").strip()
        return None

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
