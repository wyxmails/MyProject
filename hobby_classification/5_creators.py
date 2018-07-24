#coding:utf-8
###collect the distinct owners for each creator
distinct = {}
f = open('./animals_comments.csv','r')
for line in open('./sample.csv'):
	line = f.readline()
	arr = line.split(',')
	word = arr[0]+"-"+arr[1]
	if word not in distinct:
		distinct[word] = 1
	else:
		distinct[word] += 1

###get the creator with most owners
creators = {}
for word in distinct:
	c = word.split('-')[0]
	if c not in creators:
		creators[c] = 1
	else:
		creators[c] += 1

creator = sorted(creators.items(),key=lambda kv:(-kv[1],kv[0]))[:1]
print("creator has the most owners is %s"%creator[0][0])

import math
###highest statistically significant percentages
###the file here is the predict output of 3_classify.py
data = {}
f = open('./animals.classify/part-00000-a4ca92ad-3dca-4f81-8e58-97e1921e3593-c000.csv','r')
for line in open('./animals.classify/part-00000-a4ca92ad-3dca-4f81-8e58-97e1921e3593-c000.csv'):
	line = f.readline()
	arr = line.split(',')
	word = arr[0]+"-"+arr[1]+"-"+arr[2]
	if word not in data:
		data[word] = 1
	else:
		data[word] += 1
creators = {}
dogs = {}
cats = {}
for word in data:
	c = word.split('-')[0]
	a = word.split('-')[2]
	if c not in creators:
		creators[c] = 1
		if float(a)=='0.0':
			dogs[c] = 1
		else:
			cats[c] = 1
	else:
		creators[c] += 1
		if float(a)==0.0:
			if c not in dogs:
				dogs[c] = 1
			else:
				dogs[c] += 1
		else:
			if c not in cats:
				cats[c] = 1
			else:
				cats[c] += 1
sorted_dogs = {}
sorted_cats = {}
for c in creators:
	sorted_dogs[c] = 0.0
	sorted_cats[c] = 0.0
	if c in dogs:
		sorted_dogs[c] = math.log(dogs[c],2)*dogs[c]/creators[c]
	if c in cats:
		sorted_cats[c] = math.log(cats[c],2)*cats[c]/creators[c]

dog = sorted(sorted_dogs.items(),key=lambda kv:(-kv[1],kv[0]))[:1]
cat = sorted(sorted_cats.items(),key=lambda kv:(-kv[1],kv[0]))[:1]
print("creator highest dog percentage is %s \ncreator highest cat percentage is %s \n"%(dog[0][0],cat[0][0]))
