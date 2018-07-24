#coding:utf-8
###extract data contains 'my dog' or 'my cat' from animals_comments.csv
###label data with 'my dog' as 0, label data with 'my cat' as 1
###insert label to the first column
###output to 'cat_dog.csv'
d='my dog'
c='my cat'
#f = open('head.csv','r')
#for line in open('head.csv'):
f = open('animals_comments.csv','r')
fw = open("cat_dog.csv","w")
for line in open('animals_comments.csv'):
	line = f.readline()
	if d in line.lower():
		print >> fw, "0,"+line,
	if c in line.lower():
		print >> fw, "1,"+line,
f.close()
fw.close()
