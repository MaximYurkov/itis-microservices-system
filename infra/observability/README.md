# Observability

## Установленный стек
- Prometheus
- Grafana
- Alertmanager

## Установка

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

## Проверка

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

## Доступ к Grafana

```bash
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
```

Адрес:
http://localhost:3000

## Получение пароля Grafana

```bash
kubectl get secret monitoring-grafana -n monitoring -o jsonpath="{.data.admin-password}"
```

## Доступ к Prometheus

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9090:9090
```

Адрес:
http://localhost:9090

## Результат
Grafana открывается, Prometheus доступен, datasource Prometheus создан автоматически, стандартные Kubernetes dashboards доступны.