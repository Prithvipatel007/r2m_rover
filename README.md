# R2M_guidelines

This repository is inside the src folder in the catkin workspace for ROS application. This workspace consists of all the ROS packages required to start the Mars Rover prototype and make it move for the competitions like URC, CIRC, and others.

## r2m_teleoperation Package

This package is responsible for the teleoperation of the Rover using Joystick. Acording to the Joy messages that we are getting, we manuipulate these data to publish the Twist messages.

## r2m_simulation Package

This package is responsible for the simulation of the Rover in ROS within Gazebo and rViz.

### Launch Simulation

To launch the simulation in the mars environment
```bash
roslaunch curiosity_mars_rover_description main_real_mars.launch 
```

To launch the simulation in the simple environment
```bash
roslaunch curiosity_mars_rover_description main_simple_mars.launch 
```

### Speed Control
Full control over the suspension and wheels. You can change the suspension configuration and move the robot through a
simple /cmd_vel topic publish.
To launch the keyboard control of the robot
```bash
rosrun teleop_twist_keyboard teleop_twist_keyboard.py 
```
You will see the instruction on the terminal.


If the environment is too dark in gazebo, unable the shadows property.(World/Scene/shadows)
