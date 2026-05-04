terraform {
  required_version = ">= 1.5.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.32"
    }
  }
}

provider "kubernetes" {
  config_path = var.kubeconfig_path
}

resource "kubernetes_namespace" "app" {
  metadata {
    name = var.app_namespace
  }
}

resource "kubernetes_namespace" "infra" {
  metadata {
    name = var.infra_namespace
  }
}

resource "kubernetes_service_account" "task_service" {
  metadata {
    name      = "task-service-sa"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
}

resource "kubernetes_service_account" "agent_service" {
  metadata {
    name      = "agent-service-sa"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
}

resource "kubernetes_service_account" "notification_service" {
  metadata {
    name      = "notification-service-sa"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
}

resource "kubernetes_secret" "app_secrets" {
  metadata {
    name      = "app-secrets"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  type = "Opaque"

  data = {
    postgres_user     = var.postgres_user
    postgres_password = var.postgres_password
    mongo_url         = var.mongo_url
    redis_url         = var.redis_url
  }
}