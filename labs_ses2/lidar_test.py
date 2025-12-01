import os
import ydlidar
from gab_lidar import Lidar, Models

lidar = Lidar("/dev/ttyUSB0", Models.X4)

ret = lidar.demarrer()
if ret:
    scan = ydlidar.LaserScan()
    while ret and ydlidar.os_isOk() :
        r = lidar.LASER.doProcessSimple(scan);
        if r:
            print("Scan received[",scan.stamp,"]:",scan.points);
        else :
            print("Failed to get Lidar Data.")
lidar.arreter()
