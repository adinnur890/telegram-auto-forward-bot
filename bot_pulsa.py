import asyncio
import random
import os
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session = os.getenv('SESSION_NAME', 'bot_session')

target_groups = [
    "snack_video_group_diskusi", "Bebas_Share_2", "Bebas_Share_4",
    "SHARELINK06RATU", "BEBAS_SHARE_Link_Apk", "sharefreebetgratis",
    "apajalah88", "ponzymania", "Bebas_Share_3", "infolokertegalslawibrebes",
    "bebaslinksharee", "infofreebetttt", "legitinvestmentsites0",
    "salinglikevidiotiktok", "Grupbebassharelinkantibanned", "Bebas_Sharee01",
    "Bebas_Sharee02", "Bebas_Sharee03", "LINKALTERNATIF78",
    "JOIN_SINI_GROUP_BEBAS_SHARE_LINK", "ShareLadangcuan"
]

# Pesan pulsa gratis kamu
PULSA_MESSAGE = """gas apk terbaru modal spin bisa dapetin pulsa gratis tanpa modal gasken Mayan pulsa gratis 

note : link kalo ngga bisa di akses pake vpn 

link: https://www.in22.online/?code=9XLF6R
https://www.in22.online/?code=9XLF6R"""

client = TelegramClient(session, api_id, api_hash)

async def send_pulsa_promo():
    """Kirim promo pulsa gratis ke semua grup"""
    try:
        me = await client.get_me()
        print(f"🎯 PULSA GRATIS BOT ACTIVATED")
        print(f"👤 Account: {me.first_name} (@{me.username})")
        print(f"📱 Message: Pulsa gratis promo")
        print(f"🎯 Targets: {len(target_groups)} groups")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    success_count = 0
    start_time = datetime.now()
    
    for i, group in enumerate(target_groups, 1):
        try:
            await client.send_message(group, PULSA_MESSAGE)
            success_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"📱 [{timestamp}] Pulsa promo sent → {group} ({i}/{len(target_groups)})")
            
        except FloodWaitError as e:
            print(f"⏳ Flood wait {e.seconds}s for {group}, skipping...")
            await asyncio.sleep(e.seconds + 5)
            
        except Exception as e:
            print(f"❌ Failed: {group} - {str(e)[:30]}...")
        
        # Delay antar grup
        if i < len(target_groups):
            delay = random.uniform(3, 7)
            print(f"⏳ Delay: {delay:.1f}s...")
            await asyncio.sleep(delay)
    
    # Stats
    duration = (datetime.now() - start_time).total_seconds()
    success_rate = (success_count / len(target_groups)) * 100
    
    print(f"\n📊 PULSA PROMO REPORT")
    print(f"✅ Success: {success_count}/{len(target_groups)} ({success_rate:.1f}%)")
    print(f"⏱️ Duration: {duration:.1f}s")
    print(f"📱 Pulsa promo delivered!")
    print("="*50)

async def main():
    await client.start()
    await send_pulsa_promo()

if __name__ == "__main__":
    try:
        print("📱 PULSA GRATIS AUTO-SENDER")
        print("🎯 Kirim promo pulsa ke semua grup")
        print("="*50)
        asyncio.run(main())
        print("\n✅ Pulsa promo campaign completed!")
    except KeyboardInterrupt:
        print("\n👋 Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")