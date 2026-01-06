# small program to test if Spark is working


from pyspark.sql import SparkSession

data = [1, 2, 3, 4, 5, 6]

spark = SparkSession.builder.getOrCreate()

rdd = spark.sparkContext.parallelize(data)
print(f"Product of {data} is {rdd.reduce(lambda a, b: a * b)}")
spark.stop()
