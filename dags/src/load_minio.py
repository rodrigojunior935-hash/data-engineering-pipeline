from minio import Minio
import os

def upload_to_minio():

    client = Minio(
        "host.docker.internal:9000",
        access_key="admin",
        secret_key="admin123",
        secure=False
    )

    bucket = "datalake"

    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

    base_path = "/opt/airflow/datalake"

    layers = ["raw", "trusted", "curated"]

    for layer in layers:
        layer_path = os.path.join(base_path, layer)

        if not os.path.exists(layer_path):
            print(f"Pasta não encontrada: {layer_path}")
            continue

        for root, dirs, files in os.walk(layer_path):
            for file in files:
                local_file = os.path.join(root, file)

                object_name = os.path.relpath(local_file, base_path)

                client.fput_object(
                    bucket,
                    object_name.replace("\\", "/"),
                    local_file
                )

                print(f"Upload concluído: {object_name}")

    print("Upload completo para MinIO")
