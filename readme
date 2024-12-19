#Build a docker image
docker build -t my-spark-hive-iceberg-image .

#Check the image with a trial run 
docker run -e AWS_ACCESS_KEY_ID='xx' -e AWS_SECRET_ACCESS_KEY='xxx' -e AWS_REGION='ap-south-1' -it my-spark-hive-iceberg-image /opt/spark/bin/spark-submit /opt/spark/work-dir/spark-iceberg-ingest-transformer/src/app.py

#go to terraform dir
cd terraform-eks
terraform init
terraform plan -out tfout
terraform apply

#deploy spark app on 
aws eks update-kubeconfig --name granica-cluster --region ap-south-1 
helm repo add bitnami https://charts.bitnami.com/bitnami 
helm repo update
kubectl create namespace spark-operator
helm install spark-operator bitnami/spark --namespace spark-operator
kubectl get pods
kubectl create secret generic aws-credentials \
  --from-literal=AWS_ACCESS_KEY_ID=your-access-key-id \
  --from-literal=AWS_SECRET_ACCESS_KEY=your-secret-access-key
kubectl apply -f spark-iceberg-deployment/spark-app.yaml
kubectl get scheduledsparkapplications
kubectl describe scheduledsparkapplication log-ingest-job-scheduler
kubectl logs <driver-pod-name>
kubectl logs <executor-pod-name>

#deploy pyspark-jupyter notebook for query
kubectl apply -f jupyter.yaml
POD_NAME=$(kubectl get pods --selector=app=jupyter -o jsonpath='{.items[0].metadata.name}')
kubectl logs $POD_NAME
kubectl port-forward service/jupyter 8888:80

#acess jupyter using 
http://127.0.0.1:8888/?token=YOUR_TOKEN

#deploy sparkhistoryserver to capture events
kubectl apply -f spark-history-pvc.yaml
kubectl apply -f history_server.yaml
kubectl apply -f spark-history-service.yaml

#dbt thrift integration
dbt run -m spark_demo_test

#destory resource
terraform destory
