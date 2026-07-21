module "aks" {
  source = "git::https://github.com/Surendra-Puri/Terraform-Modules.git//AKS?ref=main"

  name      = "aks-lab"
  location  = data.azurerm_resource_group.rg.location
  parent_id = data.azurerm_resource_group.rg.id
  vm_size   = "Standard_B2s"
  count_of        = var.node_count
  os_disk_size_gb = var.os_disk_size_gb
}
