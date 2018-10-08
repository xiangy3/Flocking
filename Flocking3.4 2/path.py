from pandac.PandaModules import Vec2, Point2
from math import *
from lines import LineSegment
from utils import *

class Path:
	def __init__(self, pts):
		self.segments = []
		self.accumulatedDistance = []
		self.segmentDistance = []
		self.totalDistance = 0
		for i in range(1, len(pts)):
			line = LineSegment(pts[i-1], pts[i])
			self.segments.append(line)
			segmentDistance = line.length()
			self.totalDistance += segmentDistance

			self.segmentDistance.append(segmentDistance)
			self.accumulatedDistance.append(self.totalDistance)

	def getParam(self, pos, lastParam):
		closest = self.segments[0].closestPoint(pos)
		segment = 0
		for i in range(1, len(self.segments)):
			closestToThisSegment = self.segments[i].closestPoint(pos)
			if closestToThisSegment[0] < closest[0]:
				closest = closestToThisSegment
				segment = i
		distanceAlongSegment = distance(self.segments[segment].pt1, closest[1])
		if segment == 0:
			accumulatedDistance = distanceAlongSegment
		else:
			accumulatedDistance = distanceAlongSegment + self.accumulatedDistance[segment-1]
		return accumulatedDistance

	def getPosition(self, param):
		i = 0
		while i < len(self.segmentDistance) and param > self.segmentDistance[i]:
			param -= self.segmentDistance[i]
			i += 1
		
		if i == len(self.segmentDistance):
			return self.segments[-1].pt2
		else:
			return self.segments[i].pointAlongLine(param) 

if __name__ == "__main__":
	path = Path([Point2(100, 100), Point2(200, 200), Point2(300, 100),
				Point2(400, 200), Point2(500, 100), 
				Point2(400, 500), Point2(500, 500)])
	
	trueParam = 0
	while trueParam < 1100:
		pt = path.getPosition(trueParam)
		param = path.getParam(pt, 0)
		print(trueParam, pt, param)
		trueParam += 50