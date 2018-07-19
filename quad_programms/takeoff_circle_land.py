#!/usr/bin/env python
# -*- coding: utf-8 -*-

# взлет на высоту h, облет локальной точки (x,y) N раз и посадка
# usage: takeoff_circle_land.py h x y N

import rospy
import sys
import quad
import math

dh = 0.3 # height tolerance
r_min = 1 # minimum radius of rotation (m)
ang_speed = 0.3 # (rad/s)

rospy.init_node("foo")

def radius_and_angle(dx,dy):
	r = math.sqrt( dx**2 + dy**2 )
	if r > 0:
		if dy >= 0:
			angle = math.acos(dx/r)
		else:
			angle = 2*math.pi - math.acos(dx/r) 
		return r,angle	
	else:
		return 0,0


def usage():
	return "usage: takeoff_circle_land.py h x y N"

if __name__ == '__main__':
	if len(sys.argv) == 5:
		h = float(sys.argv[1])
		x = float(sys.argv[2])
		y = float(sys.argv[3])
		N = int(sys.argv[4])

		start = quad.telemetry()
		if quad.takeoff(h) != 0:
			sys.exit(1)

		while True:
			if quad.telemetry().z - start.z >= h - dh:
				break
			rospy.sleep(0.1)
		
		count = 0
		start = quad.telemetry()
		radius, start_angle = radius_and_angle(start.x - x, start.y - y)

		if (N > 0) and (radius >= r_min):
			print("quad is flying around (" + str(x) + ";" + str(y) + ")")
			while count < N:
				angle = start_angle
				while angle - start_angle <= 2*math.pi:
					angle += 0.1 * ang_speed
					posX = x + radius*math.cos(angle)
					posY = y + radius*math.sin(angle) 
					s = quad.set_pos(posX,posY,start.z)
					if s != 0:
						sys.exit(1)

					rospy.sleep(0.1)
			
				count += 1

		rospy.sleep(6)
		if quad.landing() != 0:
			sys.exit(1)

	else:
		print usage()
		sys.exit(1)


