#!/usr/bin/env python
import socket
import time
import rospy
from position_tracking.msg import *

s = socket.socket()
host = ''
port = 12345
s.bind((host, port))

s.listen(1)
c, addr = s.accept()

# while True:
#   c, addr = s.accept()
#   print ('Got connection from',addr)
#   c.send('Thank you for connecting')
#   c.close()

rospy.init_node('filter_client',anonymous=True)
x=0
y=0
def filtercb(data):
    rospy.loginfo(data)
    global x,y
    x = data.x
    y = data.y

def subscribe():
    rospy.Subscriber('filter_output',Filter_data,filtercb)
    timer = rospy.Timer(rospy.Duration(0.2),send_position)
    rospy.spin()
    timer.shutdown()

def send_position(event):
    try:
        # transmitter.sendDataPoint(x,y)
        c.send((x,y))
    except KeyboardInterrupt:
        # transmitter.signalEnd()
        c.close()
if __name__=='__main__':
	print ('Got connection from',addr)
	print('c=',c)
	subscribe()