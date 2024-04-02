This project is an NFT-integrated website where users can participate in collaboratively revealing a hidden image, one "pixel" at a time.

### What it Does

This is a full-stack application with a Django backend and a JavaScript frontend. Users can purchase individual "pixels" of a larger image. As "pixels" are bought, they are revealed to all users, slowly uncovering the complete image.

The web server does not store any non-recoverable state. NFT purchases are recorded on the smart contract and images are suggested to persist on IPFS.

**Technologies Used**

* Backend: Django
* Frontend: JavaScript
* Containerization: Docker
* Orchestration: Kubernetes
* Smart Contract: Solidity
* Dockerized Development
This project utilizes Docker for a development environment. Refer to the official Docker documentation for installation instructions: https://docs.docker.com/get-docker/

### Getting Started

1. Clone this repository.
2. Build the Docker images using provided Dockerfile.
3. Kubernetes Deployment (This application is designed for deployment on a Kubernetes cluster)

*Do you have a Kubernetes cluster set up?*

If not, you'll need to set up a Kubernetes cluster before proceeding.  There are many options available, including cloud-managed services and self-hosted solutions.

1. Google Kubernetes Engine (GKE): https://cloud.google.com/kubernetes-engine
2. Amazon Elastic Kubernetes Service (EKS): https://aws.amazon.com/eks/
3. Azure Kubernetes Service (AKS): https://azure.microsoft.com/en-us/products/kubernetes-service
4. Minikube (single-node local cluster): https://minikube.sigs.k8s.io/docs/start/
   
*Once you have a Kubernetes cluster:*

The application deployment utilizes Kubernetes manifests (YAML files). Refer to the Kubernetes documentation for details on using manifests: https://www.mirantis.com/blog/introduction-to-yaml-creating-a-kubernetes-deployment

### Deploying the Solidity Smart Contract
The Solidity smart contract manages the pixel ownership and purchase logic. You'll need a blockchain node to deploy and interact with the contract. Here are some resources to get you started:

* Solidity: https://docs.soliditylang.org/
* Ethereum Smart Contract Deployment: There are multiple tools and services for deploying smart contracts. Here's a general guide: https://medium.com/coinmonks/creating-and-deploying-a-smart-contract-on-a-blockchain-c97e9edcc065
* Blockchain Nodes: Consider using a testnet (e.g., Rinkeby for Ethereum) for initial development and testing before deploying to a mainnet.

This README provides a starting point for running the application in a Dockerized and Kubernetes-integrated environment.  The specific steps for building Docker images and deploying the application with Kubernetes will vary depending on your chosen setup.
