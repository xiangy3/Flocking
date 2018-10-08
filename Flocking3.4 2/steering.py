from panda3d.core import Vec2, Point2 
from math import pi, degrees, radians
from utils import directionInDegrees, directionalVector, clampVectorLength, MAX_VELOCITY,\
	randomBinomial, MAX_ACCELERATION, MAX_ANGULAR_ACCELERATION,\
	clampValue, normalizedDifferenceRadians, distance
from steeringOutput import SteeringOutput
from kinematics import Kinematic

class PlayerAndMovement:
	def __init__(self, kinematic, steerings):
		self.kinematic = kinematic
		if not isinstance(steerings, list):
			self.steerings = [(1, steerings)]
		else:
			self.steerings = steerings
	
	def update(self, dt):
		finalSteeringInstruction = SteeringOutput(Vec2(0,0), 0)
		
		for steering in self.steerings:
			weight = steering[0]
			steeringAlg = steering[1]
			instruction = steeringAlg.getSteering()
			if instruction != None:
				finalSteeringInstruction.linear += instruction.linear * weight
				finalSteeringInstruction.angular += instruction.angular * weight
		self.kinematic.update(dt, finalSteeringInstruction)
		
class SteeringSeek:
	def __init__(self, character, target):
		self.character = character
		self.target = target
		
	def getSteering(self):
		linear = self.target.position - self.character.position
		linear.normalize();
		return SteeringOutput(linear * MAX_ACCELERATION, 0)
		
class SteeringLinear:
	def __init__(self, character):
		self.character = character
	def getSteering(self):
		return None
	
class SteeringSeparate:
	def __init__(self, character, targets, threshold):
		self.character = character
		self.targets = targets
		self.threshold = threshold
		
	def getSteering(self):
		decayCoefficient = MAX_ACCELERATION*4
		
		linear = Vec2(0,0)
		for target in self.targets:
			direction = self.character.position - target.position
			rawDistance= direction.length()
			normalizedDistance = direction.length() / self.threshold
			if rawDistance < self.threshold:
				strength = min(decayCoefficient / (normalizedDistance * normalizedDistance), MAX_ACCELERATION)
				direction.normalize()
				linear += direction * strength
		return SteeringOutput(linear, 0)
	
class SteeringMatchVelocity:
	def __init__(self, character, others):
		self.character = character
		self.targets = others
		
	def getSteering(self):
		sumVelocities = self.character.velocity
		for target in self.targets:
			sumVelocities = sumVelocities + target.velocity
		avgVelocity = sumVelocities / (len(self.targets) + 1.0)
		N = 0
		avgVelocity[0] += N*randomBinomial()
		avgVelocity[1] += N*randomBinomial()
		return SteeringOutput(avgVelocity, 0)

if __name__ == "__main__":
	targetKinematic = Kinematic(Point2(0, 0), 0, 0, None, 0)
