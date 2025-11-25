kind create cluster

kubectl delete deployment --all
kubectl delete pods --all

docker build -t zeka-api:latest ./api
docker build -t zeka-proxy:latest ./nginx-proxy
docker build -t zeka-frontend:latest ./frontend

kind load docker-image zeka-api:latest
kind load docker-image zeka-frontend:latest
kind load docker-image zeka-proxy:latest

docker exec -it kind-control-plane crictl images | grep zeka

kubectl apply -f web.yaml

kubectl get pods -w

# Şu komutsuz çalışmıyor.
kubectl port-forward svc/proxy 30000:80

================================================================================

kubectl rollout restart deployment proxy
