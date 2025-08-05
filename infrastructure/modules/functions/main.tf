variable "name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "vnet_subnet_id" { type = string }
variable "storage_account_name" { type = string }
variable "app_insights_instrumentation_key" {
  description = "Instrumentation key for Application Insights"
  type        = string
}

variable "app_insights_connection_string" {
  description = "Connection string for Application Insights"
  type        = string
}

resource "azurerm_service_plan" "this" {
  name                = "${var.name}-plan"
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "this" {
  name                       = var.name
  location                   = var.location
  resource_group_name        = var.resource_group_name
  service_plan_id            = azurerm_service_plan.this.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = "placeholder-access-key"
  virtual_network_subnet_id  = var.vnet_subnet_id
  https_only                 = true
  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY"               = var.app_insights_instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING"        = var.app_insights_connection_string
  }
  site_config {
    application_stack {
      python_version = "3.11"
    }
  }
}

output "default_hostname" {
  value = azurerm_linux_function_app.this.default_hostname
}