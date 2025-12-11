import struct
from urllib import request
import numpy as np  # type: ignore
import serial as ser  # type: ignore
import time
import threading
import re
import math

class RadioNavigation:
    #fait par Gabriel PEreira Levesque

    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._serial = None
        self._thread = None
        self._stop = threading.Event()
        self._lock = threading.Lock()

        # cache
        self.last_position = None

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
        while not self._stop.is_set():
            try:
                raw = self._serial.readline()
                #print("reader raw", raw)
            except Exception as e:
                print("probleme dans readline", e)
                raw = b""

            if raw:
                try:
                    line = raw.decode(errors="replace").strip()
                except Exception as e:
                    print("reader en erreur:", e)
                    line = None

                if line:
                    self.last_position = self._parse_line(line)
                else:
                    print("!!! reader - no line")
            else:
                print("!!! reader - no raw")

            time.sleep(0.1)

    def _parse_line(self, line: str):
        # return numpy array of first two floats if present
        vals = [m.group(0) for m in self._float_re.finditer(line)]
        if len(vals) >= 2:
            try:
                #print("_parse_line -- vals", str(vals))
                return np.array([float(vals[0]), float(vals[1])])
            except Exception:
                return None
        return None

    def is_open(self) -> bool:
        return self._serial is not None and getattr(self._serial, "is_open", False)

    def get_position(self): 
        '''
            retourne un tableau [x, y]
        '''       
        
        return self.last_position
    
    def get_distance(self, posA, posB):
        '''
            posA et posB: tableau [x, y]
            
            retourne un distance en m
        '''
        if posA is not None or posB is not None:
            try:
                x1 = posA[0]
                x2 = posB[0]
                y1 = posA[1]
                y2 = posB[1]
                distance = math.sqrt(math.pow((x2-x1), 2)+math.pow((y2-y1),2))
                #print("distance parcourue: ", distance, "m")
                return distance
            except Exception as e:
                print("!!! error get_distance: ", e)
                return None
        else:
            #print('posA ou B sont None | posA: ', posA, 'posB: ', posB)
            return None

    def demarrer(self):
        try:
            if self._serial is None:
                raise RuntimeError("Serial port not open")
            if self._thread is None:
                raise RuntimeError("Reader thread not initialized")
            
            time.sleep(1)

            data = self._serial.readline().decode(errors="replace").strip()            
            
            print("demarrer data", data, "len", len(data))
            
            time.sleep(1)
            
            if not data.__contains__("POS"):  
                self._serial.write(b"\r\r")   
                
                time.sleep(1)
                             
                self._serial.write(b"lep\n")
                print("data ne contient pas POS")

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
                    print(
                        f"Position: X={x/1000:.2f} m, Y={y/1000:.2f} m, Z={z/1000:.2f} m"
                    )

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


class TLVRadioNavigation:
    """Simple, readable radio navigation class with a background reader thread.

    - Reader thread calls blocking `readline()` with a short timeout and caches
      the latest parsed position.
    - `get_position()` returns the cached value immediately (or None if stale).
    - Use `send_cmd()` to trigger a response from the device if it supports that.
    """

    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 115200, timeout=1):
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
                request = bytes([0x02, 0x00])
                self._serial.write(request)

                time.sleep(0.2)

                raw = self._serial.readline()
                # print("reader raw", raw)
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
                print("_parse_line -- vals", str(vals))
                return np.array([float(vals[0]), float(vals[1])])
            except Exception:
                return None
        return None

    def is_open(self) -> bool:
        return self._serial is not None and getattr(self._serial, "is_open", False)

    def get_position(self):
        pos = self.last_position
        ts = self.last_time
        return pos

    def demarrer(self):
        try:
            if self._serial is None:
                raise RuntimeError("Serial port not open")
            if self._thread is None:
                raise RuntimeError("Reader thread not initialized")

            # try to quit shell mode
            self._serial.write(b"quit \r")

            time.sleep(1)
            request = bytes([0x02, 0x00])
            self._serial.write(request)

            time.sleep(0.2)

            print("pos is", self._serial.read_all())

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
