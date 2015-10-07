from node import *
from tree import *
from treeSet import *
import time
import numpy
import re

class od2estminer(object):
	# String: filename-------The input file name
	# Int: threshold---------The support frequency
	# treeSet: ats-----------The tree set of all the data trees
	# list: freqSubTrees-----The frequent Subtrees


	def __init__(self, filename, pthreshold):
		self.filename = filename
		self.threshold = pthreshold
		self.ats = treeSet()
		self.freqSubTrees = []	
		# {'number':
		#  'plist':   
		#  'ptree':   
		#  'lastLabel':  
		#  'prefix':  }

	def mine(self):
		startTime = time.time()
		self.ats.readtrees(self.filename)
		endTime = time.time()
		print 'Read Trees costs %f seconds' %(endTime - startTime)
		
		startTime = time.time()
		self.mineFreqLabels()
		endTime = time.time()
		print 'Mine 1 Frequent Trees costs %f seconds' %(endTime - startTime)
		
		if len(self.freqSubTrees) > 0:
			startTime = time.time()
			self.mineFreq2Trees()
			endTime = time.time()
			print 'Mine 2 Frequent Trees costs %f seconds' %(endTime - startTime)
			
			self.time_freqTest = numpy.zeros([20])
			self.time_join = numpy.zeros([20])
			self.time_attachleg = numpy.zeros([20])
			self.time_settree = numpy.zeros([20])
			self.time_mine = numpy.zeros([20])
			if self.freqSubTrees[-1]['number'] == 2:
				k = 3
				while self.freqSubTrees[-1]['number'] == k-1:
					startTime = time.time()
					self.mineFreqkTrees(k)
					endTime = time.time()
					print 'Mine %d Frequent Trees costs %f seconds' %(k, endTime - startTime)
					print '	Freqeuency Test costs %f seconds' %(self.time_freqTest[k])
					print '	Join costs %f seconds' %(self.time_join[k])
					print '	Attach leg costs %f seconds' %(self.time_attachleg[k])
					print '	Set trees costs %f seconds' %(self.time_settree[k])
					print '	Mine costs %f seconds' %(self.time_mine[k])
					k += 1
					#if k == 15:
						#break

	def mineFreqLabels(self):
		splitters = '[(,;)]'
		for atree in self.ats.trees:
			labels = re.split(splitters, atree)			
			labels = filter(lambda l: l != '', labels)		# filter ''
			labels = list(set(labels))			# remove the same label
			map(self.findALabel, labels, [self.ats.trees.index(atree)] * len(labels))
		self.freqSubTrees = filter(lambda f: len(f['plist']) >= self.threshold, self.freqSubTrees)


	def findALabel(self, label, treeid):
		labelList = map(lambda f : f['ptree'], self.freqSubTrees)
		if label not in labelList:
			self.freqSubTrees.append({'number': 1, 'ptree': label, 'plist': [treeid], 'lastLabel': label, 'prefix': ''})
		else:
			self.freqSubTrees[labelList.index(label)]['plist'].append(treeid)

	def mineFreq2Trees(self):
		for parent in filter(lambda f : f['number'] == 1, self.freqSubTrees):
			for child in filter(lambda f : f['number'] == 1, self.freqSubTrees):
				intersect = list(set(parent['plist']).intersection(set(child['plist'])))
				support = []
				for k in intersect:
					if self.ats.ptrees[k].pcpairdetection(parent['ptree'], child['ptree']):
						support.append(k)
				if len(support) >= self.threshold:
					pair = parent['ptree'] + '(' + child['ptree'] + ')'
					self.freqSubTrees.append({'number': 2, 'ptree': pair, 'plist': support, 'lastLabel': child['ptree'], 'prefix': parent['ptree']})

	def mineFreqkTrees(self, k):
		startTime = time.time()
		fk = filter(lambda f : f['number'] == k-1, self.freqSubTrees)
		print 'The number of %d trees: %d' %(k, len(fk))
		for thisTree in fk:
			for anotherTree in fk:
				if thisTree['prefix'] == anotherTree['prefix']:
					if self.isSameTopology(thisTree['lastLabel'], anotherTree['lastLabel'], thisTree['ptree'], anotherTree['ptree']):
						self.join(thisTree, anotherTree, k)
						self.attachleg(thisTree, anotherTree, k)
					else:
						if self.freqSubTrees.index(thisTree) > self.freqSubTrees.index(anotherTree):
							self.join(thisTree, anotherTree, k)
							
		endTime = time.time()
		self.time_mine[k] += endTime - startTime


	def isSameTopology(self, thisLastLabel, anotherLastLabel, thisTree, anotherTree):
		if thisTree.replace(thisLastLabel, anotherLastLabel) == anotherTree.replace(thisLastLabel, anotherLastLabel):
			return True
		else:
			return False

	def frequentTest(self, thisTree, anotherTree, expandedStr, lastLabel, kTree):
		startTime = time.time()
		candidate = tree()
		candidate.settree(expandedStr)
		endTime = time.time()
		self.time_settree[kTree] += endTime - startTime

		intersect = list(set(thisTree['plist']).intersection(set(anotherTree['plist'])))
		support = []
		startTime = time.time()
		for k in intersect:
			if candidate.isembedded(self.ats.ptrees[k].postTree):
				support.append(k)
		endTime = time.time()
		self.time_freqTest[kTree] += endTime - startTime
		
		if len(support) >= self.threshold:
			position = expandedStr.rfind(lastLabel)			
			if expandedStr[position-1] == ',':
				prefix = expandedStr[:position-1] + expandedStr[position + len(lastLabel):]
			else:
				prefix = expandedStr[:position-1] + expandedStr[(position + len(lastLabel) + 1):]
			self.freqSubTrees.append({'number': kTree, 'ptree': expandedStr, 'plist': support, 'lastLabel': lastLabel, 'prefix': prefix})
		
		

	def attachleg(self, thisTree, anotherTree, kTree):
		startTime = time.time()
		oneleaftree = '(' + anotherTree['lastLabel'] + ')'
		position = thisTree['ptree'].rfind(thisTree['lastLabel']) + len(thisTree['lastLabel'])
		expandedStr = thisTree['ptree'][:position] + oneleaftree + thisTree['ptree'][position:]
		endTime = time.time()
		self.time_attachleg[kTree] += endTime - startTime
		self.frequentTest(thisTree, anotherTree, expandedStr, anotherTree['lastLabel'], kTree)
		

	def join(self, thisTree, anotherTree, kTree):
		startTime = time.time()
		lastLeafDepth = self.getLastLeafDepth(thisTree['ptree'], thisTree['lastLabel'])
		anotherLastLeafDepth = self.getLastLeafDepth(anotherTree['ptree'], anotherTree['lastLabel'])
		if lastLeafDepth >= anotherLastLeafDepth:
			expandedStr = thisTree['ptree']
			lastLabel = anotherTree['lastLabel']
			tail = ',' + lastLabel
			position = thisTree['ptree'].rfind(thisTree['lastLabel']) + len(thisTree['lastLabel'])
			position += lastLeafDepth - anotherLastLeafDepth
		else:
			expandedStr = anotherTree['ptree']
			lastLabel = thisTree['lastLabel']
			tail = ',' + lastLabel
			position = anotherTree['ptree'].rfind(anotherTree['lastLabel']) + len(anotherTree['lastLabel'])
			position += anotherLastLeafDepth - lastLeafDepth
		expandedStr = expandedStr[:position] + tail +expandedStr[position:]
		endTime = time.time()
		self.time_join[kTree] += endTime - startTime
		self.frequentTest(thisTree, anotherTree, expandedStr, lastLabel, kTree)
		

	def getLastLeafDepth(self, treeStr, lastLabel):
		# count ')' after the last label + 1
		return len(treeStr) - treeStr.rfind(lastLabel) - len(lastLabel) + 1
