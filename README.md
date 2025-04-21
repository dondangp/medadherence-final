# 💊 Medication Adherence Tracker

## 📘 Overview

The **Medication Adherence Tracker** is a web-based healthcare application that empowers patients to manage their medications, log daily intake, and receive timely reminders. Through adherence insights and visual analytics, the system helps identify gaps in medication routines and encourages consistent usage—crucial for managing chronic conditions.

---

## 🌟 Features

- 🔐 **Secure Login & Session Persistence**  
  Uses encrypted cookies for seamless login across refreshes.

- 👤 **User Profile Management**  
  Syncs with FHIR-compatible `Patient` resources for editable profile fields like name, birthdate, gender, contact info, address, race, ethnicity, and language.

- 💊 **Medication Management**  
  - View all active/inactive medications from `MedicationRequest.ndjson`  
  - RXNorm-based parsing and dosage display  
  - Prescriber and request metadata displayed

- ☑️ **Daily Medication Checklist**  
  - Track medications taken each day  
  - Logs entries to `MedicationAdministration.ndjson`  
  - Supports duplicate protection and visual indicators

- 📧 **Email Reminders**  
  - Sent automatically at **7 AM, 2 PM, and 7 PM**  
  - Includes only *unchecked* daily medications  
  - Personalized to each logged-in user  
  - Link provided to jump directly to the Medications tab

- 📊 **Analytics & Insights**  
  - Daily, weekly, and monthly adherence rates  
  - Missed medications by day and by medication  
  - Best/worst day tracker  
  - 30-day per-medication adherence bars  
  - Weekly pattern detection (day-of-week trend analysis)  
  - Visual graphs powered by Plotly  
  - Downloadable **PDF Summary Report**

- 🧠 **AI Medication Insights (Optional)**  
  - GPT-powered summaries of medication use  
  - Side effect prediction and drug interaction analysis  
  - Weekly insights generated in the History tab

- 🌙 **Dark/Light Mode Toggle**  
  Persistent theme selector with modern UI styling

- ❓ **Help Tab with FAQs & Contact Info**  
  Includes usage guidance and support links

---


## 🧰 Tech Stack

### 📦 Frontend
- [Streamlit](https://streamlit.io/) – UI framework for real-time interaction

### 🧠 Backend
- **Python** – Core language
- `uuid`, `json`, `datetime`, `smtplib` – for file handling, email, and scheduling

### 🗃 Data Storage
- Local NDJSON files:
  - `Patient.ndjson`
  - `MedicationRequest.ndjson`
  - `MedicationAdministration.ndjson`
  - `AllergyIntolerance.ndjson`, `Condition.ndjson`, `Immunization.ndjson`

### 🔁 Scheduling & Automation
- Custom Python scheduler thread running inside Streamlit app
- Sends **email reminders** using **SMTP (Gmail)**

### 📧 Email Delivery
- Gmail App Password for SMTP
- `email.message.EmailMessage`

---
