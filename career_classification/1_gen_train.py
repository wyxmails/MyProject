#coding:utf-8
import pandas as pd
from pandas import Series

raw_input1='input_files/physicians.csv'
raw_input2='input_files/procedures.csv'
train_input='train_merge.data'
predict_input='predict_merge.data'
gen_result='gen.result'
fwr = open(gen_result,'w')

def read_write():
	doctors = {}
	predict_doctors = set()
	f = open(raw_input1,'r')
	pos = 0
	neg = 0
	pre = 0
	for line in f:
		line = line.strip('\n')
		arr = line.split(',')
		if arr[1]=='Cardiology':
			doctors[arr[0]] = 1
			pos += 1
		elif arr[1]=='Unknown':
			predict_doctors.add(arr[0])
			pre += 1
		else:
			doctors[arr[0]] = 0
			neg += 1
	fwr.write("positive doctors:%d, negative doctors:%d, precit doctors:%d\n"%(pos,neg,pre))
	f.close()

	f = open(raw_input2,'r')
	fw = open('train.data','w')
	fpw = open('predict.data','w')
	pos = 0
	neg = 0
	pre = 0
	for line in f:
		line = line.strip('\n')
		arr = line.split(',')
		if arr[0] in doctors:
			if doctors[arr[0]]==1:
				pos += 1
			else:
				neg += 1
			fw.write("%s,%d\n"%(line, doctors[arr[0]]))
		elif arr[0] in predict_doctors:
			pre += 1
			fpw.write("%s\n"%line)
	fwr.write("positive cases:%d, negative cases:%d, predict cases:%d\n"%(pos,neg,pre))
	f.close()
	fw.close()
	fpw.close()
	fwr.write("read_write() done\n")

def f(x):
	return Series(dict(id=x['id'].mean(),pcode="{%s}" % '|'.join(x['pcode']),label=x['label'].mean()))
def merge_train():
	colnames = ['id', 'pcode', 'pname', 'times', 'label']
	df = pd.read_csv("train.data", names=colnames, header=None)
	df = df.groupby('id').apply(f)
	df.to_csv(train_input,index=False,header=False)
	fwr.write("merge_train() done\n")

def f1(x):
	return Series(dict(id=x['id'].mean(),pcode="{%s}" % '|'.join(x['pcode'])))
def merge_predict():
	colnames = ['id', 'pcode', 'pname', 'times']
	dfp = pd.read_csv("predict.data",names=colnames, header=None)
	dfp = dfp.groupby('id').apply(f1)
	dfp.to_csv(predict_input,index=False,header=False)
	fwr.write("merge_predict() done\n")

read_write()
merge_train()
merge_predict()
fwr.close()