module "aks" {
  source = "git::https://github.com/Surendra-Puri/Terraform-Modules.git//AKS?ref=main"

  aks_name      = var.aks_name
  location  = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  vm_size   = var.vm_size
  node_count        = var.node_count
  os_disk_size = var.os_disk_size
}
