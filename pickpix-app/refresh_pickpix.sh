docker build --tag pickpix-app:123 . --no-cache
docker save pickpix-app > pickpix-app_image.tar
microk8s ctr image import pickpix-app_image.tar
microk8s.kubectl replace -f pickpix-app-deployment.yaml --force
