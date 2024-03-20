if [ $# -lt 1 ]; then
  echo "Error: Please provide the version number as an argument. Example: ./refresh.sh 0.0.1"
  exit 1
fi

kubectl delete deployment pickpix-app
docker build --tag pickpix-app:$1 . --no-cache
docker tag pickpix-app:$1 localhost:5000/pickpix-app:latest
docker push localhost:5000/pickpix-app:latest
kubectl replace -f pickpix-app-deployment.yaml --force
