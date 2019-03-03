#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

def joyStickTeleoperation(data):

	if(data.axes[7] != 0.0):
		# going backward when negative direction
		if(data.axes[7] < 0.0):
			twistmsgs.linear.x = -0.5
			twistmsgs.angular.z = 0.0
			print("going backward!!!!")

		# going forward when positive direction
		elif(data.axes[7] > 0.0):
			twistmsgs.linear.x = 0.5
			twistmsgs.angular.z = 0.0
			print("going forward!!!!!")
		else:
			twistmsgs.linear.x = 0.0
			twistmsgs.angular.z = 0.0
			print("going nowhere!!!!")
	elif(data.axes[6] != 0.0):
		
		# turning right(Anti-clockwise) when negative
		if(data.axes[6] < 0.0):
			twistmsgs.linear.x = 0.0
			twistmsgs.angular.z = -0.5
			print("turing right")
		# turning right (Clockwise) when positive
		elif(data.axes[6] > 0.0):
			twistmsgs.linear.x = 0.0
			twistmsgs.angular.z = 0.5
			print("turning left")
		else:
			twistmsgs.linear.x = 0.0
			twistmsgs.angular.z = 0.0
			print("going nowhere!!!!")
	else:
		twistmsgs.linear.x = 0.0
		twistmsgs.angular.z = 0.0

	pub.publish(twistmsgs)

rospy.init_node("r2m_teleoperation")
twistmsgs = Twist()
sub = rospy.Subscriber("joy", Joy, joyStickTeleoperation)
pub = rospy.Publisher("cmd_vel_mux/r2m_teleoperation", Twist, queue_size=10)
rospy.spin()
