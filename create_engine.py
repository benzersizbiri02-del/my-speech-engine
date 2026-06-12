"""Speech Engine kaynağı oluştur"""
import asyncio
import os
from dotenv import load_dotenv
from elevenlabs import AsyncElevenLabs

load_dotenv()


async def main():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    public_ws_url = os.getenv("PUBLIC_WS_URL")
    
    if not api_key:
        print("❌ ELEVENLABS_API_KEY .env dosyasında ayarlanmamış")
        return
    
    if not public_ws_url:
        print("❌ PUBLIC_WS_URL .env dosyasında ayarlanmamış")
        print("💡 ngrok çalıştırın: ngrok http 3001")
        print("💡 Ardından: export PUBLIC_WS_URL=wss://your-ngrok-domain.ngrok.app/ws")
        return
    
    elevenlabs = AsyncElevenLabs(api_key=api_key)
    
    try:
        print(f"\n🔄 Speech Engine kaynağı oluşturuluyor...")
        print(f"WebSocket URL: {public_ws_url}")
        
        engine = await elevenlabs.speech_engine.create(
            name="My Speech Engine",
            speech_engine={"ws_url": public_ws_url},
            overrides={"first_message": True},
        )
        
        print(f"\n✅ Speech Engine başarıyla oluşturuldu!")
        print(f"📝 Engine ID: {engine.engine_id}")
        print(f"\n💾 Bunu .env dosyasına ekleyin:")
        print(f"ELEVENLABS_SPEECH_ENGINE_ID={engine.engine_id}")
        
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
