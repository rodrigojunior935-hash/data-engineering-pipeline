import subprocess

def run_spark_job():

    command = [
        "docker",
        "exec",
        "spark",
        "/opt/spark/bin/spark-submit",
        "--packages",
        "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.367",
        "/opt/spark/work-dir/spark_job.py"
    ]

    subprocess.run(command, check=True)

    print("Spark job executado")

