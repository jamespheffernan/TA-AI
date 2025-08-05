output "instrumentation_key" {
  description = "Instrumentation key for Application Insights"
  value       = azurerm_application_insights.monitoring.instrumentation_key
}
output "connection_string" {
  description = "Connection string for Application Insights"
  value       = azurerm_application_insights.monitoring.connection_string
}