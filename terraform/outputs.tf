output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "search_service_name" {
  value = azurerm_search_service.search.name
}

output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "openai_service_name" {
  value = azurerm_cognitive_account.openai.name
}
