/**
 * Vanilla JavaScript Browser Client - @elevenlabs/client ile konuşma
 * React kullanmadan direkt HTML/JS'de kullanılabilir
 */

import { Conversation } from "@elevenlabs/client";

class VoiceAssistant {
  constructor() {
    this.conversation = null;
    this.isMuted = false;
    this.transcript = [];
    this.initializeElements();
  }

  initializeElements() {
    this.startBtn = document.getElementById("startBtn");
    this.stopBtn = document.getElementById("stopBtn");
    this.transcriptDiv = document.getElementById("transcript");
    this.statusSpan = document.getElementById("statusText");

    this.startBtn.addEventListener("click", () => this.start());
    this.stopBtn.addEventListener("click", () => this.stop());
  }

  async start() {
    try {
      this.updateStatus("Bağlanılıyor...");
      this.startBtn.disabled = true;

      // Mikrofon izni iste
      await navigator.mediaDevices.getUserMedia({ audio: true });

      // Token al
      const response = await fetch("/api/token");
      const { token } = await response.json();

      // Conversation başlat
      this.conversation = new Conversation({
        onConnect: () => this.onConnect(),
        onDisconnect: () => this.onDisconnect(),
        onError: (error) => this.onError(error),
        onMessage: (message) => this.onMessage(message),
      });

      await this.conversation.startSession({
        conversationToken: token,
        overrides: {
          agent: { firstMessage: "Merhaba! Nasıl yardımcı olabilirim?" },
        },
      });
    } catch (error) {
      this.updateStatus(`Hata: ${error.message}`);
      this.startBtn.disabled = false;
    }
  }

  async stop() {
    if (this.conversation) {
      await this.conversation.endSession();
    }
  }

  onConnect() {
    this.updateStatus("✅ Bağlandı");
    this.stopBtn.disabled = false;
    this.addTranscript("Sistem", "Konuşma başladı", "assistant");
  }

  onDisconnect() {
    this.updateStatus("❌ Bağlantı kesildi");
    this.startBtn.disabled = false;
    this.stopBtn.disabled = true;
  }

  onError(error) {
    console.error("Hata:", error);
    this.addTranscript("Hata", error.message, "error");
  }

  onMessage(message) {
    console.log("Mesaj:", message);
    this.addTranscript("Asistan", message, "assistant");
  }

  updateStatus(text) {
    this.statusSpan.textContent = text;
  }

  addTranscript(name, text, type = "user") {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `<strong>${name}:</strong> ${text}`;
    this.transcriptDiv.appendChild(messageDiv);
    this.transcriptDiv.scrollTop = this.transcriptDiv.scrollHeight;
  }
}

// Sayfa yüklendiğinde başlat
window.addEventListener("load", () => {
  new VoiceAssistant();
});
