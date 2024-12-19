# Build a Docker Image
```bash
docker build -t my-spark-hive-iceberg-image .
```

# Check the Image with a Trial Run
```bash
docker run -e AWS_ACCESS_KEY_ID='xx' \
           -e AWS_SECRET_ACCESS_KEY='xxx' \
           -e AWS_REGION='ap-south-1' \
           -it my-spark-hive-iceberg-image /opt/spark/bin/spark-submit /opt/spark/work-dir/spark-iceberg-ingest-transformer/src/app.py
```

# Go to Terraform Directory
```bash
cd terraform-eks
terraform init
terraform plan -out tfout
terraform apply
```

# Deploy Spark App on AWS EKS
1. Update kubeconfig:
   ```bash
   update-kubeconfig --name granica-cluster --region ap-south-1
   ```

2. Add and update the Helm repository:
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```

3. Create a namespace and install Spark Operator:
   ```bash
   kubectl create namespace spark-operator
   helm install spark-operator bitnami/spark --namespace spark-operator
   kubectl get pods
   ```

4. Create AWS credentials as a secret:
   ```bash
   kubectl create secret generic aws-credentials \
       --from-literal=AWS_ACCESS_KEY_ID=your-access-key-id \
       --from-literal=AWS_SECRET_ACCESS_KEY=your-secret-access-key
   ```

5. Deploy the Spark app:
   ```bash
   kubectl apply -f spark-iceberg-deployment/spark-app.yaml
   kubectl get scheduledsparkapplications
   kubectl describe scheduledsparkapplication log-ingest-job-scheduler
   kubectl logs
   ```

# Deploy PySpark Jupyter Notebook for Query
1. Apply the Jupyter deployment:
   ```bash
   kubectl apply -f jupyter.yaml
   ```

2. Get the pod name and logs:
   ```bash
   POD_NAME=$(kubectl get pods --selector=app=jupyter -o jsonpath='{.items[0].metadata.name}')
   kubectl logs $POD_NAME
   ```

3. Forward the port to access Jupyter:
   ```bash
   kubectl port-forward service/jupyter 8888:80
   ```

4. Access Jupyter using:
   ```
   http://127.0.0.1:8888/?token=YOUR_TOKEN
   ```

# Deploy Spark History Server to Capture Events
1. Apply the persistent volume claim:
   ```bash
   kubectl apply -f spark-history-pvc.yaml
   ```

2. Deploy the History Server:
   ```bash
   kubectl apply -f history_server.yaml
   kubectl apply -f spark-history-service.yaml
   ```

# DBT Thrift Integration
```bash
dbt run -m spark_demo_test
```

# Destroy Resources
```bash
terraform destroy
