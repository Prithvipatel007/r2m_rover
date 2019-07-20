#!/usr/bin/env python
import rospy
import os
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class Teleoperation:
	def __init__(self):
		rospy.init_node("r2m_teleoperation")
		f = open("/home/iki/r2m_rover/src/r2m_teleoperation/src/data.txt","r")
		self.speed_temp = f.read().split(',')
		#print("Data is  : " , self.speed_temp, " and data type is " , type(self.speed_temp))
		self.speedConstant = [float(x) for x in self.speed_temp]
		f.close()
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
		#self.speedConstant = [25.0,25.0,40.0,40.0]

		# This part of code opens a file called data.dat and
		# reads the array data and assign it to the speedConstant
		# variable!!!
		self.speedControlOffset = 2.0

		#print(self.speedConstant, " and data type is ", type(self.speedConstant)
		#Speed Constant Control Parameters
		if(data.buttons[3] == 1):
			self.speedConstant[0] = self.speedConstant[0] + self.speedControlOffset
			#self.speedConstant_temp[0] = self.speedConstant[0]
			print("Linear Speed increased to ", self.speedConstant[0])
		elif(data.buttons[0] == 1):
			self.speedConstant[0] = self.speedConstant[0] - self.speedControlOffset
			#self.speedConstant_temp[1] = self.speedConstant[1]
			print("Linear Speed decreased to ", self.speedConstant[0])
		elif(data.buttons[2] == 1):
			self.speedConstant[1] = self.speedConstant[1] + self.speedControlOffset
			#self.speedConstant_temp[2] = self.speedConstant[2]
			print("Angular Speed increased to ",self.speedConstant[1])
		elif(data.buttons[1] == 1):
			self.speedConstant[1] = self.speedConstant[1] - self.speedControlOffset
			#self.speedConstant_temp[3] = self.speedConstant[3]
			print("Angular Speed decreased to ",self.speedConstant[1])


		# Changes are updated in the speedConstantDataFile
		#print(self.speedConstant)

		#speed constant control
		self.linearSpeedConstant = self.speedConstant[0]
		self.angularSpeedConstant = self.speedConstant[1]

		#axis constant
		self.leftAxisVertical = data.axes[4]
		self.leftAxisHorizontal = data.axes[3]

		if(data.buttons[4] == 1):
			if(data.axes[7] != 0.0):
				# going backward when negative direction
				if(data.axes[7] < 0.0):
					if(self.leftAxisVertical < -0.1):
						self.twistmsgs.linear.x = self.leftAxisVertical * self.linearSpeedConstant
						self.twistmsgs.angular.z = 0.0
						#print("Going backward at the speed of " + str(self.twistmsgs.linear.x))
					else:
						self.twistmsgs.linear.x = -0.1 * self.linearSpeedConstant
						self.twistmsgs.angular.z = 0.0
						#print("going backward at the speed of " + str(self.twistmsgs.linear.x))

				# going forward when positive direction
				elif(data.axes[7] > 0.0):
					if(self.leftAxisVertical > 0.1):
						self.twistmsgs.linear.x = self.leftAxisVertical * self.linearSpeedConstant
						self.twistmsgs.angular.z = 0.0
						#print("going forward at the speed of " + str(self.twistmsgs.linear.x))
					else:
						self.twistmsgs.linear.x = 0.1 * self.linearSpeedConstant
						self.twistmsgs.angular.z = 0.0
						#print("going forward at the speed of " + str(self.twistmsgs.linear.x))

			elif(data.axes[6] != 0.0):
				# turning right(Anti-clockwise) when negative
				if(data.axes[6] < 0.0):
					if(self.leftAxisHorizontal < -0.1):
						self.twistmsgs.linear.x = 20.0
						self.twistmsgs.angular.z = self.leftAxisHorizontal * self.angularSpeedConstant
						#print("turning right at the angle of " + str(self.twistmsgs.angular.z))

					else:
						self.twistmsgs.linear.x = -20.0
						self.twistmsgs.angular.z = -0.1 * self.angularSpeedConstant
						#print("turing right at the angle of " + str(self.twistmsgs.angular.z))
				# turning left (Clockwise) when positive
				elif(data.axes[6] > 0.0):
					if(self.leftAxisHorizontal > 0.1):
						self.twistmsgs.linear.x = 20.0
						self.twistmsgs.angular.z = self.leftAxisHorizontal * self.angularSpeedConstant
						#print("turning left at the angle of " + str(self.twistmsgs.angular.z))
					else:
						self.twistmsgs.linear.x = 20.0
						self.twistmsgs.angular.z = 0.1 * self.angularSpeedConstant
						#print("turning left at the angle of " + str(self.twistmsgs.angular.z))
			else:
				self.twistmsgs.linear.x = 0.0
				self.twistmsgs.angular.z = 0.0
				#print("going nowhere!!!!")


		self.pub.publish(self.twistmsgs)

if __name__ == "__main__":
	controller = Teleoperation()
