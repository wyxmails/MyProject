#coding=utf-8
import pandas as pd
import numpy as np
from pandas import Series,DataFrame

data_train = pd.read_csv('train.data')

print(data_train.info())

###distribution of times
print(data_train['times'].describe())
print(data_train[data_train['times']>10].count().id)
print(data_train[data_train['times']>50].count().id)
print(data_train[data_train['times']>100].count().id)
print(data_train[data_train['times']>150].count().id)
print(data_train[data_train['times']>200].count().id)
print(data_train[data_train['times']>250].count().id)
print(data_train[data_train['times']>500].count().id)
print(data_train[data_train['times']>1000].count().id)
print(data_train[data_train['times']>5000].count().id)


####distribution of pid occurance times
print(data_train['pid'].count())
gp = data_train.groupby('pid')
newdf=gp.size()
newdf=newdf.reset_index(name='times')
newdf.info()
print(newdf[newdf['times']>10000])
print(newdf[newdf['times']>0].count().pid)
print(newdf[newdf['times']>10].count().pid)
print(newdf[newdf['times']>50].count().pid)
print(newdf[newdf['times']>100].count().pid)
print(newdf[newdf['times']>500].count().pid)
print(newdf[newdf['times']>1000].count().pid)
print(newdf.count().pid)

import matplotlib.pyplot as plt

fig = plt.figure()
fig.set(alpha=0.5)

plt.subplot2grid((5,5),(0,0))
data_train.label.value_counts().plot(kind='bar')
plt.title(u'label dis')
plt.ylabel(u'cnt')

plt.subplot2grid((5,5),(0,2))
data_train.pid.value_counts().plot(kind='bar')
plt.title(u'pid dis')
plt.ylabel(u'cnt')
plt.xlabel(u'pid')

plt.subplot2grid((5,5),(0,4))
data_train.times.value_counts().plot(kind='bar')
plt.title(u'times')
plt.title(u'times dis')

plt.subplot2grid((5,5),(2,0),colspan=2)
data_train.times[data_train.label==0].plot(kind='kde')
data_train.times[data_train.label==1].plot(kind='kde')
plt.xlabel(u'times')
plt.ylabel(u'proportion')
plt.title(u'times-label dis')
plt.legend((u'label=0',u'label=1'),loc='best')

plt.subplot2grid((5,5),(2,3),colspan=2)
data_train[data_train['times']<=100].times[data_train.label==0].plot(kind='kde')
data_train[data_train['times']<=100].times[data_train.label==1].plot(kind='kde')
plt.xlabel(u'times')
plt.ylabel(u'proportion')
plt.title(u'times-label dis')
plt.legend((u'label=0',u'label=1'),loc='best')

plt.subplot2grid((5,5),(4,0))
data_train[data_train['pid']=='93306'].label.value_counts().plot(kind='bar')
plt.title(u'99306')
plt.ylabel(u'cnt')
plt.xlabel(u'label')
plt.subplot2grid((5,5),(4,1))
data_train[data_train['pid']=='99204'].label.value_counts().plot(kind='bar')
plt.title(u'99204')
plt.ylabel(u'cnt')
plt.xlabel(u'label')
plt.subplot2grid((5,5),(4,2))
data_train[data_train['pid']=='99213'].label.value_counts().plot(kind='bar')
plt.title(u'99213')
plt.ylabel(u'cnt')
plt.xlabel(u'label')
plt.subplot2grid((5,5),(4,3))
data_train[data_train['pid']=='99214'].label.value_counts().plot(kind='bar')
plt.title(u'99214')
plt.ylabel(u'cnt')
plt.xlabel(u'label')
plt.subplot2grid((5,5),(4,4))
data_train[data_train['pid']=='99232'].label.value_counts().plot(kind='bar')
plt.title(u'99232')
plt.ylabel(u'cnt')
plt.xlabel(u'label')

fig1 = plt.figure()
fig1.set(alpha=0.5)

data_train[data_train['label']==0].id.value_counts().plot(kind='kde')
data_train[data_train['label']==1].id.value_counts().plot(kind='kde')
plt.xlabel(u'id times')
plt.ylabel(u'proportion')
plt.title(u'id times dis')
plt.legend((u'label=0',u'label=1'),loc='best')