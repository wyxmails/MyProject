from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizerModel
from pyspark.sql.functions import col, split, concat_ws
from pyspark.ml.classification import LogisticRegressionModel
import os

predict_input='./predict_merge.data'
predict_output='./predict_result.data'

###reading......
def read_file():
    sc = SparkContext('local')
    spark = SparkSession(sc)
    df = spark.read.csv(predict_input)
    df = df.selectExpr('_c0 as id','_c1 as pcode')
    df = df.withColumn("pcode",split(col("pcode"),'|'))
    modelp = CountVectorizerModel.load('count_vectorizer')
    df = modelp.transform(df)
    bdf = df.select('id','features')
    print("===read_file() finished")
    return bdf

def lr_predict(df):
    blorModel = LogisticRegressionModel.load("lr")
    result = blorModel.transform(df)
    print("===lr_predict() finished")
    return result


###write down result to direction predict_result.data
def write_down(result):
    # result.select('id','prediction').write.csv("file:///Users/wyx/doximity_interview/predict_result.data",mode='overwrite')
    result.select('id', 'prediction').write.csv(predict_output,mode='overwrite')
    # print(result.collect())
    print("===write_down finished")

if __name__=="__main__":
    print("===main...")
    df = read_file()
    result = lr_predict(df)
    write_down(result)
