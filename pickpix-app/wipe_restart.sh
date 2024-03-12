docker rm -f registry
docker rmi -f $(docker images --filter=reference="*pickpix-app*" -q)
