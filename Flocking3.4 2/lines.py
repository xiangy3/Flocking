from pandac.PandaModules import Vec2, Point2
from math import *
from utils import *

class LineSegment:
	def __init__(self, pt1, pt2):
		self.pt1 = pt1
		self.pt2 = pt2
		self.direction = self.pt2 - self.pt1
		
	def length(self):
		return self.direction.length()
	
	def pointAlongLine(self, distance):
		v = Vec2(self.direction)
		v.normalize()
		return self.pt1 + v * distance
	
	def closestPoint(self, pt):
		l2 = pow(self.length(), 2.0)
		dp = (pt - self.pt1).dot(self.pt2 - self.pt1)
		t = max(0.0, min(1.0, dp / l2))
		projection = self.pt1 + (self.pt2 - self.pt1) * t
		dist = distance(pt, projection)
		return (dist, projection)

	def distanceTo(self, pt):
		return self.closestPoint(pt)[1]

if __name__ == "__main__":
	l1 = LineSegment(Point2(2, 2), Point2(3, 3))
#	print(l1.length())
#	print(l1.pointAlongLine(0))
#	print(l1.pointAlongLine(1))
#	print(l1.pointAlongLine(2))
#	print(l1.pointAlongLine(2.23))
	pt = Point2(2.5, 2.5)
	print(l1.closestPoint(pt))
	print(l1.distanceTo(pt))
