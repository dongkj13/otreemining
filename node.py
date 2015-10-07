class node(object):
	# node: parent------The parent node  
	# List: child-------The child nodes
	# String: label-----The generalized list form of the tree

	def __init__(self, plabel = ''):
		self.parent = None
		self.child = []
		self.label = plabel

