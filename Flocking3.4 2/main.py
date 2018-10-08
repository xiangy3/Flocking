from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import OrthographicLens, TransparencyAttrib, loadPrcFileData, Point2, LVector3
from direct.task import Task
import random, sys, time
from utils import *
from kinematics import Kinematic
from steering import *
from path import *

WINDOW_SZ = 700
AVATAR_RAD = 10

# This helps reduce the amount of code used by loading objects, since all of
# the objects are pretty much the same.
def loadObject(tex, scale, color):
	global loader, camera, render
	# Every object uses the plane model and is parented to the camera
	# so that it faces the screen.
	obj = loader.loadModel("models/plane")
	obj.reparentTo(render)
	obj.setP(-90)

	obj.setScale(scale)
	
	# This tells Panda not to worry about the order that things are drawn in
	# (ie. disable Z-testing).  This prevents an effect known as Z-fighting.
	obj.setBin("unsorted", 0)
	obj.setDepthTest(False)
	obj.setTransparency(TransparencyAttrib.MAlpha)
	
	tex = loader.loadTexture('textures/' + tex)
	obj.setTexture(tex, 1)
	obj.setColor(color)
	
	return obj

class MovementDemo(ShowBase):
		
	def startupSeparateOne(self):
		speed = random.random() * 45 + 5

		numObjects = 50
		kinematics = []

		# Create the kinematics		
		for i in range(numObjects):
			if i == 0:
				targetColor = (0, 1, 0, 1)
			else:
				targetColor = (1, 1, 1, 1)
			pandaObject = loadObject("ship.png", 2*AVATAR_RAD, targetColor)
			kinematic = Kinematic(Point2(0, 0), 0, speed, pandaObject, WINDOW_SZ)
			kinematics.append(kinematic)

		self.steeringObjects = []
		# Create the steering objects		
		for i in range(len(kinematics)):
			thisKinematic = kinematics[i]
			otherKinematics = kinematics[0:i] + kinematics[i+1:]
			if i == 0:
				steering = SteeringSeparate(thisKinematic, otherKinematics, 100)
			else:
				steering = SteeringLinear(thisKinematic)
			self.steeringObjects.append(PlayerAndMovement(thisKinematic, steering))

	def startupPerformMany(self):
		speed = random.random() * 45 + 5
		colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1),
					(1, 1, 0, 1), (0, 1, 1, 1), (1, 0, 1, 1)]

		numObjects = 50
		kinematics = []

		# Create the kinematics		
		for i in range(numObjects):
			targetColor = colors[i % len(colors)]
			pandaObject = loadObject("ship.png", 2*AVATAR_RAD, targetColor)
			kinematic = Kinematic(Point2(0, 0), 0, speed, pandaObject, WINDOW_SZ)
			kinematics.append(kinematic)

		self.steeringObjects = []
		# Create the steering objects		
		for i in range(len(kinematics)):
			thisKinematic = kinematics[i]
			otherKinematics = kinematics[0:i] + kinematics[i+1:]
			separate = SteeringSeparate(thisKinematic, otherKinematics, 100)
			matchVelocity = SteeringMatchVelocity(thisKinematic, otherKinematics)
			self.steeringObjects.append(PlayerAndMovement(thisKinematic, separate))
#			self.steeringObjects.append(PlayerAndMovement(thisKinematic, matchVelocity))
#			self.steeringObjects.append(PlayerAndMovement(thisKinematic, [(0.5, separate), (0.5, matchVelocity)]))
			
	def startupDetective(self):
		speed = random.random() * 45 + 5

		numObjects = 50
		kinematics = []

		# Create the kinematics		
		for i in range(numObjects):
			if i == 0:
				targetColor = (1, 0, 0, 1)
			elif i == 1:
				targetColor = (0, 1, 0, 1)
			else:
				targetColor = (0.8, 0.8, 0.8, 1)
			pandaObject = loadObject("ship.png", 2*AVATAR_RAD, targetColor)
			kinematic = Kinematic(Point2(0, 0), 0, speed, pandaObject, WINDOW_SZ)
			kinematics.append(kinematic)

		self.steeringObjects = []
		# Create the steering objects		
		for i in range(len(kinematics)):
			thisKinematic = kinematics[i]
			if i == 0:
				otherKinematics = kinematics[2:i] + kinematics[i+1:]
				steering1 = SteeringSeparate(thisKinematic, otherKinematics, 100)
				steering2 = SteeringSeek(thisKinematic, kinematics[1])
				self.steeringObjects.append(PlayerAndMovement(thisKinematic,
														[(0.5, steering1),(0.5, steering2)]))
			else:
				steering = SteeringLinear(thisKinematic)
				self.steeringObjects.append(PlayerAndMovement(thisKinematic, steering))
		
	def __init__(self):
		global taskMgr, base
		# Initialize the ShowBase class from which we inherit, which will
		# create a window and set up everything we need for rendering into it.
		ShowBase.__init__(self)
		
		lens = OrthographicLens()
		lens.setFilmSize(WINDOW_SZ, WINDOW_SZ)
		base.cam.node().setLens(lens)

		# Disable default mouse-based camera control.  This is a method on the
		# ShowBase class from which we inherit.
		self.disableMouse()
		
		# point camera down onto x-y plane
		camera.setPos(LVector3(0, 0, 1))
		camera.setP(-90)
		
		self.setBackgroundColor((0, 0, 0, 1))
		self.bg = loadObject("stars.jpg", WINDOW_SZ, (0, 0, 0, 1))
		
		self.accept("escape", sys.exit)  # Escape quits
		self.accept("space", self.newGame, [])  # Escape quits
		
		self.startupSeparateOne()
		#self.startupPerformMany()
		#self.startupDetective()
				
		self.newGame()
		
		self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")

	def gameLoop(self, task):
		global globalClock
		dt = globalClock.getDt()
		for obj in self.steeringObjects:
			obj.update(dt)
		return Task.cont
		
	def newGame(self):
		for obj in self.steeringObjects:
			speed = getRandom(20, 50)
			obj.kinematic.position = Point2(getRandom(-WINDOW_SZ/2.0, 0), getRandom(-WINDOW_SZ/2.0, 0))
			orientation = randomRadians()
			obj.kinematic.orientation = orientation
			obj.kinematic.velocity = directionalVector(orientation, speed) 

loadPrcFileData("", "win-size %d %d" % (WINDOW_SZ, WINDOW_SZ))
demo = MovementDemo()
demo.run()
