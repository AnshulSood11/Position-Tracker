import matplotlib.pyplot as plt
import socket               
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
host = '10.42.0.1' # ip of raspberry pi 
port = 12345
s.connect((host, port))
positions = []
# print(s.recv(1024))
# s.close()
xs = []
ys = []
try:
    while True:
        data = s.recv(1024)
        # positions.append(data)
        arr = data.split(b",")
        try:
        	x=float(arr[0])
        except ValueError:
        	x=x
		
        try:
        	y=float(arr[1])
        except ValueError:
        	y=y

        print('x={} y={}'.format(x,y))
        print('\n')
        xs.append(round(x,3))
        ys.append(round(y,3))
        plt.plot(xs,ys,'r-')
        plt.grid()
        plt.xlabel('X')
        plt.ylabel('Y')
        # plt.show()

        plt.pause(0.001)
        # time.sleep(0.1)
except KeyboardInterrupt:
    c.close()
plt.show()
