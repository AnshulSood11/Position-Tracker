#!/usr/bin/env python
import rospy
import FaBo9Axis_MPU9250
import time
import sys
import math
from position_tracking.msg import IMU_data
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

imu_data = IMU_data()
rospy.init_node('imu_data',anonymous=True)
publish = rospy.Publisher('imu_odom', IMU_data, queue_size=10)
rate = rospy.Rate(5)
#count=50
#mx=0
#my=0
#mz=0
while not rospy.is_shutdown():
	try:
#		if count==0:
#			MXAVE=mx/50
#			MYAVE=my/50
#			MZAVE=mz/50
#			print("Xave={} Yave={} Zave={}".format(MXAVE,MYAVE,MZAVE))
#			break
		accel = mpu9250.readAccel()
		imu_data.ax= accel['y'] - 0.055
		imu_data.ay= (-1*accel['x']) - 0.007
		#ax = accel['x']
		#ay = accel['y']
		#az = accel['z']

		gyro = mpu9250.readGyro()
		imu_data.gz= gyro['z'] - 0.009
		#gx = gyro['x']
		#gy = gyro['y']
		#gz = gyro['z']

		hdg = mpu9250.readMagnet()
#		mag = mpu9250.readMagnet()
		sign=1
		if hdg < 0:
			hdg = (-1)*(hdg)
			sign=0
		imu_data.hdg= hdg
		imu_data.sign=sign
#		mx += mag['x']
#		my += mag['y']
#		mz += mag['z']

		#print("ax={} ay={} az={} gx={} gy={} gz={} hdg={}".format(ax,ay,az,gx,gy,gz,hdg))
		#print("mx={} my={} mz={}".format(mag['x'],mag['y'],mag['z']))
#		count-=1
	except KeyboardInterrupt:
			sys.exit()

	rospy.loginfo(imu_data)
	publish.publish(imu_data)
	rate.sleep()
