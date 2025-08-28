variable "location" {
  description = "Deployment location"
  type        = string
}

variable "resource_group_name" {
  description = "rg name"
  type        = string
}

variable "acr_name" {
  description = "acr name"
  type        = string
}

variable "app_service_plan_name" {
  description = "Service Plan name"
  type        = string
}

variable "server_name" {
  description = "DB server name"
  type        = string
}

variable "web_app_name" {
  description = "WebApp name"
  type        = string
}

variable "subscription_id" {
  description = "azure_subscription_id"
  type        = string
}


variable "django_secret_key" {
  description = "Django secret key"
  type        = string
}

variable "db_user" {
  description = "CosmosDB user"
  type        = string
}

variable "db_password" {
  description = "CosmosDB Password"
  type        = string
}

variable "db_name" {
  description = "CosmosDB Name"
  type        = string
}


variable "repo" {
  description = "Deployment repo"
  type        = string
}

variable "branch" {
  description = "Deployment branch"
  type        = string
}

variable "allowed_hosts" {
  description = "Allowed hosts"
  type        = string
}