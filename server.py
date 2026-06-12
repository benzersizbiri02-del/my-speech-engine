"""ElevenLabs Speech Engine WebSocket Sunucusu"""
import asyncio
import os
from dotenv import load_dotenv
from elevenlabs import AsyncElevenLabs

load_dotenv()


class SpeechEngineCallbacks:
    """Speech Engine callback'leri"""
    
    async def on_open(self, session):
        """Oturum açıldığında"""
        print(f"✅ Oturum açıldı: {session.id}")
    
    async def on_message(self, message):
        """Kullanıcı mesajı alındığında"""
        print(f"🎤 Kullanıcı: {message.text}")
        
        # Güvenlik: Ham konuşma metni doğrudan kullanılmamalıdır
        # Burada güvenilir uygulama state'ine dönüştürün
        
        # Örnek: Basit yanıt
        response_text = f"Şunları söylediniz: {message.text}"
        
        return response_text
    
    async def on_close(self, session):
        """Oturum temiz şekilde kapandığında"""
        print(f"👋 Oturum kapandı: {session.id}")
    
    async def on_disconnect(self, session):
        """Oturum beklenmedik şekilde kesintiye uğradığında"""
        print(f"⚠️ Oturum koptu: {session.id}")


async def main():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    engine_id = os.getenv("ELEVENLABS_SPEECH_ENGINE_ID")
    
    if not api_key or not engine_id:
        print("❌ ELEVENLABS_API_KEY veya ELEVENLABS_SPEECH_ENGINE_ID ayarlanmamış")
        print("💡 Önce create_engine.py çalıştırın")
        return
    
    elevenlabs = AsyncElevenLabs(api_key=api_key)
    callbacks = SpeechEngineCallbacks()
    
    try:
        print(f"\n🚀 Speech Engine WebSocket Sunucusu başlatılıyor...")
        print(f"Engine ID: {engine_id}")
        print(f"Port: 3001")
        print(f"Path: /ws\n")
        
        engine = await elevenlabs.speech_engine.get(engine_id)
        
        await engine.serve(
            port=3001,
            path="/ws",
            debug=True,
            callbacks={
                "on_open": callbacks.on_open,
                "on_message": callbacks.on_message,
                "on_close": callbacks.on_close,
                "on_disconnect": callbacks.on_disconnect,
            }
        )
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")
        print(f"💡 Lütfen ortam değişkenlerini kontrol edin")


if __name__ == "__main__":
    asyncio.run(main())
