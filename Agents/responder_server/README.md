# Responder Agent

This agent receives Splunk alerts, applies playbook policies, stores them in DB, and forwards actions to Email Agent & SOC.

## Run
```bash
pip install -r requirements.txt
python main.py
```

Endpoint: `http://127.0.0.1:6000/webhook`

Auth header required: `Authorization: Splunk <HEC_TOKEN>`
