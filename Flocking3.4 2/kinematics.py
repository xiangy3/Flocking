from panda3d.core import Vec2
from math import sin, cos, degrees, pi
from pandac.PandaModules import Point2
from utils import directionInRadians, clampVectorLength, clampValue, MAX_VELOCITY, \
					MAX_ANGULAR_VELOCITY, normalizedRadians, distance, directionInDegrees, \
					relativeDirectionInDegrees
from steeringOutput import SteeringOutput

class Kinematic:

	def __init__(self, pos, heading, speed, pandaObject, fieldLimit):
		self.halfField = fieldLimit / 2
		self.position = pos
		self.orientation = heading		# orientation may differ from direction of travel
		self.velocity = Vec2(cos(heading), sin(heading)) * speed
		self.rotation = 0				# angular velocity
		self.pandaObject = pandaObject	# 
	
	def update(self, dt, steering):
		if steering == None:
			steering = SteeringOutput(0, 0)

		self.position += self.velocity * dt
		self.orientation += self.rotation * dt
		self.orientation = normalizedRadians(self.orientation)
		
		self.velocity += steering.linear * dt
		self.rotation += steering.angular * dt
		self.orientation = directionInRadians(self.velocity)
		
		clampVectorLength(self.velocity, MAX_VELOCITY)

		self.rotation = clampValue(self.rotation, -MAX_ANGULAR_VELOCITY, MAX_ANGULAR_VELOCITY)
		
		# Perform wrap-around
		if self.position.getX() <= -self.halfField:
			self.position.setX(self.halfField)
		elif self.position.getX() >= self.halfField:
			self.position.setX(-self.halfField)
		elif self.position.getY() <= -self.halfField:
			self.position.setY(self.halfField)
		elif self.position.getY() >= self.halfField:
			self.position.setY(-self.halfField)
			
		self.pandaObject.setPos(self.position.getX(), self.position.getY(), 0)
		self.pandaObject.setH(degrees(self.orientation - (pi / 2.0)))

	def __str__(self):
		return "Pos=%s Vel=%s Orientation=%f" % \
		        (self.position.__str__(), self.velocity.__str__(), self.orientation)

if __name__ == "__main__":
	o1 = Kinematic(Point2(5, 0), pi/4, 5, None, 100)
	o2 = Kinematic(Point2(3, -3), 0.75*pi, 1, None, 100)
	print(o1)
	print(o2)
	print(distance(o1.position, o2.position))
	print(relativeDirectionInDegrees(o1.position, o2.position))
