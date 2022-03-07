#key management service
#module "kms" {
#  source  = "terraform-google-modules/kms/google"
#  version = "~> 2.0"
# project_id = var.project
#  keyring    = var.keyringname
#  location   = var.region
#  keys       = var.keyname
#}

#Manually apply to KMS
#resource "google_kms_crypto_key_iam_binding" "binding" {
#  crypto_key_id = "${var.project}/${var.region}/${var.keyringname}/${var.keyname[0]}"
#  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"

#  members = [local.kmstest_sa]


#}