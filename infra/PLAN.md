# План реализации блока 2 ПИ Инфра

## Цель

Во втором блоке требуется развернуть инфраструктурную платформу для уже существующего микросервисного приложения.  
В качестве базового приложения используется сервис асинхронной модерации пользовательских объявлений, разработанный в первом блоке.

## Что уже есть

В проекте уже реализованы:
- task-service
- agent-service
- notification-service
- Kafka
- PostgreSQL
- Redis
- MongoDB
- Nginx gateway
- Docker Compose для локального запуска

## Что нужно сделать во втором блоке

Нужно перенести проект на Kubernetes и дополнить его инфраструктурными инструментами:
- локальный Kubernetes-кластер
- GitOps
- IaC
- Kafka в Kubernetes
- service mesh
- ingress и rate limiting
- observability
- CI/CD
- нагрузочное тестирование

## Выбранный стек

Для реализации второго блока выбран следующий стек:

- Kubernetes: Minikube
- CNI: Cilium
- IaC: Terraform
- GitOps: ArgoCD
- Kafka в Kubernetes: Strimzi
- Конфигурация и автоматизация: Ansible
- Service Mesh: Istio
- Ingress: NGINX Ingress Controller
- Rate Limiting: через ingress / redis-backed подход
- Observability:
  - Prometheus
  - Grafana
  - Loki
  - Tempo
  - Alertmanager
- CI/CD: GitHub Actions Self-Hosted Runner
- Package manager для сервисов: Helm
- Нагрузочное тестирование: Locust

## Что делаем в упрощённом виде

Так как проект учебный и разворачивается локально, часть решений будет реализована в упрощённом формате:

- локальный кластер будет поднят на Minikube;
- упор делается на работоспособность и демонстрацию архитектурных подходов;
- high availability в полном production-виде не является основной целью;
- autoscaling нод в локальной среде рассматривается с учётом ограничений Minikube;
- observability будет собрана на одном выбранном стеке, без параллельного сравнения нескольких платформ в реальном развёртывании.

## Этапы реализации

1. Подготовить новую git-ветку под второй блок.
2. Поднять локальный Kubernetes-кластер.
3. Установить Cilium.
4. Подготовить Helm-чарты для трёх микросервисов.
5. Развернуть Kafka через Strimzi.
6. Развернуть ArgoCD и настроить GitOps.
7. Добавить Terraform для базовой инфраструктуры.
8. Добавить Ansible role для Kafka / Strimzi.
9. Развернуть Istio.
10. Настроить ingress и rate limiting.
11. Подключить observability стек.
12. Настроить self-hosted runner и CI/CD.
13. Подготовить Locust и провести тестирование.

## Минимальный результат

Минимально достаточным результатом считается:
- кластер Kubernetes поднят локально;
- приложение развёрнуто в Kubernetes;
- сервисы упакованы в Helm;
- Kafka работает в кластере;
- ArgoCD синхронизирует приложения из Git;
- есть базовая observability;
- есть нагрузочный тест;
- есть материалы для отчёта и защиты.