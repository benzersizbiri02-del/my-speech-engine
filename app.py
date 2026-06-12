"""Flask uygulaması - Token endpoint ve statik dosyalar"""
import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, jsonify
from elevenlabs import AsyncElevenLabs

load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ElevenLabs istemcisi
elevenlabs = AsyncElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


@app.route("/api/token", methods=["GET"])
def get_token():
    """Browser için WebRTC token'ı döndür"""
    try:
        # Async işlemi Flask içinde çalıştır
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def fetch_token():
            response = await elevenlabs.conversational_ai.conversations.get_webrtc_token(
                agent_id=os.getenv("ELEVENLABS_SPEECH_ENGINE_ID")
            )
            return response.token
        
        token = loop.run_until_complete(fetch_token())
        loop.close()
        
        return jsonify({"token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Sunucu sağlık kontrolü"""
    return jsonify({
        "status": "healthy",
        "api_key_set": bool(os.getenv("ELEVENLABS_API_KEY")),
        "engine_id_set": bool(os.getenv("ELEVENLABS_SPEECH_ENGINE_ID"))
    })


@app.route("/", methods=["GET"])
def index():
    """Ana sayfa - Browser istemcisini sun"""
    return app.send_static_file("client.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))
    print(f"\n🚀 Sunucu başlatılıyor: http://localhost:{port}")
    print(f"Token endpoint: http://localhost:{port}/api/token")
    print(f"Sağlık kontrolü: http://localhost:{port}/health\n")
    
    app.run(host="0.0.0.0", port=port, debug=True)
