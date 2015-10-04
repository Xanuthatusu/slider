import random, solver

class SliderLogic():
	def __init__(self, size):
		self.solver = solver.SliderSolver(size)
		self.size = size
		self.restart()
		self.shuffle(1)
		self.countMoves = 0

	def restart(self):
		self.list = []
		for i in range(self.size**2):
			self.list.append(i)
		self.list[-1] = -1
		self.hole = self.list[-1]
		self.solver.reset()

	def legalNeighbors(self):
		legal = []
		self.holePos = [i for i, x in enumerate(self.list)if x == -1]
		self.holePos = self.holePos[0]
		try:
			top = [i for i, x in enumerate(self.list)if x == self.list[self.holePos-self.size]]
			if -1 in self.list[:self.size]:
				pass
			else:
				legal.append(top[0])
		except:pass
		try:
			bottom = [i for i, x in enumerate(self.list)if x == self.list[self.holePos+self.size]]
			legal.append(bottom[0])
		except:pass
		try:
			left = [i for i, x in enumerate(self.list)if x ==self.list[self.holePos-1]]
			if self.holePos % self.size == 0:
				pass
			else:
				legal.append(left[0])
		except:pass
		try:
			right = [i for i, x in enumerate(self.list)if x ==self.list[self.holePos+1]]
			if self.holePos+1 % self.size == 0:
				pass
			else:
				legal.append(right[0])
		except:pass
		return legal

	def shuffle(self, count):
		for i in range(count):
			choice = random.choice(self.legalNeighbors())
			self.list[self.holePos], self.list[choice] = self.list[choice], self.list[self.holePos]
		self.solver.reset()

	def takeTurn(self, n):
		legal = self.legalNeighbors()
		if n in legal:
			self.swapCells(n)
		self.countMoves += 1
		self.solver.reset()

	def swapCells(self, n):
		self.list[self.holePos], self.list[n] = self.list[n], self.list[self.holePos]

	def getCell(self, n):
		return self.list[n]

	def getHole(self):
		return self.holePos

	def solveStep(self):
		temp = self.solver.solve(self.list, self.getHole())
		print temp
		if temp == None:
			print "solved"
		else:
			self.takeTurn(temp)

def main():
	sl = SliderLogic(4)

main()