#Cloud run service
resource "google_cloud_run_service" "kmstest" {

    name = local.service_name
    location = var.region
    autogenerate_revision_name = true

    template {
      spec {
        service_account_name = google_service_account.kmstestsa.email
        containers {
          image = "us-east1-docker.pkg.dev/terraform2022/kmtestrepo/my-image"
          
        }
      }
    }
   
    traffic {
    percent         = 100
    latest_revision = true
  }
   depends_on = [google_project_service.run]
  }

# Set service public
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

# create policy
resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.kmstest.location
  project  = google_cloud_run_service.kmstest.project
  service  = google_cloud_run_service.kmstest.name

  policy_data = data.google_iam_policy.noauth.policy_data
  depends_on  = [google_cloud_run_service.kmstest]
}
