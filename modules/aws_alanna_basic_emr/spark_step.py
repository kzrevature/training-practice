# small program to test if Spark is working

from random import random

from pyspark.sql import SparkSession

data_len = 1000
data = [random() for _ in range(data_len)]

spark = SparkSession.builder.getOrCreate()
rdd = spark.sparkContext.parallelize(data)
print(f"Sum of {data_len} random numbers (using PySpark RDD):  {rdd.sum()}")
print(f"Sum of {data_len} random numbers (basic Python sum):   {rdd.sum()}")
spark.stop()
