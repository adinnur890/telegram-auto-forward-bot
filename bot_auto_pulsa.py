import asyncio
import random
import os
from datetime import datetime, timedelta
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

# === SETTINGS OTOMATIS ===
INTERVAL_HOURS = 6  # Kirim setiap 6 jam
MIN_DELAY = 2
MAX_DELAY = 5

client = TelegramClient(session, api_id, api_hash)
campaign_count = 0

async def send_pulsa_campaign():
    """Kirim campaign pulsa gratis"""
    global campaign_count
    campaign_count += 1
    
    success_count = 0
    start_time = datetime.now()
    
    print(f"\n🚀 CAMPAIGN #{campaign_count} STARTED")
    print(f"🕐 Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Targets: {len(target_groups)} groups")
    print("="*60)
    
    for i, group in enumerate(target_groups, 1):
        try:
            await client.send_message(group, PULSA_MESSAGE)
            success_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"📱 [{timestamp}] Campaign #{campaign_count} → {group} ({i}/{len(target_groups)})")
            
        except FloodWaitError as e:
            print(f"⏳ Flood wait {e.seconds}s for {group}")
            await asyncio.sleep(e.seconds + random.randint(5, 15))
            
        except Exception as e:
            print(f"❌ Failed: {group} - {str(e)[:40]}...")
        
        # Smart delay
        if i < len(target_groups):
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"⚡ Delay: {delay:.1f}s...")
            await asyncio.sleep(delay)
    
    # Campaign stats
    duration = (datetime.now() - start_time).total_seconds()
    success_rate = (success_count / len(target_groups)) * 100
    
    print(f"\n📊 CAMPAIGN #{campaign_count} REPORT")
    print(f"✅ Success: {success_count}/{len(target_groups)} ({success_rate:.1f}%)")
    print(f"⏱️ Duration: {duration:.1f}s")
    print(f"🚀 Speed: {len(target_groups)/duration*60:.1f} groups/min")
    print("="*60)
    
    return success_count

async def auto_pulsa_bot():
    """Bot otomatis kirim pulsa 24/7"""
    try:
        me = await client.get_me()
        print(f"🤖 AUTO PULSA BOT 24/7 ACTIVATED")
        print(f"👤 Account: {me.first_name} (@{me.username})")
        print(f"📱 Message: Pulsa gratis promo")
        print(f"⏰ Interval: Every {INTERVAL_HOURS} hours")
        print(f"🎯 Targets: {len(target_groups)} groups")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    # Kirim campaign pertama langsung
    await send_pulsa_campaign()
    
    # Loop otomatis
    while True:
        try:
            # Hitung waktu next campaign
            next_time = datetime.now() + timedelta(hours=INTERVAL_HOURS)
            print(f"\n💤 WAITING FOR NEXT CAMPAIGN...")
            print(f"⏰ Next campaign: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⏳ Waiting {INTERVAL_HOURS} hours...")
            
            # Wait dengan countdown
            total_seconds = INTERVAL_HOURS * 3600
            for remaining in range(total_seconds, 0, -300):  # Update setiap 5 menit
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                print(f"⏳ [{datetime.now().strftime('%H:%M:%S')}] Next campaign in {hours}h {minutes}m...")
                await asyncio.sleep(300)  # Sleep 5 menit
            
            # Kirim campaign berikutnya
            await send_pulsa_campaign()
            
        except Exception as e:
            print(f"❌ Error in auto loop: {e}")
            print("🔄 Retrying in 10 minutes...")
            await asyncio.sleep(600)

async def main():
    await client.start()
    await auto_pulsa_bot()

if __name__ == "__main__":
    try:
        print("🤖 AUTO PULSA GRATIS BOT 24/7")
        print("🔄 Kirim otomatis setiap 6 jam tanpa henti")
        print("⚡ Press Ctrl+C to stop")
        print("="*60)
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n👋 Auto bot stopped by user")
        print(f"📊 Total campaigns sent: {campaign_count}")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print(f"📊 Total campaigns sent: {campaign_count}")