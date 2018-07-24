from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import CountVectorizer
from pyspark.sql.functions import col, split, concat_ws
from pyspark.sql.window import Window
from pyspark.sql import functions as func
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql import DataFrame
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.ml.feature import OneHotEncoder

train_input = 'train_merge.data'
train_result = 'train.result'
fw = open(train_result,'w')

###reading......
def read_file():
    sc = SparkContext('local')
    spark = SparkSession(sc)
    df = spark.read.csv(train_input)
    df = df.selectExpr('_c0 as id','_c1 as pcode','_c2 as label')
    df = df.select('id', 'pcode', df.label.cast('float').alias('label'))
    fw.write("df.dtypes=%s\n"%df.dtypes)
    df = df.withColumn("pcode",split(col("pcode"),'|'))
    fw.write("df.dtypes=%s\n" % df.dtypes)
    fw.write("df.count()=%d\n"%df.count())
    cvp = CountVectorizer(inputCol="pcode", outputCol="features")
    modelp = cvp.fit(df)
    modelp.write().overwrite().save('count_vectorizer')
    df = modelp.transform(df)
    fw.write("df.dtypes=%s\n"%df.dtypes)
    bdf = df.select('id','features', 'label')
    fw.write("bdf.dtypes=%s\n"%bdf.dtypes)
    # print(bdf.collect())
    return bdf

###train test spliting...
###split data by samplBy
def split_data(df):
    dftrain = df.sampleBy('label',fractions={0.0:0.8,1.0:0.8},seed=0)
    dftest = df.sampleBy('label',fractions={0.0:0.2,1.0:0.2},seed=1)
    fw.write("train case num=%d, test case num=%d\n"%(dftrain.count(),dftest.count()))
    return dftrain,dftest

###train test spliting...
###split data randomSplit
def split_data1(df):
    splits = df.randomSplit([4.0,1.0],17)
    dftrain = splits[0]
    dftest = splits[1]
    fw.write("train case num=%d, test case num=%d\n"%(dftrain.count(),dftest.count()))
    return dftrain,dftest

###training.....
def lr_train(dftrain):
    blor = LogisticRegression(regParam=0.005, elasticNetParam=0.005,threshold=0.4)
    blorModel = blor.fit(dftrain)
    print("=====coefficients = %s\n"%blorModel.coefficients)
    lr_path = "./lr"
    blorModel.write().overwrite().save(lr_path)
    fw.write("lr model saved\n")
    return blorModel


###predicting......
def lr_test(dftest, blorModel):
    result = blorModel.transform(dftest)
    fw.write("result.dtypes=%s\n"%result.dtypes)
    return result

###evaluating.....
def bi_eval(result):
    dfEval = result.select('prediction','label')
    evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
    pr=evaluator.evaluate(dfEval,{evaluator.metricName: "areaUnderPR"})
    roc=evaluator.evaluate(dfEval,{evaluator.metricName: "areaUnderROC"})
    fw.write("pr===%f roc===%f\n"%(pr,roc))

def pr_eval(result):
    dfEval = result.select('prediction','label')
    rows = dfEval.collect()
    true_p = 0
    false_p = 0
    true_n = 0
    false_n = 0
    for row in rows:
        if row.prediction==1.0 and row.label==1.0:
            true_p += 1
        elif row.prediction==1.0 and row.label==0.0:
            false_p += 1
        elif row.prediction==0.0 and row.label==0.0:
            true_n += 1
        else:
            false_n += 1
    fw.write("precision=true_p/(true_p+false_p)=%d/(%d+%d)=%f\n" % (true_p, true_p, false_p,(true_p * 1.0) / (true_p + false_p)))
    fw.write("recall=true_p/(true_p+false_n)=%d/(%d+%d)=%f\n" % (true_p, true_p, false_n, (true_p * 1.0) / (true_p + false_n)))


if __name__=="__main__":
    fw.write("main...\n")
    df = read_file()
    dftrain, dftest = split_data1(df)
    blorModel = lr_train(dftrain)
    result = lr_test(dftrain, blorModel)
    fw.write("result for train\n")
    bi_eval(result)
    pr_eval(result)
    result = lr_test(dftest, blorModel)
    fw.write("result for test\n")
    bi_eval(result)
    pr_eval(result)
    fw.close()