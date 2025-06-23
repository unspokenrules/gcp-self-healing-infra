# 🛠️ GCP Self-Healing Infrastructure (VM Auto-Restart)

This project showcases a **self-healing infrastructure pattern** in Google Cloud. It automatically detects when a VM is unreachable (via uptime check) and **auto-restores it** using a serverless function triggered by alerts.

Built with:
- 🧠 Cloud Monitoring (Uptime Checks + Alert Policies)
- 📬 Pub/Sub
- ⚙️ Cloud Functions (Python)
- 💻 Compute Engine VM

---

## ✅ What It Does

If a GCE VM goes down or stops responding to HTTP requests:
1. Cloud Monitoring's Uptime Check detects the failure.
2. An alert policy sends a message to a Pub/Sub topic.
3. A Cloud Function is triggered by that message.
4. The Function uses the GCP API to **restart the failed VM**.

---

## 📁 Project Structure

```
gcp-self-healing-infra/
├── main.py               # Cloud Function to restart VM
├── requirements.txt      # Python dependency
├── alert-policy.json     # Alert policy config (optional CLI method)
└── README.md             # This file
```

---

## 🚀 How to Set It Up

### 1️⃣ Deploy a Test VM
```bash
gcloud compute instances create test-vm \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --tags=http-server
```

### 2️⃣ Install Apache on the VM
```bash
gcloud compute ssh test-vm --zone=us-central1-a
sudo apt update && sudo apt install apache2 -y
sudo systemctl start apache2
```

### 3️⃣ Open Port 80 via Firewall
```bash
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags=http-server \
  --direction INGRESS \
  --priority 1000 \
  --network default
```

---

### 4️⃣ Create a Pub/Sub Topic
```bash
gcloud pubsub topics create vm-alert-topic
```

### 5️⃣ Register Pub/Sub as a Notification Channel  
🔧 Do this in **Cloud Console**:  
- Go to Monitoring → Alerting → Notification Channels  
- Scroll to **Pub/Sub**, click **Add**, and select `vm-alert-topic`

---

### 6️⃣ Deploy the Cloud Function
```bash
gcloud functions deploy restart_vm \
  --runtime=python311 \
  --trigger-topic=vm-alert-topic \
  --entry-point=restart_vm \
  --region=us-central1 \
  --timeout=60s \
  --memory=256MB
```

---

### 7️⃣ Set Up an Uptime Check
In GCP Console → Monitoring → Uptime Checks:
- Type: `Instance`
- Protocol: `HTTP`
- Port: `80`
- Resource: Select your `test-vm`

---

### 8️⃣ Create Alert Policy
In GCP Console → Monitoring → Alerting:
- Condition: Uptime check failed
- For: 1 minute
- Notification: Select the Pub/Sub topic

---

## 🔁 Test the Self-Healing Flow

To simulate a failure:
```bash
gcloud compute ssh test-vm --zone=us-central1-a
sudo systemctl stop apache2
```

✅ Within 1–2 minutes:
- Uptime check fails → alert fires
- Pub/Sub sends message
- Cloud Function triggers and restarts the VM

Check logs:
```bash
gcloud functions logs read restart_vm --region=us-central1
```

---

## 📌 Use Cases
- Auto-recovery for production workloads
- Reduce manual on-call burden
- Showcase DevOps/SRE automation maturity

![Image](https://github.com/user-attachments/assets/6d2af2ff-b147-4763-ab2d-6e28fea4c55f)

