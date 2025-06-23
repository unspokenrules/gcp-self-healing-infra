# GCP Self-Healing VM (Uptime Check + Auto-Restart)

This project demonstrates a self-healing infrastructure pattern in Google Cloud Platform. When a VM becomes unreachable via an Uptime Check, a Cloud Monitoring alert is triggered, which sends a Pub/Sub message. A Cloud Function listens to that message and automatically restarts the affected VM.

## 🔧 Components Used
- Cloud Monitoring (Uptime Check + Alert Policy)
- Pub/Sub
- Cloud Functions (Python)
- Compute Engine

## 🚀 How It Works
1. Uptime check monitors VM on port 80
2. If the check fails, Monitoring fires an alert
3. Alert sends message to Pub/Sub topic
4. Cloud Function triggers on Pub/Sub and restarts the VM using GCP API

## 📂 Project Structure
```
gcp-self-healing-vm/
├── main.py               # Cloud Function logic
├── requirements.txt      # Python dependencies
├── alert-policy.json     # JSON config for alert policy
└── README.md             # Project documentation
```

## 🧪 Testing It
1. Deploy a VM and run Apache on it
2. Set up Uptime Check + Alert Policy
3. Deploy the Cloud Function
4. Stop Apache to simulate failure
5. Monitor alert trigger and VM restart in logs

## ✅ Result
The VM is automatically restarted without human intervention.
