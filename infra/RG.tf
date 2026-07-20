data "azurerm_resource_group" "rg" {
  name     = "rg-github-actions-lab"
  location = "data.azurerm_resource_group.rg.location"
  
}