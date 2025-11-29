import asyncio
import random
import os
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
]

MIN_DELAY = 30   # jeda lebih lama biar aman dari flood
MAX_DELAY = 60
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

async def forward_to_groups(message):
    """Forward pesan ke semua grup dengan handling yang lebih baik"""
    success_count = 0
    
    for i, group in enumerate(target_groups, 1):
        try:
            await client.forward_messages(group, message)
            success_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"✅ [{timestamp}] Forward ke {group} ({i}/{len(target_groups)})")
            
        except FloodWaitError as e:
            print(f"⚠️ Flood wait {e.seconds}s untuk {group}, skip...")
            await asyncio.sleep(e.seconds + 5)
            
        except Exception as e:
            print(f"❌ Gagal forward ke {group}: {e}")
        
        # Jeda antar grup
        if i < len(target_groups):  # jangan delay di grup terakhir
            delay = random.randint(MIN_DELAY, MAX_DELAY)
            print(f"⏳ Tunggu {delay}s sebelum grup berikutnya...")
            await asyncio.sleep(delay)
    
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
                last_message_id = latest_message.id
                print(f"📌 Set baseline message ID: {last_message_id}")
                await asyncio.sleep(30)
                continue
            
            if latest_message.id > last_message_id:
                print(f"🆕 Pesan baru ditemukan! ID: {latest_message.id}")
                print(f"📝 Preview: {latest_message.text[:100] if latest_message.text else 'Media/File'}...")
                
                success_count = await forward_to_groups(latest_message)
                last_message_id = latest_message.id
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"✅ [{timestamp}] Selesai! Berhasil forward ke {success_count}/{len(target_groups)} grup")
                print("="*50)
            else:
                print(f"💤 Belum ada pesan baru (last ID: {last_message_id})")
            
            # Check interval lebih lama
            await asyncio.sleep(120)  # cek setiap 2 menit
            
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
