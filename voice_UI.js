import React, { useState, useRef } from "react";
import axios from "axios";

const VoiceUI = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    
    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorderRef.current.onstop = async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      setAudioBlob(audioBlob);
      sendAudio(audioBlob);
      audioChunksRef.current = [];
    };

    mediaRecorderRef.current.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  const sendAudio = async (blob) => {
    const formData = new FormData();
    formData.append("audio", blob, "recording.wav");

    try {
      const response = await axios.post("https://your-ngrok-url.ngrok-free.app/process_audio", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      console.log("Response:", response.data);
    } catch (error) {
      console.error("Error sending audio:", error);
    }
  };

  return (
    <div className="voice-ui">
      <h2>LiveKit Voice Assistant</h2>
      <button onClick={isRecording ? stopRecording : startRecording}>
        {isRecording ? "Stop Recording" : "Start Recording"}
      </button>
      {audioBlob && <audio controls src={URL.createObjectURL(audioBlob)} />}
    </div>
  );
};

export default VoiceUI;
