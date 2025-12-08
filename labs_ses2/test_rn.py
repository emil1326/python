#!/usr/bin/env python3
"""Minimal test for the `DWM1001Tag` class in `labs_ses2.rn`.

This script does not take command-line arguments. It uses the class
defaults from `rn.DWM1001Tag` (port, baudrate) and performs two checks:
  1) a one-shot `get_position()`
  2) start background polling for a short time, then read cached value

Run from PowerShell:
  python .\labs_ses2\test_rn.py

The script is defensive and prints errors instead of raising.
"""
import time

from rn import DWM1001Tag


def run_test():
    print("Testing DWM1001Tag using defaults from rn.DWM1001Tag")
    try:
        tag = DWM1001Tag()  # uses defaults declared in rn.py
        print("Default port:", tag.port, "baudrate:", tag.baudrate)

        print("\n-- One-shot get_position() --")
        try:
            tag.connect()
            print("connected:", tag.is_open())
            pos = tag.get_position()
            print("one-shot position:", pos)
        finally:
            tag.disconnect()

        print("\n-- Background polling (2s) --")
        try:
            ok = tag.start()
            print("start returned:", ok)
            time.sleep(2.0)
            pos = tag.get_position()
            print("cached position after polling:", pos)
        finally:
            tag.stop()

    except Exception as e:
        print("Error during DWM1001Tag test:", e)


if __name__ == '__main__':
    run_test()
