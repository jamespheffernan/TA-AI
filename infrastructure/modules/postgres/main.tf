variable "name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "vnet_subnet_id" { type = string }

resource "azurerm_postgresql_flexible_server" "this" {
  name                   = var.name
  location               = var.location
  resource_group_name    = var.resource_group_name
  administrator_login    = "pgadmin"
  administrator_password = "P@ssword1234!"
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  version                = "15"
  delegated_subnet_id    = var.vnet_subnet_id
  zone                   = "1"
  high_availability      = "Disabled"
  public_network_access_enabled = true
}

resource "azurerm_postgresql_flexible_server_database" "db" {
  name      = "taai"
  server_id = azurerm_postgresql_flexible_server.this.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}

output "fqdn" {
  value = azurerm_postgresql_flexible_server.this.fqdn
}