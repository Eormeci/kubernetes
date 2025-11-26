kind create cluster

kubectl delete deployment --all
kubectl delete pods --all

docker build -t kubernetes-api:latest ./api
docker build -t kubernetes-proxy:latest ./nginx-proxy
docker build -t kubernetes-frontend:latest ./frontend
docker build -t kubernetes-db-service:latest ./db-service


kind load docker-image kubernetes-api:latest
kind load docker-image kubernetes-frontend:latest
kind load docker-image kubernetes-proxy:latest
kind load docker-image kubernetes-db-service:latest


kubectl apply -f web.yaml

kubectl get pods -w

# Şu komutsuz çalışmıyor.
kubectl port-forward svc/proxy 30000:80

================================================================================

kubectl rollout restart deployment proxy
