# Random resource names
resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "random_string" "search_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "random_string" "storage_suffix" {
  length  = 12
  special = false
  upper   = false
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = random_pet.rg_name.id
  location = var.resource_group_location
}

# Storage Account + Container for notes
resource "azurerm_storage_account" "storage" {
  name                     = "${var.storage_account_name}${random_string.storage_suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_blob_public_access = true

  tags = {
    environment = "clinical-rag"
  }
}

resource "azurerm_storage_container" "notes" {
  name                  = "notes"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

# Azure AI Search Service (Free tier for learning)
resource "azurerm_search_service" "search" {
  name                = "${var.search_service_name}-${random_string.search_suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "free"  # or "basic" for production
  replica_count       = 1
  partition_count     = 1

  tags = {
    environment = "clinical-rag"
  }
}

# Azure OpenAI Service
resource "azurerm_cognitive_account" "openai" {
  name                = "${var.openai_service_name}-${random_string.search_suffix.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "OpenAI"
  sku_name            = "S0"

  tags = {
    environment = "clinical-rag"
  }
}

# Output keys for your Python scripts
output "azure_keys" {
  value = {
    SEARCH_ENDPOINT    = azurerm_search_service.search.endpoint
    SEARCH_ADMIN_KEY   = azurerm_search_service.search.primary_key
    STORAGE_CONNECTION_STRING = azurerm_storage_account.storage.primary_connection_string
    AZURE_OPENAI_ENDPOINT = "https://${azurerm_cognitive_account.openai.endpoint}"
    AZURE_OPENAI_KEY    = azurerm_cognitive_account.openai.primary_access_key
  }
  sensitive = true
}

output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "notes_container_name" {
  value = azurerm_storage_container.notes.name
}
