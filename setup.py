#!/usr/bin/env python3
"""
Tam Otomatik Setup Betiği
Tüm gerekli işlemleri tamamlar
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from elevenlabs import AsyncElevenLabs

print("=" * 60)
print("🚀 ElevenLabs Speech Engine - Otomatik Setup")
print("=" * 60)

load_dotenv()

async def main():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    public_ws_url = os.getenv("PUBLIC_WS_URL")
    engine_id = os.getenv("ELEVENLABS_SPEECH_ENGINE_ID")
    
    print(f"\n✅ Kontroller:")
    print(f"   API Key: {'✓ Set' if api_key else '✗ Missing'}")
    print(f"   PUBLIC_WS_URL: {'✓ Set' if public_ws_url else '✗ Missing'}")
    print(f"   Engine ID: {'✓ Set' if engine_id else '✗ Missing (oluşturulacak)'}")
    
    if not api_key:
        print("\n❌ ELEVENLABS_API_KEY .env'de yok!")
        sys.exit(1)
    
    if not public_ws_url:
        print("\n❌ PUBLIC_WS_URL .env'de yok!")
        sys.exit(1)
    
    elevenlabs = AsyncElevenLabs(api_key=api_key)
    
    # Engine ID varsa kontrol et, yoksa oluştur
    if engine_id:
        print(f"\n✅ Mevcut Engine ID kullanılıyor: {engine_id}")
    else:
        print(f"\n🔄 Yeni Speech Engine oluşturuluyor...")
        print(f"   WebSocket URL: {public_ws_url}")
        
        try:
            engine = await elevenlabs.speech_engine.create(
                name="My Speech Engine",
                speech_engine={"ws_url": public_ws_url},
                overrides={"first_message": True},
            )
            
            engine_id = engine.engine_id
            print(f"\n✅ Speech Engine başarıyla oluşturuldu!")
            print(f"📝 Engine ID: {engine_id}")
            
            # .env dosyasını güncelle
            with open(".env", "a") as f:
                f.write(f"\nELEVENLABS_SPEECH_ENGINE_ID={engine_id}\n")
            
            print(f"✅ Engine ID .env dosyasına kaydedildi")
            
        except Exception as e:
            print(f"\n❌ Hata oluştu: {str(e)}")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ SETUP TAMAMLANDI!")
    print("=" * 60)
    print(f"\n📋 Yapılandırma Özeti:")
    print(f"   API Key: {api_key[:20]}...")
    print(f"   WebSocket URL: {public_ws_url}")
    print(f"   Engine ID: {engine_id}")
    print(f"   Port: {os.getenv('PORT', '3001')}")
    
    print(f"\n🚀 Sunucuyu başlatmak için şu komutu çalıştır:")
    print(f"   python app.py")
    
    print(f"\n🌐 Tarayıcıda aç:")
    print(f"   http://localhost:3001")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
