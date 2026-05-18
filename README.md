# Kubernetes + Docker + EKS-CTL

This README provides end-to-end steps for installing **eksctl**,
**kubectl**, **Docker**, **Ingress-Nginx**, **MariaDB**, **ArgoCD**, and
creating necessary namespaces and database tables.

## Install eksctl

``` bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

## Create EKS Cluster

``` bash
eksctl create cluster --name google --region ap-northeast-1 --node-type t3.medium --nodes 2
```

## Install kubectl

``` bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

## Install Docker & Git

``` bash
yum install docker -y
systemctl start docker
yum install git -y
```

## Install Ingress-Nginx

``` bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
kubectl get ingress -n google
```

## Install MariaDB

``` bash
sudo yum update -y
sudo dnf install -y mariadb105
```

## MySQL Database Setup

``` sql
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
exit
```

## Install ArgoCD

``` bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc -n argocd
```

## Create Namespace

``` bash
kubectl create namespace google
```

## Retrieve ArgoCD Password

``` bash
kubectl -n argocd get secret argocd-initial-admin-secret   -o jsonpath="{.data.password}" | base64 -d
```

------------------------------------------------------------------------

# 📸 Architecture & Workflow Diagrams

### Cluster Architecture

``` bash
Need to change the detils 
```

![Cluster Architecture](https://i.ibb.co/6R7ZN38f/image.png)

### Workflow Diagram

![Workflow Diagram](https://i.ibb.co/t9WR8c8/drawing.png)
