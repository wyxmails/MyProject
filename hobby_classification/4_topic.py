from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import Tokenizer
from pyspark.sql.functions import col, split

###tokenizer....
###transform comments to vectors
sc = SparkContext('local')
spark = SparkSession(sc)
df = spark.read.csv('file:///Users/wyx/pyspark/sample.csv')
df = df.na.drop()
tokenizer = Tokenizer(inputCol="_c2", outputCol="words")
dftoken = tokenizer.transform(df)
cv = CountVectorizer(inputCol="words",outputCol="features")
model = cv.fit(dftoken)
dfcv = model.transform(dftoken)

###get topic with LDA
from pyspark.ml.clustering import LDA
print("LDA processing...")
lda = LDA(k=10, seed=31, optimizer="em")
ldaModel = lda.fit(dfcv)
ldaModel.vocabSize()
ldaModel.describeTopics().show()
topicTerm = ldaModel.describeTopics().select('termIndices')

###translate the result to words
rows = topicTerm.collect()
cnt=0
for row in rows:
	cnt += 1
	print("topic %d"%cnt)
	for i in row.termIndices:
		print model.vocabulary[i],
	print
