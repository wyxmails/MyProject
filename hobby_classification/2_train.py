from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec
from pyspark.sql.functions import col, split

###word2vec.....
###read data from 'cat_dog.csv', and transform comments to vectors
sc = SparkContext('local')
spark = SparkSession(sc)
df = spark.read.csv('file:///Users/wyx/pyspark/cat_dog.csv')
df = df.withColumn("_c3",split(col("_c3")," "))
df = df.na.drop()
word2Vec = Word2Vec(vectorSize=60, seed=42, inputCol="_c3",outputCol="features")
word2Vec.setMinCount(5)
model = word2Vec.fit(df)
dfW2V = model.transform(df)

###train test spliting...
###split data to train:test=7:3
from pyspark.sql.window import Window
from pyspark.sql import functions as func
window = Window.orderBy(func.col('_c2'))
dfW2V = dfW2V.select('*', func.rank().over(window).alias('rank'))
num=dfW2V.count()*0.3
dfTrain = dfW2V.filter("rank>%d"%num)
dfTest = dfW2V.filter("rank<=%d"%num)
print("Train case num===%d, Test case num===%d\n"%(dfTrain.count(),dfTest.count()))

###training.....
###use Decision Tree to train a classifier
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer
stringIndexer = StringIndexer(inputCol="_c0",outputCol="indexed")
si_model = stringIndexer.fit(dfTrain)
td = si_model.transform(dfTrain)
dt = DecisionTreeClassifier(maxDepth=2,labelCol="indexed")
trainmodel = dt.fit(td)
#trainmodel.numNodes
#trainmodel.numClasses
#print(trainmodel.toDebugString)

###predicting......
#test0 = spark.read.csv('file:///Users/wyx/pyspark/cat_dog.csv')
testResult = trainmodel.transform(dfTest)
testResult.select('prediction','_c0').write.csv("./cat_dog.predict")


###evaluating.....
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql import DataFrame
dfEval = testResult.select('prediction',testResult._c0.cast('float').alias('label'))
evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
pr=evaluator.evaluate(dfEval,{evaluator.metricName: "areaUnderPR"})
roc=evaluator.evaluate(dfEval,{evaluator.metricName: "areaUnderROC"})
print("pr===%f roc===%f\n"%(pr,roc))

###save model.....
dtModelPath="./dtModelPath"
trainmodel.save(dtModelPath)
