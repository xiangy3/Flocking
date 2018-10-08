from pandac.PandaModules import Vec2, Point2
from math import *
import random

MAX_VELOCITY = 40
MAX_ACCELERATION = 40

MAX_ANGULAR_VELOCITY = pi/8.0
MAX_ANGULAR_ACCELERATION = pi/8.0	

def getRandom(lo, hi):
	delta = hi - lo
	return random.random() * delta + lo

def randomRadians():
	return getRandom(0, 2 * pi)

def normalizedDegrees(degs):
	return degs % 360

def normalizedRadians(rads):
	return rads % (2 * pi)

def directionalVector(rads, speed):
	return Vec2(cos(rads), sin(rads)) * speed

def directionInRadians(vec):
	return atan2(vec.getY(), vec.getX())

def directionInDegrees(vec):
	return degrees(atan2(vec.getY(), vec.getX()))

def relativeDirectionInDegrees(referencePos, otherPos):
	return directionInDegrees(otherPos - referencePos)

def clampVectorLength(vec, maxLength):
	if vec.length() > maxLength:
		vec.normalize();
		vec *= maxLength

def distance(pos1, pos2):
	return (pos1 - pos2).length()

def clampValue(value, lo, hi):
	if value < lo:
		return lo
	elif value > hi:
		return hi
	else:
		return value

def randomBinomial():
	return random.random() - random.random()

def normalizedDifferenceRadians(rads1, rads2):
	return normalizedRadians(normalizedRadians(rads1) - normalizedRadians(rads2))