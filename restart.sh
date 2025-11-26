#!/bin/bash

echo "🧹 Eski imajlar , deployment ve podlar siliniyor..."

docker rmi -f kubernetes-api:latest
docker rmi -f kubernetes-proxy:latest
docker rmi -f kubernetes-frontend:latest
docker rmi -f kubernetes-db-service:latest

kubectl delete deployment --all --ignore-not-found
kubectl delete pods --all --ignore-not-found

echo "🐳 Docker imajları build ediliyor..."

docker build -t kubernetes-api:latest ./api
docker build -t kubernetes-proxy:latest ./nginx-proxy
docker build -t kubernetes-frontend:latest ./frontend
docker build -t kubernetes-db-service:latest ./db-service   # düzeltildi!


echo "📦 KIND içine image'lar yükleniyor..."

kind load docker-image kubernetes-api:latest
kind load docker-image kubernetes-frontend:latest
kind load docker-image kubernetes-proxy:latest
kind load docker-image kubernetes-db-service:latest


echo "📜 Kubernetes manifest apply ediliyor..."
kubectl apply -f web.yaml

echo "🎉 Deployment tamamlandı!"
sleep 3
kubectl port-forward svc/proxy 30000:80
echo "👉 Proxy NodePort: 30000 (http://localhost:30000)"
