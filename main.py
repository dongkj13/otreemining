from od2estminer import *

a = od2estminer('orderedhjj.txt',4)
a.mine()

out = open('orderedhjj_out.txt','w')
for v in a.freqSubTrees:
	str1 = v['ptree'] + ' : ' + str(v['plist'])[1:-1] + '\n'
	out.write(str1)
out.close()
