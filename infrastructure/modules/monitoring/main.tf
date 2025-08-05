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