# Локальный Kubernetes-кластер

## Используемый стек
- Minikube
- Docker driver
- Cilium CNI

## Команда запуска

```bash
minikube start --driver=docker --cni=cilium --cpus=4 --memory=6144

## Проверка состояния
minikube status
kubectl get nodes
kubectl get pods -A