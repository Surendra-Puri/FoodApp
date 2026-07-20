module "aks" {
  source = "git::https://github.com/Surendra-Puri/Terraform-Modules.git//AKS?ref=main"

  name      = "aks-lab"
  location  = data.azurerm_resource_group.rg.location
  parent_id = data.azurerm_resource_group.rg.id
  vm_size   = "Standard_B2s"
  node_count = 1
  os_disk_size_gb = 30
}