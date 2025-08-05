variable "name" {
  description = "Name of the Application Insights instance"
  type        = string
}

variable "location" {
  description = "Azure region for resources"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "retention_in_days" {
  description = "Data retention period in days"
  type        = number
  default     = 30
}
variable "functions_app_id" {
  description = "Resource ID of the Azure Function App to monitor"
  type        = string
}