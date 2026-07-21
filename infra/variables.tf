variable "aks_name" {
  type = string
}

variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "vm_size" {
  type = string
}

variable "node_count" {
  type    = number
  default = 1
}

variable "os_disk_size" {
  type    = number
  default = 35
}