from od2estminer import *
import time

a = od2estminer('orderedhjj.txt', 3)
start = time.time()
a.mine()


out = open('orderedhjj_out.txt','w')
for v in a.freqSubTrees:
	str1 = v['ptree'] + ' : ' + str(v['plist'])[1:-1] + '\n'
	out.write(str1)
	
print 'total frequent subtree: %d' %(len(a.freqSubTrees))
out.close()

print 'total time: %f ' %(time.time() - start)
