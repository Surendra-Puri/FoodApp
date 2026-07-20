module "aks" {
  source = "git::https://github.com/Surendra-Puri/Terraform-Modules.git//AKS?ref=main"

  name      = "aks-lab"
  location  = "Central India"
  parent_id = "/subscriptions/.../resourceGroups/rg-test"
  vm_size   = "Standard_B2s"
}