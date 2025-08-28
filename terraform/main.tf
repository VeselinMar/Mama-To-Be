terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.41.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_service_plan" "asp" {
  name                = var.app_service_plan_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "F1"
}

resource "azurerm_linux_web_app" "awa" {
  name                = var.web_app_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_service_plan.asp.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      python_version = "3.12"
    }
    app_command_line = "gunicorn mama_to_be.wsgi --bind=0.0.0.0"

  }
  app_settings = {
    "DJANGO_SETTINGS_MODULE" = "mama_to_be.settings"
    "SECRET_KEY"             = var.django_secret_key
    "ALLOWED_HOSTS"          = var.allowed_hosts
  }
}

resource "azurerm_app_service_source_control" "sourcecontrol" {
  app_id                 = azurerm_linux_web_app.awa.id
  repo_url               = var.repo
  branch                 = var.branch
  use_manual_integration = false
}