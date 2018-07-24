from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec
from pyspark.sql.functions import col, split
from pyspark.ml.classification import DecisionTreeClassificationModel

###read data from animals_comments.csv 
###transform comments to vectors
sc = SparkContext('local')
spark = SparkSession(sc)
#dfp = spark.read.csv('file:///Users/wyx/pyspark/animals_comments.csv')
dfp = spark.read.csv('file:///Users/wyx/pyspark/sample.csv')
dfp = dfp.withColumn("_c2",split(col("_c2")," "))
dfp = dfp.na.drop()
word2Vec = Word2Vec(vectorSize=60, seed=42, inputCol="_c2",outputCol="features")
word2Vec.setMinCount(5)
model = word2Vec.fit(dfp)

dfW2V = model.transform(dfp)

###load model
###load model saved in 2_train.py
dtModelPath="./dtModelPath"
trainmodel = DecisionTreeClassificationModel.load(dtModelPath)
predictResult = trainmodel.transform(dfW2V)

###output predict result with columns: 
### (creator,userId,prediction(0:dog,1:cat))
predictResult.select('_c0','_c1','prediction').write.csv("./animals.classify")
print("===finished===")
