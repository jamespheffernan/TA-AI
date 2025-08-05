"""
Create Application Insights for monitoring
"""
resource "azurerm_application_insights" "monitoring" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
  retention_in_days   = var.retention_in_days
}
resource "azurerm_monitor_diagnostic_setting" "functions" {
  name               = "${var.name}-functions-diag"
  target_resource_id = var.functions_app_id

  application_insights {
    connection_string = azurerm_application_insights.monitoring.connection_string
  }
  logs {
    category = "FunctionAppLogs"
    enabled  = true

    retention_policy {
      enabled = false
    }
  }
  metrics {
    category = "AllMetrics"
    enabled  = true

    retention_policy {
      enabled = false
    }
  }
}