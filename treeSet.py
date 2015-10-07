from tree import *

class treeSet(object):
	def __init__(self):
		self.trees = []
		self.ptrees = []

	def readtrees(self, filename):
		for lines in open(filename):
			if lines != '':
				self.trees.append(lines)
				t = tree()
				t.settree(lines)
				self.ptrees.append(t)
