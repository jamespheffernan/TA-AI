terraform {
  required_version = ">= 1.4.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80.0"
    }
  }
}

provider "azurerm" {
  features {}
}

module "resource_group" {
  source = "../../modules/resource_group"
  name   = "taai-dev-rg"
  location = "uksouth"
}

module "vnet" {
  source = "../../modules/vnet"
  name   = "taai-dev-vnet"
  location = module.resource_group.location
  resource_group_name = module.resource_group.name
}

module "postgres" {
  source = "../../modules/postgres"
  name   = "taai-dev-pg"
  location = module.resource_group.location
  resource_group_name = module.resource_group.name
  vnet_subnet_id = module.vnet.postgres_subnet_id
}

module "openai" {
  source = "../../modules/openai"
  name   = "taai-dev-openai"
  location = module.resource_group.location
  resource_group_name = module.resource_group.name
  vnet_subnet_id = module.vnet.openai_subnet_id
}

module "storage" {
  source = "../../modules/storage"
  name   = "taai-devstorage"
  location = module.resource_group.location
  resource_group_name = module.resource_group.name
}

module "staticwebapp" {
  source = "../../modules/staticwebapp"
  name   = "taai-dev-web"
  location = module.resource_group.location
  resource_group_name = module.resource_group.name
}

module "functions" {
  source              = "../../modules/functions"
  name                = "taai-dev-func"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  vnet_subnet_id      = module.vnet.functions_subnet_id
  storage_account_name= module.storage.name
  app_insights_instrumentation_key = module.monitoring.instrumentation_key
  app_insights_connection_string   = module.monitoring.connection_string
}
module "monitoring" {
  source              = "../../modules/monitoring"
  name                = "taai-dev-ai"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  retention_in_days   = 30
}