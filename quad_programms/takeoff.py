#!/usr/bin/env python
# -*- coding: utf-8 -*-
# взлет на t секунд на высоту h и посадка
# usage: takeoff.py t h
import rospy
import sys
from clever.srv import *
from std_srvs.srv import Trigger

dh = 0.2 # height tolerance
takeoff_speed = 1 # speed of taking off

rospy.init_node('takeoff')

navigate = rospy.ServiceProxy("navigate",Navigate)
get_telemetry = rospy.ServiceProxy("get_telemetry",GetTelemetry)
land = rospy.ServiceProxy("land",Trigger)

def takeoff(height):
	rospy.wait_for_service("navigate")
	try:
		navigate(x = 0, y = 0, z = height, speed = takeoff_speed,auto_arm = True)
		return 0
	except rospy.ServiceException:
		return -1

def landing(start):
	rospy.wait_for_service("land")
	try:
		land()
		return 0
	except rospy.ServiceException:
		return -1

def usage():
	return "usage: takeoff.py t h"

if __name__ == '__main__':
	if len(sys.argv) == 3:
		t = int(sys.argv[1])
		h = int(sys.argv[2])
		start = get_telemetry()
		if takeoff(h) == 0:
			print("quad is taking off..")
		else:
			print("unable to take off(")
			sys.exit(1)
		while True:
			if get_telemetry().z - start.z >= h - dh:
				break
			rospy.sleep(0.1)
		print("quad has now reached " + str(h) + " metres")	
		rospy.sleep(t)
		if landing(start) == 0:
			print("quad is landing..")
		else:
			print("unable to land(")
			sys.exit(1)
		while True:
			if get_telemetry().armed == False:
				break
			rospy.sleep(0.1)
		print("successful landing!")
	else:
		print usage()
		sys.exit(1)