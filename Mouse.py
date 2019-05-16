#!/usr/bin/env python

import rospy
import sys
import usb.core
import usb.util
from position_tracking.msg import Mouse_data

# decimal vendor and product values
#dev = usb.core.find(idVendor=10077, idProduct=2982)
#this id is found by using the finddevices code
# or, uncomment the next line to search instead by the hexidecimal equivalent
dev = usb.core.find(idVendor=0x046d, idProduct=0xc084)
#dev = usb.core.find(idVendor=0x275d, idProduct=0xba6)
# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]
# if the OS kernel already claimed the device, which is most likely true
# thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
if dev.is_kernel_driver_active(interface) is True:
  	# tell the kernel to detach
       	dev.detach_kernel_driver(interface)
  	# claim the device
       	usb.util.claim_interface(dev, interface)

md = Mouse_data()
x=0.0
y=0.0
factor = 0.000077244
count=25
#px=0.0
#py=0.0
rospy.init_node('mouse_data', anonymous =True)
publish = rospy.Publisher('mouse_odom', Mouse_data , queue_size = 10)
rate = rospy.Rate(125)

while not rospy.is_shutdown():
        try:
                data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
                if data[5]>=127:      #IF the mouse is moving in the positiv$
                        y=y+(256-data[4])*factor
                else:
                        y=y-data[4]*factor
                if data[3]>=127:      #IF the mouse is moving in the negativ$
                        x=x-(256-data[2])*factor
                else:
                        x=x+(data[2])*factor
        except usb.core.USBError as e:
                data = None
                if e.args == ('Operation timed out',):
                        continue
	count-=1
        if count==0 :
		md.x=round(x,5)
		md.y=round(y,5)
#		px=md.x
#		py=md.y
		x=0.0
		y=0.0
		rospy.loginfo(md)
		publish.publish(md)
		count=25
#		print("!!!!----px={} py={}----!!!!".format(px,py))
	rate.sleep()

# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)
