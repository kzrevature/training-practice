from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.getOrCreate()

# mutes extremely spammy MicroBatchExecutionContext logs
spark.sparkContext.setLogLevel("WARN")

lines = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "elysium-topic")
    .load()
)

decoded = lines.select(col("value").cast("string").alias("message"))

query = decoded.writeStream.format("console").start()
query.awaitTermination()
