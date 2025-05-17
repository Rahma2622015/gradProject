##  Graduation Project - Chatbot for CS Students

###  Purpose

This project is an intelligent chatbot designed to assist female students in the **Computer Science Department**. It uses **Natural Language Processing (NLP)** to understand and respond to queries in both **Arabic** and **English**. The chatbot also features customizable interface themes and allows users to **edit their messages** after sending.

---

###  Features

* Understands Arabic and English input.
* Changeable chat interface color.
* Frontend built with React for dynamic and responsive chat.

---

###  How to Run the Project

1. **Clone the repository**

```bash
git clone https://github.com/Rahma2622015/gradProject.git
```

2. **Install Backend Dependencies**

```bash
# Flask server and backend utilities
pip install flask
pip install flask-cors
pip install gevent
pip install sqlalchemy
pip install requests
pip install rapidfuzz

# NLP libraries
pip install nltk
pip install stanza
pip install language_tool_python
pip install flair
pip install sentence-transform
pip install autocorrect
pip install pyspellchecker
```

3. **Install Frontend Dependencies (React)**

```bash
npm install
npm install react-chat-elements       # For chat UI rendering
npm install emoji-picker-react        # For emoji support
npm install framer-motion             # For animations
npm install --save react-toastify     # For user notifications
```

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
