#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class Teleoperation:
	def __init__(self):
		rospy.init_node("r2m_teleoperation")
		self.twistmsgs = Twist()
		self.sub = rospy.Subscriber("joy", Joy, self.joystickcallback)
		self.pub = rospy.Publisher("cmd_vel_mux/r2m_teleoperation", Twist, queue_size=10)
		rospy.spin()


	def joystickcallback(self, data):
		self.roverControl(data)
	
	def roverControl(self, data):
		if(data.buttons[6] == 1):
			if(data.axes[7] != 0.0):
				# going backward when negative direction
				if(data.axes[7] < 0.0):
					self.twistmsgs.linear.x = -0.5
					self.twistmsgs.angular.z = 0.0
					print("going backward!!!!")

				# going forward when positive direction
				elif(data.axes[7] > 0.0):
					self.twistmsgs.linear.x = 0.5
					self.twistmsgs.angular.z = 0.0
					print("going forward!!!!!")
			elif(data.axes[6] != 0.0):
		
				# turning right(Anti-clockwise) when negative
				if(data.axes[6] < 0.0):
					self.twistmsgs.linear.x = 0.0
					self.twistmsgs.angular.z = -0.5
					print("turing right")
				# turning right (Clockwise) when positive
				elif(data.axes[6] > 0.0):
					self.twistmsgs.linear.x = 0.0
					self.twistmsgs.angular.z = 0.5
					print("turning left")
			else:
				self.twistmsgs.linear.x = 0.0
				self.twistmsgs.angular.z = 0.0
				print("going nowhere!!!!")
			
	
		self.pub.publish(self.twistmsgs)

controller = Teleoperation()


