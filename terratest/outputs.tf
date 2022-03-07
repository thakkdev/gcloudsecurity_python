output "some_output" {
  
  description = "any value"
  value = var.project
}

output "kmstestsaemail" {
  value = google_service_account.kmstestsa.email
}

output "service_url" {
  value = google_cloud_run_service.kmstest.status[0].url
}

output "toset" {
   value =   toset([
   "run.invoker"  ])
}

#output "keyring" {
#  description = "The name of the keyring."
#  value       = module.kms.keyring_resource.name
#}

#output "keyringlocation" {
#  description = "The location of the keyring."
#  value       = module.kms.keyring_resource.location
#}

#output "keyringkeys" {
#  description = "List of created kkey names."
#  value       = keys(module.kms.keys)
#}