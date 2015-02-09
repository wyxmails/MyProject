#use execfile( "someFile.py") under python interpreter

import apriori

dataSet = apriori.loadDataSet()
print "Show dataSet: "
print dataSet

C1 = apriori.createC1(dataSet)
print "\nShow C1: "
print C1

D = map(set, dataSet)
print "\nShow D: "
print D

L1,suppData0 = apriori.scanD(D,C1,0.5)
print "\nShow L1: "
print L1

L,suppData=apriori.apriori(dataSet)
print "\nShow L: "
print L

print "\nShow L[0]: "
print L[0]

print "\nShow L[1]: "
print L[1]

print "\nShow L[2]: "
print L[2]

print "\nShow L[3]: "
print L[3]

apriori.aprioriGen(L[0],2)

L,suppData=apriori.apriori(dataSet,minSupport=0.7)
print "\nShow L 0.7: "
print L

L,suppData=apriori.apriori(dataSet,minSupport=0.5)
rules=apriori.generateRules(L,suppData,minConf=0.7)
print "\nShow rules minConf=0.7: "
print rules

rules=apriori.generateRules(L,suppData,minConf=0.5)
print "\nShow rules minConf=0.5: " 
print rules

