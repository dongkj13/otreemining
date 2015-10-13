from node import *
import numpy

class tree(object):
	# node: root------------The root node of this tree
	# String: treestr-------The generalized list form of the tree
	# List: postTree--------The list of the postorder
	# Array: matrix---------The embedded information of two trees
	# Array: blopam

	def __init__(self):
		self.root = node()
		self.treestr = ''
		self.postTree = []

	def settree(self, t):
		self.treestr = t
		self.convert()
		self.postorder(self.root, self.postTree)

	def findLabel(self, treestr, i):
		tlabel = ''
		while (i < len(treestr) and treestr[i] !='(' and treestr[i] != ',' and treestr[i] != ')'):
			tlabel += treestr[i]
			i += 1
		newNode = node(tlabel)
		return newNode, i

	def convert(self):
		i = 0
		tlabel=''
		newNode, i = self.findLabel(self.treestr, i)
		self.root = newNode		
		labelList = []
		labelList.append(self.root)
		while (i < len(self.treestr) and self.treestr[i] != ';' ):
			tchar = self.treestr[i]
			i += 1
			if tchar == ')':
				labelList.pop()
			else:				
				if tchar == ',':
					labelList.pop()
				# both for tchar = ',' or '('
				newNode, i = self.findLabel(self.treestr, i)				
				preNode = labelList[-1]
				preNode.child.append(newNode)
				newNode.parent = preNode
				labelList.append(newNode)
			
	def postorder(self, n, postTree):
		for child in n.child:
			self.postorder(child,postTree)
		postTree.append(n)
		

	def isembedded(self, anotherPostTree):
		self.matrix = numpy.zeros([len(self.postTree), len(anotherPostTree)], int)
		for i in range(len(self.postTree)):
			for j in range(len(anotherPostTree)):
				if self.iscontain(i, j, anotherPostTree):
					self.matrix[i, j] = 1
				else:
					self.matrix[i, j] = 0;
				if (i == len(self.postTree) - 1) and (self.matrix[i, j] == 1):
					return True
		return False

	def iscontain(self, i, j, anotherPostTree):
		l1 = self.postTree[i].label
		l2 = anotherPostTree[j].label
		# neither two trees have children
		if not(self.postTree[i].child or anotherPostTree[j].child):
			return (l1 == l2)
		if not(anotherPostTree[j].child):
			return False
		if not(self.postTree[i].child):
			if (l1 == l2):
				return True
			else:
				for n in anotherPostTree[j].child:
					if self.matrix[i, anotherPostTree.index(n)] == 1:
						return True
				return False
		# both trees have children
		# case 1:parent match parent, children in children
		if l1 == l2:
			self.blopam = []
			for n1 in self.postTree[i].child:
				self.blopam.append([])
				for n2 in anotherPostTree[j].child:
					m = self.postTree.index(n1)
					n = anotherPostTree.index(n2)
					self.blopam[-1].append(self.matrix[m, n])
			return (self.blopa(0, 0))
		# case 2:parent match one of the child of the other tree
		else:
			for n in anotherPostTree[j].child:
				if self.matrix[i, anotherPostTree.index(n)] == 1:
					return True
			return False

	def blopa(self, row, col):
		if row < len(self.blopam):
			flag = False
			for j in range(col,len(self.blopam[0])):
				if self.blopam[row][j] == 1:
					flag = True
					break
			if not(flag):
				return False
			else:
				return self.blopa(row+1, j+1)
		else:
			return True



	def pcpairdetection(self, par, child):
		ischild = filter(lambda n: n.label == child, self.postTree)
		for eachchild in ischild:
			p = eachchild.parent
			while (p != None and p.label != par):
				p = p.parent
			if (p != None and p.label == par):
				return True
		return False

