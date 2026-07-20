module "aks" {
  source = "../modules/aks"

  name      = "aks-lab"
  location  = "Central India"
  parent_id = "/subscriptions/.../resourceGroups/rg-test"
  vm_size   = "Standard_B2s"
}