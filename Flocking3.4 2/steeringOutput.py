
class SteeringOutput:
	def __init__(self, acceleration, angluarVelocity):
		self.linear = acceleration
		self.angular = angluarVelocity
		
	def __str__(self):
		return "(%s,%f)" % (self.linear.__str__(), self.angular)
