from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SparkAggregation")
    .config("spark.hadoop.fs.s3a.endpoint", "http://host.docker.internal:9000")
    .config("spark.hadoop.fs.s3a.access.key", "admin")
    .config("spark.hadoop.fs.s3a.secret.key", "admin123")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
    .getOrCreate()
)

print("Lendo dados do curated...")

df = spark.read.parquet("s3a://datalake/curated")

print("Linhas lidas:", df.count())

df_grouped = df.groupBy("category").avg("price")

print("Gravando resultado...")

df_grouped.write.mode("overwrite").parquet("s3a://datalake/spark_curated")

print("Spark finalizado com sucesso")

spark.stop()
