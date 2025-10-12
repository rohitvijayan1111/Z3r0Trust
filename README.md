# 🔐 Z3r0Trust – Trust Me, Always Verified  

Z3r0Trust is an **autonomous multi-agent security framework** designed to safeguard enterprise and cloud-based systems against modern cyber threats. It continuously authenticates, detects, analyzes, responds, and manages suspicious activities - ensuring transparency, fairness, and SOC oversight powered by **open-source technologies**.

Unlike traditional SIEMs that only record events, **Z3r0Trust** integrates **open-source identity management**, **real-time log intelligence**, **autonomous response**, and **human appeal workflows** to build a **resilient, adaptive, and intelligent defense ecosystem**.

It acts as a **middleware security layer** for third-party applications, protecting them from brute force, credential stuffing, suspicious API usage, and more. Any application integrating with Z3r0Trust routes backend traffic through its middleware, ensuring logs are captured, anomalies detected, and malicious actors blocked automatically.

---

## 📛 Project Info  

| Field | Description |
|---|---|
| **Project Name** | Z3r0Trust – Trust Me, Always Verified |
| **Short Description** | An AI-driven, multi-agent framework leveraging **open-source identity management** for secure inter-agent communication, autonomous detection & response, and fair user management. |
| **Team Name** | United Hackos |
| **Hackathon / Domain** | Thales GenTech India Hackathon 2025 |
| **Thales Domains Addressed** | Data, Identity & Access Management (Descope)  <br>• Threat Detection & Incident Response<br>• AI & Autonomous Systems Security |

---

## 👥 Team – United Hackos  

We are **United Hackos**, a passionate team of developers and security innovators dedicated to building resilient, human-centric cyber defense systems.  
Our expertise spans **full-stack development, cybersecurity, machine learning, DevOps, cloud computing, and UI/UX design**, enabling us to deliver scalable end-to-end solutions.

**Team Members:**  
* [Rohit Vijayan B](https://www.linkedin.com/in/rohitvijayan1111/)  
* [Divakar G](https://www.linkedin.com/in/divakar3501/)  
* [Rithik Raja S](https://www.linkedin.com/in/rithik-raja-s/)  
* [Gokul J](https://www.linkedin.com/in/gokul-jeyachandran-37a649229/)  
* [Kaviyarasu S](https://www.linkedin.com/in/kaviyarasu-sivaraj-312893262/)  

---

## 🎯 Hackathon Theme / Challenge Addressed  

**Hackathon:** Thales GenTech India Hackathon 2025  
**Theme:** Cybersecurity – Creating smart solutions to protect India’s digital space, especially around **cloud security**, **AI model safety**, and **threat detection**.

We specifically align with these Thales domains:  
1. **Identity & Access Management (IAM)** — continuous authentication, scoped tokens, delegation(Descope)  
2. **Threat Detection & Incident Response** — anomaly detection, automated containment, alerting  
3. **AI & Autonomous Systems Security** — explainable autonomous agents, fairness, human override  

**Evaluation Criteria:**  
✅ Relevance to Thales domains  
✅ Utilisation of open-source technologies  
✅ Adaptability to diverse scenarios  
✅ Ease of design, extensibility, and scalability  

---

## 📌 Problem  

Enterprises and cloud environments face persistent challenges:

- Credential theft and phishing are major attack vectors  
- SOC teams are overwhelmed by repetitive alerts  
- Manual triage causes slow incident responses  
- Legitimate users often face unfair account restrictions  

Logs alone are not enough — Z3r0Trust converts raw data into actionable insights via autonomous containment and fair, AI-guided decisions.

---

## 🏗 Solution  

Z3r0Trust introduces a **coordinated system of specialized agents**, each with distinct responsibilities.  
All inter-agent communication is secured through **open-source IAM** with scoped access, ensuring strict trust boundaries and delegated operations.

**Third-party integration flow:**

- Third-party apps integrate via Z3r0Trust middleware proxy  
- Traffic is verified, authenticated, and enriched with user attributes  
- Logs are captured, anomalies detected, and malicious actions mitigated automatically  

---

### 🔒 Alignment with Thales Hackathon Goals  

- ✅ Strengthens **cloud security** via agent-driven anomaly detection  
- ✅ Promotes **AI model safety** through autonomous, explainable responses  
- ✅ Utilizes **open-source tools** (Descope, Splunk, FastAPI, React)  
- ✅ Scalable and adaptable to **multi-domain cybersecurity** use cases  
- ✅ Designed for **extensibility and integration** into enterprise ecosystems  

---

## 🏗 Deployment Links (Working Prototype)  

🔗 [Z3r0Trust Deployment](https://zero--trust.web.app/)  

---

## 🔑 Key Features  

- 🔒 Authentication & validation via **open-source IAM**  
- 📡 **Splunk real-time analytics** for anomaly detection  
- 🤖 **AI-powered log summarization** for SOC clarity  
- ⚡ Automated response: block, suspend, or monitor  
- 📬 Tiered notifications for users and SOC  
- 🧑‍💼 Human oversight via a **SOC dashboard**  
- 📝 Transparent appeal system for fair handling  
- 📜 Immutable audit trails ensuring compliance  

---

## 🧩 Architecture  

```mermaid
flowchart LR
  A[User Login/Action] -->|Logs + Auth| B[Detector Agent]
  B -->|Attributes + Tokens| C[Analyser Agent]
  C -->|Splunk HEC| D[Alert Handler Agent]
  D -->|Notify| E[Mail MCP Agent]
  D -->|DB Update| F[Database Controller Agent]
  D -->|Appeals| G[Appeal Handler Agent]
  E --> H[User]
  E --> I[SOC Analyst]
  I -->|Review/Override| G
  G -->|Reinstatement| F
```

---

## 🏗 Systematic Work Flow

![WhatsApp Image 2025-09-08 at 18 22 49\_694ac8cd](https://github.com/user-attachments/assets/000c5550-b0ca-4785-96d2-bf742d9ada4c)

## 🤖 Agents

### 🔍 Detector Agent

* Authenticates with **Descope**.
* Retrieves user attributes (IP, device, geo, MFA status).
* Validates logins and flags anomalies.
* Forwards enriched logs to **Splunk**.

### 📊 Analyser Agent

* Receives logs from Detector Agent.
* Sends data to **Splunk** for real-time processing.
* Splunk processes in 3 tiers:
  * **High Frequency (5 mins):** Brute force, credential stuffing, suspicious API usage, bot/malware.
  * **Medium Frequency (30 mins):** Impossible travel, account takeover, privilege escalation.
  * **Low Frequency (5 hrs):** Data exfiltration, insider abuse, network anomalies.
* Maintains **MD5 hash cache** (alert\_name.username.ip.device) to prevent duplicate alerts.
* Forwards validated anomalies to Alert Handler Agent.

### 🚨 Alert Handler Agent

* Processes alert data.
* Decides on appropriate action:
  * Temporary/Permanent block
  * User logout or session invalidation
  * Enforce MFA
* Coordinates with Mail Sender, Database Controller, and Appeal Handler.
* Creates **appeal tickets** in DB.

### 📧 Mail Sender Agent

* Handles outbound email notifications.
* Pre-configured with secure sender ID and app passkey.
* Use cases:
  * Alert user of suspicious activity.
  * Notify SOC with forensic details.
  * Confirm appeal submission.
  * Notify user of account reinstatement.

### 🗄 Database Controller Agent

* Securely interfaces with the database under scoped privileges.
* Only executes *traceable and recoverable* operations.
* Acts as a delegate to SOC for safe query execution.

### 📝 Appeal Handler Agent

* Activated when a user submits an appeal.
* Reviews alert data + user message.
* If low risk, reinstates account autonomously.
* If uncertain, escalates to **SOC Analyst**.
* Updates DB and notifies user via Mail Sender.

➡️ The last four agents (Alert Handler, Mail Sender, Database Controller, and Appeal Handler) communicate among themselves using secure access keys. If any third party attempts to access them without proper authorization, they are instantly blocked through strict access key validation and security policies.

---

## 📂 Example Work Flow (Scenario Based)

**Scenario:** Multiple failed logins → sudden success from a new device in Moscow.

1. **Detector** authenticates login via **Descope OAuth**, retrieves attributes, and sends enriched logs to Splunk.
2. **Analyser** correlates with Splunk, scores risk as High.
3. **Alert Handler** suspends account, updates Alerts DB.
4. **Mail MCP Agent** sends:

   * ✉ User-friendly alert to employee
   * 📑 SOC email with forensic details
5. **SOC Analyst** validates the suspension.
6. **Appeal Agent** reviews employee’s appeal, reinstates if legitimate.

➡ Threat contained instantly  
➡ SOC informed with summarized context  
➡ User treated fairly with transparent process  
➡ Full **Descope-based trust validation** ensured

---

## ⚙️ What We Built + How to Run It

Z3r0Trust is a **multi-agent security system** aligns with **Thales Domains**.

### Core Workflow

* **Detector Agent**: Validates sessions via Descope, enriches data, forwards to Splunk.
* **Analyser Agent**: Performs correlation, risk scoring.
* **Alert Handler Agent**: Takes enforcement actions (block/logout/MFA).
* **Mail Agent**: Notifies users + SOC.
* **Appeal Agent**: Provides human fairness and consent-based reinstatements.
  
---
## 🚀 Z3r0Trust - Setup & Run Guide

This guide explains how to set up and run the Z3r0Trust project step by step.

📦 Prerequisites

    -> Python 3.10+
    
    -> Node.js (>=18.x) + npm
    
    -> pip (Python package manager)
    
    -> A Gmail App Password (for email sending)

    -> Splunk Enterprise
    
    -> A Descope account (for authentication & management keys)

⚙️ Environment Variables


1️⃣ Clone the Repository
```
git clone https://github.com/rohitvijayan1111/Z3r0Trust/
cd Z3r0Trust/Agent
```
Create a .env file inside Z3r0Trust/Agent folder with the following:
```
# API Keys
PHI_API_KEY=your_phi_api_key
GROQ_API_KEY=your_groq_api_key
GMAIL_PASSKEY=your_gmail_app_password
DESCOPE_MANAGEMENT_KEY=your_descope_management_key
DESCOPE_PROJECT_ID=your_descope_project_id

# Agent Access Keys (for secure internal communication)
EMAIL_SENDER_AGENT_ACCESS_KEY=your_email_sender_access_key
ALERT_HANDLER_AGENT_ACCESS_KEY=your_alert_handler_access_key
DB_CONTROLLER_AGENT_ACCESS_KEY=your_db_controller_access_key
APPEAL_HANDLER_AGENT_ACCESS_KEY=your_appeal_handler_access_key

# Models and Services
GROQ_MODEL_1=llama-3.1-70b-versatile   # or any supported model
IP_AND_PORT_1=http://localhost:2222
IP_AND_PORT_2=http://localhost:5000

```
⚠️ Never commit .env to GitHub. It’s already added to .gitignore.


2️⃣ Run the Agent Service
```
pip install -r requirements.txt
python app.py
```
3️⃣ Run the Z3r0Trust - Backend
```
cd ../backend
pip install -r requirements.txt
python app.py
```
4️⃣ Run the Z3r0Trust - Frontend
```
cd ../frontend/zero-trust
npm install
npm run dev
```
5️⃣ Run the Third Party Application (Bank Management App)
```
cd ../Bank
npm install
npm run dev
```
    Login Credentials (Bank Management App)
      Login Id: diva22022.it@rmkec.ac.in
      Password: 123qwe!@#QWE

6️⃣ Bank - Backend ( Z3r0Trust works as Middleware using descope)
```
cd ../Bank/backend
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 4000
```
7️⃣ Splunk - Analyzer Agent Working
```
start the splunk enterprise application from start menu
splunk server will start in server URL = 127.0.0.1:8001
Create an index called ZeroTrust logs to save the logs from the detector agent
Configure alerts going into search and reporting, paste the SPL query in it and save it , name the alert, configure CRON job according to the frequency of the threat and set trigger to webhook and paste the url of the Agent's backend service.
SPL queries of various threats - 
```

The frontend will be available at:
```
👉 http://localhost:5173
```

✅ Notes

Agents communicate securely using the access keys defined in .env.

Ensure all services (Agent, Backend, Frontend) are running simultaneously.

Use Gmail App Password (not your Gmail login password).

Update .env values with actual keys from Descope and Groq.

---

## 🛠 Tech Stack

* **Auth & Trust** – Descope Console (OAuth, Flows, Scoped Tokens)
* **Backend Agents** – Python backend(FastAPI, Flask), MCP and FastMCP, Phidata Agents and Tools
* **Log Analytics** – Splunk (SPL, HEC)
* **Frontend Dashboard** – React
* **Database** – MySQL
* **Email Service** – GROQ-based templating
* **Cloud Services** – Google Console
---

### 🎥 Demo Video

📺 \[[Z3R0 Trust - Trust Me, Always Verified (Prototype Video)](https://youtu.be/oAwjJabutoY)]

---
### 📸 Snapshots


## 🖥️Deployment Details:

<p align="center">
  <img src="https://github.com/user-attachments/assets/58c505e2-25bd-4fbb-97db-82cdcb7f1278" width="45%" />
  <img src="https://github.com/user-attachments/assets/9aa6d181-510f-46be-a654-a1b6aac9c6bf" width="45%" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/7dba4a46-a472-47c4-80c4-1960c898adf2" width="45%" />
  <img src="https://github.com/user-attachments/assets/43de869a-244d-4f6a-a312-60e2b7644b37" width="45%" />
</p>

## 🖥️ Prototype:

<p align="center">
  <img src="https://github.com/user-attachments/assets/3240035c-b8b2-42f5-aac8-7aed1a0d5b3d" width="22%" />
  <img src="https://github.com/user-attachments/assets/01c697a4-4ad0-4096-9c75-440b54aa0030" width="22%" />
  <img src="https://github.com/user-attachments/assets/5b0611f4-3520-4495-9169-f37b8151bec4" width="22%" />
  <img src="https://github.com/user-attachments/assets/5be65473-432d-4c61-af5c-15d64e65928e" width="22%" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/c8f95d60-7e3d-4155-9875-a003af147a7b" width="22%" />
  <img src="https://github.com/user-attachments/assets/7e51e676-a93e-4302-8120-92aebd92d4c8" width="22%" />
  <img src="https://github.com/user-attachments/assets/ea3aaedd-f297-4bc7-94d6-9778ea8b2daa" width="22%" />
  <img src="https://github.com/user-attachments/assets/48239b86-8538-4799-992e-bd42cc6df3bf" width="22%" />
</p>

---

## 🎥 PPT Link

📺 [PPT Link](https://drive.google.com/file/d/1fYZRbzq2pA29tYjK-mGMvCXn1-LyPcj_/view?usp=sharing)


## 🔮 Future Advancements (What We’d Do With More Time)

* 🚀 Extend adaptive **machine learning models** for advanced anomaly detection.
* 🔗 Correlate **multi-vector incidents** (e.g., brute force + privilege escalation).
* 🚀 upgrade the MVP to Production ready app 

---

## 📊 Impact

Z3r0Trust is built to be both **technically robust** and **human-centric**:

* Reduces breach risk while lowering SOC fatigue
* Balances automation with fairness via multi-agent autonomy
* Ensures **security-by-design** with scoped Descope tokens and access boundaries
* Demonstrates strong technical execution with **Splunk, Descope, FastAPI, React**
* Maintains **connectivity and reliability** through secure APIs and real-time updates

⚡ Currently, Z3r0Trust represents a **Minimal Viable Product (MVP)** – a foundational yet functional system that proves the effectiveness of Descope-secured multi-agent workflows while leaving space for future scaling.

---

## 📧 Contact  

**Team Sentinel 5**  

- RohitVijayan B : rohitvijayan1111@gmail.com (+91 9986913189)  
- Divakar G : divakar3501@gmail.com (+91 6382547207)  
- Rithik Raja S : rithikraja28.rr@gmail.com (+91 9952276785)  
- Gokul J : goku22028.it@rmkec.ac.in (+91 9080639960)  
- Kaviyarasu S : kavirajmetech@gmail.com (+91 9360670658)  




