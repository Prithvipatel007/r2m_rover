#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class Teleoperation:
	def __init__(self):
		rospy.init_node("r2m_teleoperation")
		self.leftAxisVertical = 0.0
		self.leftAxisHorizontal = 0.0
		self.twistmsgs = Twist()
		self.sub = rospy.Subscriber("joy", Joy, self.joystickcallback)
		self.pub = rospy.Publisher("cmd_vel_mux/r2m_teleoperation", Twist, queue_size=10)
		rospy.spin()


	def joystickcallback(self, data):
		self.roverControl(data)
	
	def roverControl(self, data):
		
		self.leftAxisVertical = data.axes[3]
		self.leftAxisHorizontal = data.axes[2]
#		print("leftAxisVertial = " + str(self.leftAxisVertical))
		if(data.buttons[6] == 1):
			if(data.axes[7] != 0.0):
				# going backward when negative direction
				if(data.axes[7] < 0.0):
					if(self.leftAxisVertical < -0.1):
						self.twistmsgs.linear.x = self.leftAxisVertical
						self.twistmsgs.angular.z = 0.0
						print("Going backward at the speed of " + str(self.twistmsgs.linear.x))
					else:
						self.twistmsgs.linear.x = -0.1
						self.twistmsgs.angular.z = 0.0
						print("going backward at the speed of " + str(self.twistmsgs.linear.x))

				# going forward when positive direction
				elif(data.axes[7] > 0.0):
					if(self.leftAxisVertical > 0.1):
						self.twistmsgs.linear.x = self.leftAxisVertical
						self.twistmsgs.angular.z = 0.0
						print("going forward at the speed of " + str(self.twistmsgs.linear.x))
					else:
						self.twistmsgs.linear.x = 0.1
						self.twistmsgs.angular.z = 0.0
						print("going forward at the speed of " + str(self.twistmsgs.linear.x))
	
			elif(data.axes[6] != 0.0):
				# turning right(Anti-clockwise) when negative
				if(data.axes[6] < 0.0):
					if(self.leftAxisHorizontal < -0.1):
						self.twistmsgs.linear.x = 0.0
						self.twistmsgs.angular.z = self.leftAxisHorizontal
						print("turning right at the angle of " + str(self.twistmsgs.angular.z))
						
					else:
						self.twistmsgs.linear.x = 0.0
						self.twistmsgs.angular.z = -0.1
						print("turing right at the angle of " + str(self.twistmsgs.angular.z))
				# turning left (Clockwise) when positive
				elif(data.axes[6] > 0.0):
					if(self.leftAxisHorizontal > 0.1):
						self.twistmsgs.linear.x = 0.0
						self.twistmsgs.angular.z = self.leftAxisHorizontal
						print("turning left at the angle of " + str(self.twistmsgs.angular.z))
					else:
						self.twistmsgs.linear.x = 0.0
						self.twistmsgs.angular.z = 0.1
						print("turning left at the angle of " + str(self.twistmsgs.angular.z))
			else:
				self.twistmsgs.linear.x = 0.0
				self.twistmsgs.angular.z = 0.0
				print("going nowhere!!!!")
			
	
		self.pub.publish(self.twistmsgs)

controller = Teleoperation()


