# Strimzi / Kafka в Kubernetes

## Namespace
- kafka

## Установка Strimzi operator

kubectl create namespace kafka
kubectl create -f "https://strimzi.io/install/latest?namespace=kafka" -n kafka
kubectl get pods -n kafka -w

## Развёртывание Kafka

kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-single-node.yaml -n kafka
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
kubectl get pods -n kafka
kubectl get kafka -n kafka

## Проверка producer / consumer

Consumer:
kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:1.0.0-kafka-4.2.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning

Producer:
kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:1.0.0-kafka-4.2.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic