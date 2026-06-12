"""React Browser Client - @elevenlabs/react ile tam konuşma desteği"""
import { useConversation } from "@elevenlabs/react";
import { useState } from "react";

export function VoiceControls() {
  const [isMuted, setIsMuted] = useState(false);
  const [transcript, setTranscript] = useState<string[]>([]);

  const conversation = useConversation({
    onConnect: () => {
      console.log("✅ Bağlandı");
      setTranscript([]);
    },
    onDisconnect: () => {
      console.log("👋 Bağlantı kesildi");
    },
    onError: (error) => {
      console.error("❌ Hata:", error);
      setTranscript((prev) => [...prev, `Hata: ${error.message}`]);
    },
    onMessage: (message) => {
      console.log("📨 Mesaj:", message);
      setTranscript((prev) => [...prev, `Asistan: ${message}`]);
    },
    onStatusChange: (status) => {
      console.log("🔄 Durum:", status);
    },
  });

  async function startConversation() {
    try {
      // Mikrofon izni iste
      await navigator.mediaDevices.getUserMedia({ audio: true });

      // Token al
      const { token } = await fetch("/api/token").then((res) => res.json());

      // Oturumu başlat
      await conversation.startSession({
        conversationToken: token,
        overrides: {
          agent: { firstMessage: "Merhaba! Nasıl yardımcı olabilirim?" },
        },
      });
    } catch (error) {
      console.error("Bağlantı hatası:", error);
    }
  }

  function stopConversation() {
    conversation.endSession();
  }

  function toggleMute() {
    if (conversation.isSpeaking) {
      conversation.interrupt();
    }
    setIsMuted(!isMuted);
  }

  return (
    <div className="voice-controls">
      <h2>🎤 Sesli Asistan</h2>

      <div className="status">
        <span>
          Durum:{" "}
          {conversation.status === "connected"
            ? "✅ Bağlandı"
            : conversation.status === "connecting"
              ? "🔄 Bağlanılıyor..."
              : "❌ Bağlantısız"}
        </span>
      </div>

      <div className="controls">
        <button
          onClick={startConversation}
          disabled={conversation.status !== "disconnected"}
          className="btn-start"
        >
          🎤 Başla
        </button>
        <button
          onClick={stopConversation}
          disabled={conversation.status === "disconnected"}
          className="btn-stop"
        >
          ⏹️ Durdur
        </button>
        <button
          onClick={toggleMute}
          disabled={conversation.status === "disconnected"}
          className="btn-mute"
        >
          {isMuted ? "🔇 Sesli Yap" : "🔊 Sessiz Yap"}
        </button>
      </div>

      <div className="transcript">
        <h3>Konuşma Transkripti</h3>
        {transcript.length === 0 ? (
          <p className="empty">Henüz bir konuşma yok...</p>
        ) : (
          <ul>
            {transcript.map((msg, i) => (
              <li key={i}>{msg}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default VoiceControls;
