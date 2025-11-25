docker build -t zeka-api:latest .
docker build -t zeka-proxy:latest .
docker build -t zeka-frontend:latest .

kind load docker-image zeka-api:latest
kind load docker-image zeka-frontend:latest
kind load docker-image zeka-proxy:latest

docker exec -it kind-control-plane crictl images | grep zeka

kubectl apply -f web.yaml

kubectl get pods -w
