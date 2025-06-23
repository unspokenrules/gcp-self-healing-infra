from googleapiclient import discovery
from google.auth import default

def restart_vm(event, context):
    credentials, _ = default()
    compute = discovery.build('compute', 'v1', credentials=credentials)

    project = "YOUR_PROJECT_ID"
    zone = "us-central1-a"
    instance = "test-vm"

    request = compute.instances().reset(project=project, zone=zone, instance=instance)
    response = request.execute()
    print(f"Restarted VM '{instance}': {response}")
