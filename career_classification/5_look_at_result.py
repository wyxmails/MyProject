import pandas as pd
import os
import fnmatch


###split predicted result into two files: predict.cardiology, predict.other
def merge_result_feature():
    doctors = {}
    fname = ""
    for file in os.listdir('./predict_result.data'):
        if fnmatch.fnmatch(file,'*.csv'):
            fname = file
    print("fname=%s\n"%fname)
    f = open('predict_result.data/'+fname,'r')
    for line in f:
        line.strip('\n')
        arr = line.split(',')
        doctors[float(arr[0])] = float(arr[1])
    f.close()
    colnames = ['id', 'pcode']
    predict_data = pd.read_csv('./predict_merge.data',names=colnames,header=None)
    fwp = open('predict.cardiology','w')
    fwn = open('predict.other','w')
    for index,row in predict_data.iterrows():
        if doctors[row['id']]==1.0:
            fwp.write("%s,%s\n"%(row['id'],row['pcode']))
        else:
            fwn.write("%s,%s\n"%(row['id'],row['pcode']))
    fwp.close()
    fwn.close()
    print(predict_data.dtypes)


merge_result_feature()