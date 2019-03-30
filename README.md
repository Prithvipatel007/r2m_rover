# R2M_guidelines

This repository is inside the src folder in the catkin workspace for ROS application. This workspace consists of all the ROS packages required to start the Mars Rover prototype and make it move for the competitions like URC, CIRC, and others.

## r2m_teleoperation Package

This package is responsible for the teleoperation of the Rover using Joystick. According to the Joy messages that we are getting, we manuipulate these data to publish the Twist messages.

## Setup_Ros script
This is the script to install all the basic requirement to access ROS framework. It would he helpful and less time consumption for the installation of the ROS into RPI or any other PC or Laptop.

To run this file, boot the ubuntu any OS and version from Virtual Box or Bootable Pen drive or any other way. Open the terminal of the newly installed OS, and type the following command :

''' ./setup_ros.sh '''

Make sure that the file is executable. Normally, if you type ls -all in the terminal, the file should be in green color or have * at the end of the filename or maybe both. If it is not executable, type the command :

''' chmod +x setup_ros.sh'''

Then, it will install the libraries and tools you need to work with ROS.
