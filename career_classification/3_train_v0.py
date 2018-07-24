from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import CountVectorizer
from pyspark.sql.functions import col, split
from pyspark.sql.window import Window
from pyspark.sql import functions as func
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql import DataFrame

###reading......
def read_file():
    sc = SparkContext('local')
    spark = SparkSession(sc)
    df = spark.read.csv('train.data')
    df = df.selectExpr('_c0 as id','_c1 as pcode','_c4 as label')
    df = df.select('id','pcode',df.label.cast('float').alias('label'))
    df = df.withColumn("pcode",split(col("pcode")," "))
    cv = CountVectorizer(inputCol="pcode", outputCol="features")
    model = cv.fit(df)
    df = model.transform(df)
    print("=====dfcv.dtypes")
    print(df.dtypes)
    bdf = df.select('id','features', 'label')
    print("=====bdf.dtypes")
    print(bdf.dtypes)
    return bdf

###train test spliting...
###split data to train:test=8:2
def split_data(df):
    window = Window.orderBy(func.col('id'))
    df = df.select('*', func.rank().over(window).alias('rank'))
    num=df.count()*0.2
    dftrain = df.filter("rank>%d"%num)
    dftest = df.filter("rank<=%d"%num)
    print("Train case num===%d, Test case num===%d\n"%(dftrain.count(),dftest.count()))
    # print(dftest.collect())
    return dftrain,dftest


###training.....
def lr_train(dftrain):
    blor = LogisticRegression(regParam=0.01)
    blorModel = blor.fit(dftrain)
    print("=====coefficients")
    print(blorModel.coefficients)
    lr_path = "./lr"
    blorModel.write().overwrite().save(lr_path)
    print("=====lr model saved")
    return blorModel


###predicting......
def lr_test(dftest, blorModel):
    result = blorModel.transform(dftest)
    print("=====result")
    print(result.dtypes)
    return result

###evaluating.....
def bi_eval(result):
    dfEval = result.select('prediction','label')
    evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
    pr=evaluator.evaluate(dfEval,{evaluator.metricName: "areaUnderPR"})
    roc=evaluator.evaluate(dfEval,{evaluator.metricName: "areaUnderROC"})
    print("pr===%f roc===%f\n"%(pr,roc))

if __name__=="__main__":
    print("===main...")
    df = read_file()
    dftrain,dftest = split_data(df)
    blorModel = lr_train(dftrain)
    result = lr_test(dftest, blorModel)
    bi_eval(result)