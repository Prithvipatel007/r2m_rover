# R2M_guidelines

This repository is inside the src folder in the catkin workspace for ROS application. This workspace consists of all the ROS packages required to start the Mars Rover prototype and make it move for the competitions like URC, CIRC, and others.

## r2m_teleoperation Package

This package is responsible for the teleoperation of the Rover using Joystick. Acording to the Joy messages that we are getting, we manuipulate these data to publish the Twist messages.