#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import sys
import math
from clever.srv import *
from std_srvs.srv import Trigger

takeoff_speed = 1 # speed of taking off

navigate = rospy.ServiceProxy("navigate",Navigate)
get_telemetry = rospy.ServiceProxy("get_telemetry",GetTelemetry)
land = rospy.ServiceProxy("land",Trigger)
set_position = rospy.ServiceProxy('set_position', SetPosition)

def telemetry():
	rospy.wait_for_service("get_telemetry")
	try:
		return get_telemetry()
	except rospy.ServiceException:
		print("unable to get telemetry")
		return -1

def takeoff(height):
	rospy.wait_for_service("navigate")
	try:
		print("quad is taking off..")
		navigate(x = 0, y = 0, z = height, speed = takeoff_speed,auto_arm = True)
		return 0
	except rospy.ServiceException:
		print("unable to take off")
		return -1

def set_pos(posX,posY,posZ):
	rospy.wait_for_service("set_position")
	try:
		set_position(x = posX, y = posY, z = posZ)
		return 0
	except rospy.ServiceException:
		print("unable to set position")
		return -1


def landing():
	rospy.wait_for_service("land")
	try:
		print("quad is landing..")
		land()
		return 0
	except rospy.ServiceException:
		print("unable to land")
		return -1