import asyncio
import random
import os
import sys
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
    "JOIN_SINI_GROUP_BEBAS_SHARE_LINK", "ShareLadangcuan",
    "Bebas Share APK Cuan", "SHARE BEBAS WEB CUAN"
]

PULSA_MESSAGE = """gas apk terbaru modal spin bisa dapetin pulsa gratis tanpa modal gasken Mayan pulsa gratis 

note : link kalo ngga bisa di akses pake vpn 

link: https://www.in22.online/?code=9XLF6R
https://www.in22.online/?code=9XLF6R"""

# === AUTO SETTINGS ===
INTERVAL_MINUTES = 5  # Kirim setiap 5 menit (super cepat!)
MIN_DELAY = 1
MAX_DELAY = 3

client = TelegramClient(session, api_id, api_hash)
total_sent = 0

def log(message):
    """Log dengan timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    
    # Save to log file
    with open("bot_service.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

async def send_quick_campaign():
    """Kirim campaign cepat"""
    global total_sent
    
    success_count = 0
    start_time = datetime.now()
    
    log(f"🚀 Starting quick campaign...")
    
    for i, group in enumerate(target_groups, 1):
        try:
            await client.send_message(group, PULSA_MESSAGE)
            success_count += 1
            total_sent += 1
            log(f"📱 Sent to {group} ({i}/{len(target_groups)})")
            
        except FloodWaitError as e:
            log(f"⏳ Flood wait {e.seconds}s for {group}")
            await asyncio.sleep(e.seconds + 10)
            
        except Exception as e:
            log(f"❌ Failed {group}: {str(e)[:30]}")
        
        # Quick delay
        if i < len(target_groups):
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            await asyncio.sleep(delay)
    
    duration = (datetime.now() - start_time).total_seconds()
    success_rate = (success_count / len(target_groups)) * 100
    
    log(f"✅ Campaign done: {success_count}/{len(target_groups)} ({success_rate:.1f}%) in {duration:.1f}s")
    log(f"📊 Total messages sent: {total_sent}")
    
    return success_count

async def service_bot():
    """Bot service yang jalan terus"""
    try:
        me = await client.get_me()
        log(f"🤖 PULSA SERVICE BOT STARTED")
        log(f"👤 Account: {me.first_name} (@{me.username})")
        log(f"⏰ Interval: Every {INTERVAL_MINUTES} minutes")
        log(f"🎯 Targets: {len(target_groups)} groups")
        
    except Exception as e:
        log(f"❌ Login failed: {e}")
        return
    
    # Main service loop
    while True:
        try:
            # Send campaign
            await send_quick_campaign()
            
            # Wait for next campaign
            next_time = datetime.now() + timedelta(minutes=INTERVAL_MINUTES)
            log(f"💤 Next campaign: {next_time.strftime('%H:%M:%S')}")
            log(f"⏳ Waiting {INTERVAL_MINUTES} minutes...")
            
            # Sleep dengan progress
            for i in range(INTERVAL_MINUTES):
                remaining = INTERVAL_MINUTES - i
                if remaining % 5 == 0:  # Log setiap 5 menit
                    log(f"⏳ {remaining} minutes until next campaign...")
                await asyncio.sleep(60)  # Sleep 1 menit
            
        except Exception as e:
            log(f"❌ Service error: {e}")
            log("🔄 Retrying in 5 minutes...")
            await asyncio.sleep(300)

async def main():
    # Clear log file on start
    with open("bot_service.log", "w") as f:
        f.write("")
    
    await client.start()
    await service_bot()

if __name__ == "__main__":
    try:
        log("🤖 PULSA SERVICE BOT STARTING...")
        log("🔄 Auto-send every 30 minutes")
        log("📝 Logs saved to bot_service.log")
        asyncio.run(main())
    except KeyboardInterrupt:
        log("👋 Service stopped by user")
        log(f"📊 Total messages sent: {total_sent}")
    except Exception as e:
        log(f"❌ Fatal error: {e}")
        log(f"📊 Total messages sent: {total_sent}")
        # Auto restart on error
        os.system("python bot_service.py")