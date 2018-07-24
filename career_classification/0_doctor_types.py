#coding:utf-8
import operator
###
###
###
doc_types = {}
f = open('input_files/physicians.csv','r')
for line in open('input_files/physicians.csv'):
	line = f.readline()
	line = line.strip('\n')
	arr = line.split(',')
	if arr[1] not in doc_types:
		doc_types[arr[1]] = 1
	else:
		doc_types[arr[1]] += 1
f.close()
doc_types =  sorted(doc_types.items(),key=operator.itemgetter(1))
for t in doc_types:
	print(t)
	#print("%s : %d"%(t,doc_types[t]))
