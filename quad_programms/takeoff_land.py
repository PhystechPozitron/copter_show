#!/usr/bin/env python
# -*- coding: utf-8 -*-

# взлет на t секунд на высоту h и посадка
# usage: takeoff_land.py h t

import rospy
import sys
import quad

dh = 0.3 # height tolerance

rospy.init_node('foo')

def usage():
    return "usage: takeoff_land.py t h"

if __name__ == '__main__':
    if len(sys.argv) == 3:
        t = int(sys.argv[2])
        h = float(sys.argv[1])

        start = quad.telemetry()
        if quad.takeoff(h) != 0:
            sys.exit(1)
        while True:
            if quad.telemetry().z - start.z >= h - dh :
                break
            rospy.sleep(0.1)
        print("quad has now reached " + str(int(round(h - dh))) + " metres") 

        rospy.sleep(t)

        if quad.landing() != 0:
            sys.exit(1)
        while True:
            if quad.telemetry().armed == False:
                break
            rospy.sleep(0.1)
        print("successful landing!")
    else:
        print usage()
        sys.exit(1)