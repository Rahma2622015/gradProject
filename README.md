##  Graduation Project - Chatbot for CS Students

###  Purpose

This project is an intelligent chatbot designed to assist students in the **Computer Science Department**. It uses **Natural Language Processing (NLP)** to understand and respond to queries in both **Arabic** and **English**. The chatbot also features customizable interface themes and allows users to **edit their messages** after sending.

---

###  Features

* Understands Arabic and English input.
* Changeable chat interface color.
* Frontend built with React for dynamic and responsive chat.

---

###  How to Run the Project

### Prerequisites
- Python 3.8 or higher
- Node.js v16 or higher
- npm v8 or higher
- Git installed
1. **Clone the repository**

```bash
git clone https://github.com/Rahma2622015/gradProject.git
```
2. **Navigate to project directory:**
    - cd gradProject
3. **Create virtual environment (Windows):**
   - python -m venv venv
   - venv\Scripts\activate
3.1.**Or on macOS/Linux:**
   - python3 -m venv venv
   - source venv/bin/activate
4. **Install Backend & Ai Dependencies**
    - pip install -r requirements.txt
5. **Install Frontend Dependencies (React)**

```bash
npm install
npm install react-chat-elements       # For chat UI rendering
npm install emoji-picker-react        # For emoji support
npm install framer-motion             # For animations
npm install --save react-toastify     # For user notifications
```
6.**Run the backend:**
  - python mainApp.py
  
### Frontend Setup (React)
1. Navigate to front_end:
  cd front_end
2. Install packages:
  npm install
3. Start React app:
  npm start

### Troubleshooting
- Flask not starting? Make sure port 5000 is not in use.
- CORS issues? Ensure frontend and backend are on correct ports.
- Missing packages? Try `npm cache clean --force` and re-run `npm install`.

---

###  Project Structure

gradProject/

├── front\_end	# Contains the frontend code built using React and Next.j

├── Database	# Includes the SQLite or other database files and related

├── Ai	# NLP and AI models

├── endpoints	# Contains the core API functions (

├── Modules	# Helper and utility functions used by the backend

├── mainApp.py # The main entry point that runs the Flask server

├── cert.crt	# SSL certificate file for enabling HTTPS (used with priv

├── private.key	# Private key for SSL encryption

├── variables.py	# Contains configurable variables and constants

└── routes	# Holds the API route definitions

---

###  Use Cases

* Help CS students with questions about subjects, schedules, and regulations.
* Smart assistant for responding to frequently asked questions.

---

### Team Members

• **Heba Gamal Ahmed Abdel shafi**

• **Hagar Mohamed Kamel sayed**

• **Rahma Mohamed Sayed**

• **Hager Basuony Attia**
