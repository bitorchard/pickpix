kubectl delete deployment pickpix-app
docker build --tag pickpix-app:$1 . --no-cache
docker tag pickpix-app:$1 localhost:5000/pickpix-app:latest
docker push localhost:5000/pickpix-app:latest
#yq '.spec.template.spec.containers[0].image = "pickpix-app:$1"' -i pickpix-app-deployment.yaml
kubectl replace -f pickpix-app-deployment.yaml --force
