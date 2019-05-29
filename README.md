# Position-Tracker
- This project was done to help positioning the trotbot - an autonomous delivery bot to be used indoors; developed by the Robotics club, BITS Goa. Since GPS does not work indoors and gives accuracy of >= 5m, this created the need of a positioning system which relied on data from sensors mounted on the bot.

- This position tracker takes data from an optical mouse sensor and an IMU(Inertial Measurement Unit) and fuses them together using a Kalman Filter.

## I used the following components in this project:-
1. Raspberry Pi
2. Logitech G102 gaming mouse
3. MPU9250 (accelerometer, gyroscope and magnetometer)

## The tracker has the following limitations/assumptions:
- The bot is placed on a horizontal surface with no inclination. So, the tracker tracks the postion in 2D only.
- Euler angles are used.
