# Position-Tracker
- This project was done to help positioning the trotbot - an autonomous delivery bot to be used indoors; developed by the Robotics club, BITS Goa. Since GPS does not work indoors and gives accuracy of >= 5m, this created the need of a positioning system which relied on data from sensors mounted on the bot.

- This position tracker takes data from an optical displacement sensor and an IMU(Inertial Measurement Unit) and fuses them together using a Kalman Filter.

## I used the following components in this project:-
1. Raspberry Pi
2. Logitech G102 gaming mouse
3. MPU9250 (accelerometer, gyroscope and magnetometer)

## The tracker has the following limitations/assumptions:
- The bot is placed on a horizontal surface with no inclination. So, the tracker tracks the postion in 2D only.
- Euler angles are used.

## How to Run :-
- First run IMU.py and Mouse2.py. You should now see data being published on the terminal.
- Then run positionEstimation.py. Now you will see the states of the filter being updated 10 times every second. That is because I have set the time interval between 2 states (dt) as 0.1 sec. You can decrease this interval to increase accuracy though it will cost more processing power.
- Then run server2.py from simpleDAQ on raspi
- Run client2.py on your PC (For this to work, connect your PC to raspi's hotspot). You shall now see real time position of the bot being plotted on your pc's screen (using matplotlib). 
