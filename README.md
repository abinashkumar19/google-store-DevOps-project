#!/bin/bash

# =========================================================================
# 🛠️ Installation and Configuration Script for EKS, Kubernetes, and ArgoCD
# =========================================================================

# --- 1. Kubernetes and EKS Prerequisites ---

echo "--- 1.1 Installing eksctl ---"
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | \
tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version

echo "--- 1.2 Installing kubectl ---"
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

# --- 2. System Tools Installation (Docker and Git) ---

echo "--- 2. Installing Docker and Git ---"
yum install docker -y
systemctl start docker 
yum install git -y

# --- 3. EKS Cluster Creation ---

echo "--- 3. Creating EKS Cluster named 'google' (This may take 15-20 minutes) ---"
eksctl create cluster --name google \
   --region ap-northeast-1 \
   --node-type c7i-flex.large \
   --nodes-min 2 \
   --nodes-max 2

# --- 4. Kubernetes Ingress Setup ---

echo "--- 4. Installing NGINX Ingress Controller ---"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

echo "--- 4.1 Verifying Ingress Deployment ---"
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
kubectl get ingress -n google

# --- 5. Database Setup (MariaDB) ---

echo "--- 5.1 Installing MariaDB 10.5 ---"
sudo yum update -y
sudo dnf install -y mariadb105

# Note: Running SQL non-interactively. Assumes MariaDB is running and accessible (e.g., as root).
echo "--- 5.2 Creating Database and Users Table in MariaDB ---"
mysql -e "
CREATE DATABASE IF NOT EXISTS cloud;
USE cloud;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"
# The 'exit' command is not needed when using 'mysql -e'

# --- 6. ArgoCD Installation and Configuration ---

echo "--- 6.1 Installing ArgoCD ---"
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "--- 6.2 Exposing ArgoCD Server via LoadBalancer ---"
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc -n argocd

echo "--- 6.3 Creating Custom Namespace 'google' ---"
kubectl create namespace google

echo "--- 6.4 Retrieving ArgoCD initial admin password ---"
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" |
base64 -d

echo ""
echo "--- Script Execution Complete! ---"
