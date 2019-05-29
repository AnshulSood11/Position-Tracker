#!/usr/bin/env python
import rospy
import math
from position_tracking.msg import *
from filterpy.kalman import KalmanFilter
import numpy as np
from scipy.linalg import block_diag
from filterpy.common import Q_discrete_white_noise

fd = Filter_data()
rospy.init_node('filter', anonymous=True)
publish = rospy.Publisher('filter_output', Filter_data , queue_size = 10)
sign = 0
z = np.empty(shape=(6,1))
trotbot_tracker = KalmanFilter(dim_x=8, dim_z=6)

def mousecb(data):
#	rospy.loginfo(data)
	z[0] = data.x
	z[2] = data.y

def imucb(data):
#	rospy.loginfo(data)
	z[1] = data.ax
	z[3] = data.ay
	z[4] = data.hdg
	z[5] = data.gz
	global sign
	sign = data.sign

def subscribe():

	rospy.Subscriber('mouse_odom',Mouse_data,mousecb)
	rospy.Subscriber('imu_odom',IMU_data,imucb)
	timer = rospy.Timer(rospy.Duration(0.2),run)
	rospy.spin()
	timer.shutdown()

def init_tracker(tracker):

	dt = 0.2   # time step 0.2 second
	dt2 = dt*dt;
	g = 9.96 #in m/s^2
	var_mouse = 0.01 ** 2 #in metres
	var_hdg = 0.005 ** 2
	var_ang_vel =0.002  ** 2
	var_acceleration = (0.01*g)**2
	tracker.F = np.array([[1, dt, .5*dt2,  0, 0, 0, 0, 0],
	                      [0,  1, dt, 0, 0, 0, 0, 0],
	                      [0,  0, 1, 0, 0, 0, 0, 0],
	                      [0,  0, 0,  1, dt, .5*dt2, 0, 0],
	                      [0, 0, 0, 0, 1, dt, 0, 0],
	                      [0, 0, 0, 0, 0, 1, 0, 0],
	                      [0, 0, 0, 0, 0, 0, 1, dt],
			      		  [0, 0, 0, 0, 0, 0, 0, 1]])


	q1 = Q_discrete_white_noise(dim=3, dt=dt, var=g*(0.1))	#In practice we pick a number, run simulations on data, and choose a value that works well.
	q2 = block_diag(q1,q1);
	q3 = Q_discrete_white_noise(dim=2, dt=dt, var=1)
	tracker.Q = block_diag(q2, q3)

	tracker.H = np.array([[0, dt, 0, 0, 0, 0, 0, 0],  #matrix to transform from state space to measurement space.
	                      [0, 0, 1/g, 0, 0, 0, 0, 0],
	                      [0, 0, 0, 0, dt, 0, 0, 0],
	                      [0, 0, 0, 0, 0, 1/g, 0, 0],
	                      [0, 0, 0, 0, 0, 0, 1, 0],
	                      [0, 0, 0, 0, 0, 0, 0, 1]])

	tracker.R = np.array([[var_mouse, 0, 0, 0, 0, 0],
	                      [0,var_acceleration, 0, 0, 0, 0],
	                      [0, 0,var_mouse, 0, 0, 0],
	                      [0, 0, 0,var_acceleration, 0, 0],
	                      [0, 0, 0, 0, var_hdg, 0],
	                      [0, 0, 0, 0, 0, var_ang_vel]])
	
	tracker.x = np.array([[0, 0, 0, 0, 0, 0, 0, 0]]).T #initial state when bot starts from starting point. check for theta (magnetometer measurement)
	tracker.P = np.array([[0.1 **2, 0, 0, 0, 0, 0, 0, 0], #initial uncertainity in x_coordinate = +-10 m
				[0, 0.1**2, 0, 0, 0, 0, 0, 0],
				[0, 0, (g*0.01)**2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0.1**2, 0, 0, 0, 0],
				[0, 0, 0, 0, 0.1**2, 0 , 0, 0],
				[0, 0, 0, 0, 0, (g*0.01)**2, 0, 0],
				[0, 0, 0, 0, 0, 0, 6.279**2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0.01**2]])

	return tracker
def transform(z): #Transforms the measurements from the bot frame to the tracker frame
	global sign
	if sign == 1:
		# When heading is positive
		k = z[0]*math.cos(trotbot_tracker.x[6])-z[2]*math.sin(trotbot_tracker.x[6])
		l = z[1]*math.cos(trotbot_tracker.x[6])-z[3]*math.sin(trotbot_tracker.x[6])
		m = z[2]*math.cos(trotbot_tracker.x[6])+z[0]*math.sin(trotbot_tracker.x[6])
		n = z[3]*math.cos(trotbot_tracker.x[6])+z[1]*math.sin(trotbot_tracker.x[6])
	else :
		# When heading is negative
        k = z[0]*math.cos(trotbot_tracker.x[6])+z[2]*math.sin(trotbot_tracker.x[6])
        l = z[1]*math.cos(trotbot_tracker.x[6])+z[3]*math.sin(trotbot_tracker.x[6])
        m = z[2]*math.cos(trotbot_tracker.x[6])-z[0]*math.sin(trotbot_tracker.x[6])
        n = z[3]*math.cos(trotbot_tracker.x[6])-z[1]*math.sin(trotbot_tracker.x[6])
	
	z[0]=k
    z[1]=l
    z[2]=m
    z[3]=n
	return z

def run(event):
	trotbot_tracker.predict()
#	new data is subscribed automatically.
	zt = transform(z)
	trotbot_tracker.update(zt)
#	print '\n -----Filter output-----at'+str(event.current_real)
#	st = 'x={} vx={} ax={} y={} vy={} ay={} hdg={} angvel={}'
#	print st.format(*trotbot_tracker.x)
	fd.x=round(trotbot_tracker.x[0],3)
	fd.vx=round(trotbot_tracker.x[1],3)
	fd.ax=round(trotbot_tracker.x[2],3)
	fd.y=round(trotbot_tracker.x[3],3)
	fd.vy=round(trotbot_tracker.x[4],3)
	fd.ay=round(trotbot_tracker.x[5],3)
	fd.hdg=round(trotbot_tracker.x[6],3)
	fd.angvel=round(trotbot_tracker.x[7],3)

	rospy.loginfo(fd)
	publish.publish(fd)
	# print filter output and relay it to actuator controlling node
if __name__=='__main__':
	init_tracker(trotbot_tracker)
	subscribe()