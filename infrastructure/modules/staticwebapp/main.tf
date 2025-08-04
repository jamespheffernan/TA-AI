variable "name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }

resource "azurerm_static_site" "this" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku_name            = "Free"
}

output "default_hostname" {
  value = azurerm_static_site.this.default_hostname
}