# ElevenLabs Speech Engine - Python Setup

Bu proje, ElevenLabs Speech Engine'i kullanarak gerçek zamanlı sesli konuşma özelliği ekleyen bir Python uygulamasıdır.

## Özellikler

- 🎙️ WebSocket tabanlı Speech Engine sunucusu
- 🔐 Güvenli token endpoint'i
- 🌐 Browser istemcisi (React)
- 🛡️ API Key koruması (sunucu tarafı)

## Hızlı Başlangıç

### 1. Gereksinimler

- Python 3.8+
- ElevenLabs API Key (hesabınızdan alın)
- ngrok (yerel geliştirme için)

### 2. Kurulum

```bash
# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 3. Ortam Değişkenlerini Ayarla

```bash
cp .env.example .env
# .env dosyasını düzenle ve API keyin'i ekle
```

### 4. Yerel Geliştirme için ngrok Setup

```bash
# Terminal 1: ngrok başlat
ngrok http 3001

# Terminal 2: PUBLIC_WS_URL'yi .env'ye ekle
export PUBLIC_WS_URL="wss://your-ngrok-domain.ngrok.app/ws"
```

### 5. Speech Engine Kaynağı Oluştur

```bash
python create_engine.py
```

Bu betik Speech Engine ID'sini konsola yazdıracak. `.env` dosyasına ekleyin.

### 6. Sunucuyu Başlat

```bash
python app.py
```

Sunucu `http://localhost:3001` adresinde çalışacak.

## Dosya Yapısı

```
.
├── .env.example           # Ortam değişkenleri şablonu
├── .gitignore            # Git'e göre dosyaları yoksay
├── requirements.txt      # Python bağımlılıkları
├── README.md             # Bu dosya
├── app.py                # Flask sunucusu (token endpoint)
├── create_engine.py      # Speech Engine kaynağı oluştur
├── server.py             # Speech Engine WebSocket sunucusu
└── static/
    └── client.html       # Browser istemcisi
```

## API Endpoints

### Token Endpoint

```
GET /api/token
```

Browser için WebRTC token döndürür.

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Güvenlik Notları

- ⚠️ **API Key'i asla browser koduna koymayın**
- Token endpoint'i sunucu tarafında korunmalıdır
- Production'da HTTPS kullanın
- Kısa ömürlü token'lar kullanın

## Troubleshooting

### WebSocket bağlantısı başarısız
- ngrok çalışıyor mu kontrol edin
- `PUBLIC_WS_URL` doğru şekilde ayarlandı mı kontrol edin
- ELEVENLABS_API_KEY geçerli mi kontrol edin

### Token alınamıyor
- Flask sunucusu çalışıyor mu kontrol edin
- `/api/token` endpoint'ine erişebiliyor musunuz test edin

## Referanslar

- [ElevenLabs Documentation](https://elevenlabs.io/docs)
- [Speech Engine Guide](https://elevenlabs.io/docs/speech-engine)
