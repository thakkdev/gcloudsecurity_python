variable "project" {
description = "Google Project Id"
default = "terraform2022"
type = string

}

variable "region" {
    description = "region"
    type = string
    default = "us-east1"
  }

variable "keyringname" {
  description = "Keyring name."
  type        = string
  default = "kmstestprojkeyring"
}

variable "keyname" {
  description = "Key names."
  type        = list(string)
  default     = ["kmstestkeyname"]
}
