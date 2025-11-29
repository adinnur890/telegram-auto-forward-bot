# 🤖 Telegram Auto Forward Bot

Bot Telegram otomatis untuk forward pesan dari channel ke multiple grup dengan fitur keamanan dan monitoring yang lebih baik.

## ✨ Fitur

- 🔒 **Secure**: Credentials disimpan di environment variables
- 🤖 **Smart Monitoring**: Hanya forward pesan baru, tidak spam
- ⏰ **Anti-Flood**: Delay 30-60 detik antar grup
- 📊 **Real-time Logging**: Progress dan timestamp
- 🛡️ **Error Handling**: Handle FloodWaitError dan error lainnya
- 💾 **Memory Efficient**: Track message ID untuk efisiensi

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment
Buat file `.env` di root folder:
```env
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=bot_session
SOURCE_CHANNEL=your_source_channel
```

### 4. Jalankan Bot
```bash
python bot_tele.py
```

## ⚙️ Konfigurasi

### Target Groups
Edit list `target_groups` di `bot_tele.py`:
```python
target_groups = [
    "group1",
    "group2",
    # tambah grup lainnya...
]
```

### Delay Settings
```python
MIN_DELAY = 30   # minimum delay (detik)
MAX_DELAY = 60   # maximum delay (detik)
```

## 📋 Requirements

- Python 3.7+
- Telethon
- python-dotenv

## 🔐 Keamanan

- ✅ Credentials di `.env` file (tidak di-commit ke git)
- ✅ Anti-flood protection
- ✅ Error handling yang proper
- ✅ Session management yang aman

## 📝 Log Output

```
✅ Login berhasil! Akun: Your Name (@username)
🔍 Monitoring channel: your_channel
📤 Target groups: 21 grup
🆕 Pesan baru ditemukan! ID: 1234
📝 Preview: Ini adalah preview pesan...
✅ [14:30:15] Forward ke group1 (1/21)
⏳ Tunggu 45s sebelum grup berikutnya...
✅ [14:31:00] Selesai! Berhasil forward ke 21/21 grup
```

## ⚠️ Disclaimer

Bot ini untuk keperluan edukasi. Pastikan mematuhi Terms of Service Telegram dan tidak melakukan spam.

## 🤝 Contributing

1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## 📄 License

MIT License - lihat file LICENSE untuk detail.