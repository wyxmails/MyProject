#coding:utf-8
###calculate the metrics
f = open('./cat_dog.predict/part-00000-1c2f75d4-7255-476b-8a4b-00515ff2a845-c000.csv','r')
fw = open('./metrics.out','w')
tp=0
fp=0
tn=0
fn=0
total=0
for line in open('./cat_dog.predict/part-00000-1c2f75d4-7255-476b-8a4b-00515ff2a845-c000.csv'):
	total += 1
	line = f.readline()
	arr = line.split(',')
	if float(arr[0])==0.0 and int(arr[1])==0:
		tp += 1
	if float(arr[0])==0.0 and int(arr[1])==1:
		fp += 1
	if float(arr[0])==1.0 and int(arr[1])==1:
		tn += 1
	if float(arr[0])==1.0 and int(arr[1])==0:
		fn += 1
print ('%d %d %d %d %d'%(total,tp,fp,tn,fn))
print('tp/(tp+fp)=%f, tn/(tn+fn)=%f\n'%(1.0*tp/(tp+fp),1.0*tn/(tn+fn)))
f.close()
fw.close()

###estimate real cat/dog owners
f = open('./animals.classify/part-00000-a4ca92ad-3dca-4f81-8e58-97e1921e3593-c000.csv','r')
fw = open('./estimate.result','w')
dog=0
cat=0
total=0
for line in open('./animals.classify/part-00000-a4ca92ad-3dca-4f81-8e58-97e1921e3593-c000.csv'):
	total += 1
	line = f.readline()
	arr = line.split(',')
	if float(arr[2])==0.0:
		dog += 1
	if float(arr[2])==1.0:
		cat += 1
print('total=%d\npredict dog owner=%d,real dog owner=%d\npredict cat owner=%d,real cat owner=%d\n'%(total,dog,dog*tp/(tp+fp),cat,cat*tn/(tn+fn)))
