# LiveKit Voice Assistant

## 📌 Overview
This project implements a voice assistant using LiveKit's Voice Pipeline Agent. It consists of a Flask backend for processing audio and a React-based frontend UI for voice interaction.

---

## 📌 Features
✅ **LiveKit Integration** - Real-time voice streaming using LiveKit's Voice Pipeline Agent.  
✅ **Flask Backend** - Handles requests, validates audio, and trims responses.  
✅ **ngrok for Tunneling** - Exposes the local server for public access.  
✅ **Error Handling** - Prevents invalid or excessively long audio responses.  
✅ Voice UI: A web interface to interact with the assistant.  

---

## 📌 Installation & Setup

### 🔹 1. Clone the Repository
```sh
git clone https://github.com/your-username/LiveKit-Voice-Assistant.git
cd LiveKit-Voice-Assistant
```

### 🔹 2. Install Dependencies
Ensure you have Python 3.8+ installed, then run:
#### **For Backend (Flask)**
```sh
pip install -r requirements.txt
```


#### **For Frontend (React)**
```sh
npx create-react-app livekit-voice-ui
cd livekit-voice-ui
npm install axios
```

## **📌 Expose the Flask Backend Using Ngrok**
Run the following command:
```sh
ngrok http 5000
```
Copy the public URL and replace `"https://your-ngrok-url.ngrok-free.app"` in `VoiceUI.js`.

---

### 🔹 3. Configure Environment Variables
Create a `.env` file in the project root and add your LiveKit credentials:
```sh
LIVEKIT_API_KEY=your_api_key
LIVEKIT_SECRET=your_secret
LIVEKIT_SERVER_URL=wss://your-livekit-server
FLASK_SERVER_URL=https://your-ngrok-url/validate_audio
```
⚠ **Note:** Replace `your-api-key`, `your-secret`, and `your-ngrok-url` accordingly.

---

## 📌 Running the Project

### 🔹 1. Start the Flask Server
```sh
python app.py
```

### 🔹 2. Start ngrok (if not running already)
```sh
ngrok http 5000
```
Copy the **ngrok public URL** and update `FLASK_SERVER_URL` in `.env`.

### 🔹 3. Start the LiveKit Agent
```sh
python agent.py start
```
## **📌 Run the Frontend**
Go to the `livekit-voice-ui` folder and start the app:
```sh
npm start
```
---

## 📌 Usage Guide
1️⃣ Speak into the assistant's microphone.  
2️⃣ The LiveKit agent streams your voice to the Flask server.  
3️⃣ The server processes the request and validates the response duration.  
4️⃣ If the response is **over 60 seconds**, it gets trimmed before playback.  

---

## 📌 Troubleshooting

### ❌ LiveKit cannot connect?
🔹 Ensure the **LiveKit Server URL** is correct in `.env`.  
🔹 Check that the server is running: `python agent.py start`.  

### ❌ ngrok URL keeps changing?
🔹 Manually update `.env` with the latest ngrok URL.  
🔹 Consider using an **ngrok reserved domain** for stability.  

### ❌ Permission Error (WinError 32)?
🔹 Close any process using the file (e.g., PyTorch hub cache).  
🔹 Restart your system or manually delete the `torch/hub` cache folder.  


---



