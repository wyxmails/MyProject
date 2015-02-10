import fp_growth

rootNode = fp_growth.treeNode('pyramid',9,None)
rootNode.children['eye'] = fp_growth.treeNode('eye',13,None)
rootNode.disp()

rootNode.children['phoenix']=fp_growth.treeNode('phoenix',3,None)
rootNode.disp()

simpDat = fp_growth.loadSimpDat()
print "\nShow simpDat: "
print simpDat

initSet = fp_growth.createInitSet(simpDat)
print "\nShow initSet: "
print initSet

#myFPtree, myHeaderTab = fp_growth.createTree(initSet,3)
#myFPtree.disp()
