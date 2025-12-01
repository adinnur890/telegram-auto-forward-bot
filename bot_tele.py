import asyncio
import random
import os
import re
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === AMBIL DARI ENV FILE ===
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session = os.getenv('SESSION_NAME', 'bot_session')

source_channel = os.getenv('SOURCE_CHANNEL', 'cuanonline2024_2025')
target_groups = [
    "snack_video_group_diskusi",
    "Bebas_Share_2",
    "Bebas_Share_4",
    "SHARELINK06RATU",
    "BEBAS_SHARE_Link_Apk",
    "sharefreebetgratis",
    "apajalah88",
    "ponzymania",
    "Bebas_Share_3",
    "infolokertegalslawibrebes",
    "bebaslinksharee",
    "infofreebetttt",
    "legitinvestmentsites0",
    "salinglikevidiotiktok",
    "Grupbebassharelinkantibanned",
    "Bebas_Sharee01",
    "Bebas_Sharee02",
    "Bebas_Sharee03",
    "LINKALTERNATIF78",
    "JOIN_SINI_GROUP_BEBAS_SHARE_LINK",
    "ShareLadangcuan",
    "Bebas Share APK Cuan",
    "SHARE BEBAS WEB CUAN",
]

MIN_DELAY = 3   # delay minimal aman
MAX_DELAY = 7   # delay maksimal aman
last_message_id = None  # track pesan terakhir
# =====================

client = TelegramClient(session, api_id, api_hash)

async def get_latest_message():
    """Ambil pesan terbaru dari channel"""
    try:
        messages = await client.get_messages(source_channel, limit=1)
        return messages[0] if messages else None
    except Exception as e:
        print(f"❌ Gagal ambil pesan terbaru: {e}")
        return None

def clean_spam_message(text):
    """Bersihkan pesan dari elemen spam"""
    if not text:
        return text
    
    # Ganti kata-kata sensitif dulu
    replacements = {
        'slot': 'game',
        'depo': 'deposit', 
        'freebet': 'bonus',
        'wd': 'withdraw'
    }
    
    for old, new in replacements.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)
    
    # Link penting yang harus dipertahankan
    important_links = ['bitly.cx', 'bit.ly', 'tinyurl.com']
    
    # Hapus link berlebihan tapi pertahankan yang penting
    lines = text.split('\n')
    new_lines = []
    main_link_count = 0
    
    for line in lines:
        # Cek apakah line punya link
        line_links = re.findall(r'https?://[^\s]+', line)
        
        if line_links:
            # Cek apakah ada link penting di line ini
            has_important = any(imp in link for link in line_links for imp in important_links)
            
            if has_important:
                # Selalu pertahankan line dengan link penting
                new_lines.append(line)
            elif main_link_count < 2:  # sisakan 2 link utama
                new_lines.append(line)
                main_link_count += 1
            # skip line dengan link berlebihan
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines).strip()

def is_spam_like(text):
    """Cek apakah pesan berpotensi spam"""
    if not text:
        return False
    
    spam_indicators = [
        text.count('http') > 5,  # banyak link
        len(text.split('\n')) > 20,  # terlalu panjang
        'slot' in text.lower() and 'depo' in text.lower(),  # gambling
    ]
    return any(spam_indicators)

async def forward_to_groups(message):
    """Forward pesan ke semua grup dengan handling yang lebih baik"""
    success_count = 0
    
    # Cek potensi spam
    if is_spam_like(message.text):
        print("⚠️ Pesan berpotensi spam, gunakan delay lebih lama...")
        spam_delay_multiplier = 2
    else:
        spam_delay_multiplier = 1
    
    for i, group in enumerate(target_groups, 1):
        try:
            # Bersihkan pesan kalau spam
            if message.text and is_spam_like(message.text):
                cleaned_text = clean_spam_message(message.text)
                await client.send_message(group, cleaned_text)
                print(f"🧽 Pesan dibersihkan untuk {group}")
            else:
                await client.forward_messages(group, message)
            
            success_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"✅ [{timestamp}] Forward ke {group} ({i}/{len(target_groups)})")
            
        except FloodWaitError as e:
            print(f"⚠️ Flood wait {e.seconds}s untuk {group}, skip...")
            await asyncio.sleep(e.seconds + 5)
            
        except Exception as e:
            print(f"❌ Gagal forward ke {group}: {e}")
        
        # Jeda antar grup dengan variasi natural
        if i < len(target_groups):  # jangan delay di grup terakhir
            base_delay = random.randint(MIN_DELAY, MAX_DELAY)
            # Tambah variasi acak kecil
            extra_delay = random.uniform(0.5, 2.0)
            # Kalau spam, delay lebih lama
            total_delay = (base_delay + extra_delay) * spam_delay_multiplier
            print(f"⏳ Tunggu {total_delay:.1f}s sebelum grup berikutnya...")
            await asyncio.sleep(total_delay)
    
    return success_count

async def monitor_new_messages():
    """Monitor pesan baru dari channel"""
    global last_message_id
    
    try:
        me = await client.get_me()
        print(f"✅ Login berhasil! Akun: {me.first_name} (@{me.username})")
    except SessionPasswordNeededError:
        print("⚠️ Akun 2FA aktif, perlu password!")
        return
    except Exception as e:
        print(f"❌ Gagal login: {e}")
        return
    
    print(f"🔍 Monitoring channel: {source_channel}")
    print(f"📤 Target groups: {len(target_groups)} grup")
    
    while True:
        try:
            latest_message = await get_latest_message()
            
            if not latest_message:
                print("⚠️ Tidak ada pesan di channel")
                await asyncio.sleep(60)
                continue
            
            # Cek apakah ada pesan baru
            if last_message_id is None:
                print(f"📌 Set baseline message ID: {latest_message.id}")
                print("🚀 Bot siap! Forward pesan ID 1077 untuk test...")
                
                # Ambil pesan spesifik ID 1077
                try:
                    target_message = await client.get_messages(source_channel, ids=1077)
                    if target_message:
                        print(f"📝 Pesan 1077 ditemukan: {target_message.text[:100] if target_message.text else 'Media/File'}...")
                        success_count = await forward_to_groups(target_message)
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"✅ [{timestamp}] Test selesai! Berhasil forward ke {success_count}/{len(target_groups)} grup")
                    else:
                        print("⚠️ Pesan ID 1077 tidak ditemukan")
                except Exception as e:
                    print(f"❌ Error ambil pesan 1077: {e}")
                
                print("="*50)
                last_message_id = latest_message.id
                await asyncio.sleep(10)
                continue
            
            if latest_message.id > last_message_id:
                print(f"🆕 Pesan baru ditemukan! ID: {latest_message.id}")
                preview_text = latest_message.text[:100] if latest_message.text else 'Media/File'
                print(f"📝 Preview: {preview_text}...")
                
                # Cek dan bersihkan kalau spam
                if latest_message.text and is_spam_like(latest_message.text):
                    print("⚠️ Pesan terdeteksi spam, akan dibersihkan otomatis")
                
                success_count = await forward_to_groups(latest_message)
                last_message_id = latest_message.id
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"✅ [{timestamp}] Selesai! Berhasil forward ke {success_count}/{len(target_groups)} grup")
                print("="*50)
            else:
                print(f"💤 Belum ada pesan baru (last ID: {last_message_id})")
            
            # Check interval lebih cepat
            await asyncio.sleep(30)  # cek setiap 30 detik
            
        except Exception as e:
            print(f"❌ Error di monitoring: {e}")
            await asyncio.sleep(60)

async def main():
    await client.start()
    await monitor_new_messages()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot dihentikan oleh user")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
