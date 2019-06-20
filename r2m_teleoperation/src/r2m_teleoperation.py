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
		self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
		rospy.spin()


	def joystickcallback(self, data):
		self.roverControl(data)

	def roverControl(self, data):
		# speedConstant = [forward, backward, left, right]
		self.speedConstant = [1.0,1.0,1.0,1.0]
		self.speedControlOffset = 2.0
		#Speed Constant Control Parameters
		if(data.buttons[3] == 1):
			self.speedConstant[0] = self.speedConstant[0] + self.speedControlOffset
			print("Linear Speed increased to ", self.speedConstant[0])
		elif(data.buttons[0] == 1):
			self.speedConstant[1] = self.speedConstant[1] - self.speedControlOffset
			print("Linear Speed decreased to ", self.speedConstant[1])
		elif(data.buttons[2] == 1):
			self.speedConstant[2] = self.speedConstant[2] + self.speedControlOffset
			print("Angular Speed increased to ",self.speedConstant[2])
		elif(data.buttons[1] == 1):
			self.speedConstant[3] = self.speedConstant[3] - self.speedControlOffset
			print("Angular Speed decreased to ",self.speedConstant[3])

		#speed constant control
		self.backwardSpeedConstant = self.speedConstant[1]
		self.forwardSpeedConstant = self.speedConstant[0]
		self.leftSpeedConstant = self.speedConstant[2]
		self.rightSpeedConstant = self.speedConstant[3]

		#axis constant
		self.leftAxisVertical = data.axes[4]
		self.leftAxisHorizontal = data.axes[3]

		if(data.buttons[4] == 1):
			if(data.axes[7] != 0.0):
				# going backward when negative direction
				if(data.axes[7] < 0.0):
					if(self.leftAxisVertical < -0.1):
						self.twistmsgs.linear.x = self.leftAxisVertical * self.backwardSpeedConstant
						self.twistmsgs.angular.z = 0.0
						#print("Going backward at the speed of " + str(self.twistmsgs.linear.x))
					else:
						self.twistmsgs.linear.x = -0.1 * self.backwardSpeedConstant
						self.twistmsgs.angular.z = 0.0
						#print("going backward at the speed of " + str(self.twistmsgs.linear.x))

				# going forward when positive direction
				elif(data.axes[7] > 0.0):
					if(self.leftAxisVertical > 0.1):
						self.twistmsgs.linear.x = self.leftAxisVertical * self.forwardSpeedConstant
						self.twistmsgs.angular.z = 0.0
						#print("going forward at the speed of " + str(self.twistmsgs.linear.x))
					else:
						self.twistmsgs.linear.x = 0.1 * self.forwardSpeedConstant
						self.twistmsgs.angular.z = 0.0
						#print("going forward at the speed of " + str(self.twistmsgs.linear.x))

			elif(data.axes[6] != 0.0):
				# turning right(Anti-clockwise) when negative
				if(data.axes[6] < 0.0):
					if(self.leftAxisHorizontal < -0.1):
						self.twistmsgs.linear.x = 20.0
						self.twistmsgs.angular.z = self.leftAxisHorizontal * self.rightSpeedConstant
						#print("turning right at the angle of " + str(self.twistmsgs.angular.z))

					else:
						self.twistmsgs.linear.x = -20.0
						self.twistmsgs.angular.z = -0.1 * self.rightSpeedConstant
						#print("turing right at the angle of " + str(self.twistmsgs.angular.z))
				# turning left (Clockwise) when positive
				elif(data.axes[6] > 0.0):
					if(self.leftAxisHorizontal > 0.1):
						self.twistmsgs.linear.x = 20.0
						self.twistmsgs.angular.z = self.leftAxisHorizontal * self.leftSpeedConstant
						#print("turning left at the angle of " + str(self.twistmsgs.angular.z))
					else:
						self.twistmsgs.linear.x = 20.0
						self.twistmsgs.angular.z = 0.1 * self.leftSpeedConstant
						#print("turning left at the angle of " + str(self.twistmsgs.angular.z))
			else:
				self.twistmsgs.linear.x = 0.0
				self.twistmsgs.angular.z = 0.0
				#print("going nowhere!!!!")


		self.pub.publish(self.twistmsgs)

if __name__ == "__main__":
	controller = Teleoperation()
