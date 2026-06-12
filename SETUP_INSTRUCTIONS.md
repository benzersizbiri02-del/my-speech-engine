# 🚀 Speech Engine Kurulum Adımları

## 1. Proje Dosyalarını İndir

```bash
git clone https://github.com/benzersizbiri02-del/my-speech-engine.git
cd my-speech-engine
```

## 2. Python Ortamını Kur

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

## 4. Ortam Değişkenlerini Ayarla

```bash
cp .env.example .env
```

Sonra `.env` dosyasını açın ve bilgilerini girin:

```bash
ELEVENLABS_API_KEY=sk_...  # ElevenLabs hesabınızdan alın
```

## 5. ngrok Kur (Yerel Geliştirme İçin)

### macOS (Homebrew)
```bash
brew install ngrok
```

### Linux
```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
unzip ngrok-v3-stable-linux-amd64.zip
```

### Windows
- https://ngrok.com/download adresinden indir
- ZIP dosyasını aç

## 6. ngrok'u Başlat (Terminal 1)

```bash
ngrok http 3001
```

Çıktıda şu gibi bir URL göreceksiniz:
```
Forwarding                    https://abc-123-456.ngrok.app -> http://localhost:3001
Forwarding                    https://abc-123-456.ngrok.app -> http://localhost:3001
```

wss:// versiyonunu kopyalayın (örn: `wss://abc-123-456.ngrok.app/ws`)

## 7. .env Dosyasını Tamamla (Terminal 2)

```bash
export PUBLIC_WS_URL="wss://abc-123-456.ngrok.app/ws"
```

Veya `.env` dosyasına ekleyin:
```
PUBLIC_WS_URL=wss://abc-123-456.ngrok.app/ws
```

## 8. Speech Engine Kaynağı Oluştur (Terminal 2)

```bash
python create_engine.py
```

Çıktıda şu gibi bir Engine ID göreceksiniz:
```
✅ Speech Engine başarıyla oluşturuldu!
📝 Engine ID: seng_abc123def456

💾 Bunu .env dosyasına ekleyin:
ELEVENLABS_SPEECH_ENGINE_ID=seng_abc123def456
```

## 9. Engine ID'sini .env'ye Ekle

```bash
echo 'ELEVENLABS_SPEECH_ENGINE_ID=seng_...' >> .env
```

## 10. Flask Sunucusunu Başlat (Terminal 2)

```bash
python app.py
```

Çıktıda şu görünmeli:
```
🚀 Sunucu başlatılıyor: http://localhost:3001
Token endpoint: http://localhost:3001/api/token
Sağlık kontrolü: http://localhost:3001/health
```

## 11. Speech Engine WebSocket Sunucusunu Başlat (Terminal 3) - OPSİYONEL

Eğer özel callback'ler kullanmak istiyorsanız:

```bash
python server.py
```

## 12. Browser'da Test Et

```
http://localhost:3001
```

"Başla" butonuna tıklayın ve konuşmaya başlayın! 🎤

---

## Sorun Giderme

### "connection refused" hatası
- Flask sunucusu çalışıyor mu kontrol edin
- Port 3001 başka bir uygulama tarafından kullanılıyor mu kontrol edin

### ngrok URL'si çalışmıyor
- ngrok çalışıyor mu kontrol edin (Terminal 1)
- URL'yi .env dosyasına ekledin mi kontrol edin

### Token alınamıyor
- API key doğru mu kontrol edin
- Speech Engine ID oluşturuldu mu kontrol edin

### WebSocket bağlantısı başarısız
- Flask çalışıyor mu kontrol edin
- ngrok URL'si doğru mu kontrol edin
- Browser konsolunda hata var mı kontrol edin (F12)

---

## Sonraki Adımlar

✅ **Production İçin:**
- ngrok yerine gerçek domain kullanın
- HTTPS/WSS kullanın
- API key'i secure secrets yöneticisine koyun
- Kısa ömürlü token'lar kullanın
- Cors ve rate limiting ekleyin

✅ **React İntegrasyonu:**
- `browser-client-react.tsx` dosyasını kullanın
- Özel callback'ler ekleyin
- Stil geliştirin

✅ **Özel İşleme:**
- `server.py` dosyasında `SpeechEngineCallbacks` sınıfını özelleştirin
- Güvenilir uygulama state'ine dönüşüm ekleyin
- Tool çağrıları ekleyin
