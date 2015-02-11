import fp_create
import fp_growth

rootNode = fp_create.treeNode('pyramid',9,None)
rootNode.children['eye'] = fp_create.treeNode('eye',13,None)
rootNode.disp()

rootNode.children['phoenix']=fp_create.treeNode('phoenix',3,None)
rootNode.disp()

simpDat = fp_create.loadSimpDat()
print "\nShow simpDat: "
print simpDat

initSet = fp_create.createInitSet(simpDat)
print "\nShow initSet: "
print initSet

myFPtree, myHeaderTab = fp_create.createTree(initSet,3)
print "myFptree disp: " 
myFPtree.disp()

print '\n\nFP growth start.....\n'

pre = fp_growth.findPrefixPath('x',myHeaderTab['x'][1])
print pre
pre = fp_growth.findPrefixPath('z',myHeaderTab['z'][1])
print pre
pre = fp_growth.findPrefixPath('r',myHeaderTab['r'][1])
print pre

freqItems = []
con = fp_growth.mineTree(myFPtree, myHeaderTab, 3, set([]), freqItems)
print 'freqItems: '
print freqItems
