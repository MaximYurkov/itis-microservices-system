output "app_namespace" {
  value = kubernetes_namespace.app.metadata[0].name
}

output "infra_namespace" {
  value = kubernetes_namespace.infra.metadata[0].name
}

output "service_accounts" {
  value = [
    kubernetes_service_account.task_service.metadata[0].name,
    kubernetes_service_account.agent_service.metadata[0].name,
    kubernetes_service_account.notification_service.metadata[0].name
  ]
}