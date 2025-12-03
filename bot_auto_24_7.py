import asyncio
import random
import os
import time
import signal
import sys
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from dotenv import load_dotenv

load_dotenv()

# Config
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session = 'auto_24_7_session'

target_groups = [
    "snack_video_group_diskusi", "SHARELINK06RATU", "BEBAS_SHARE_Link_Apk", 
    "sharefreebetgratis", "apajalah88", "ponzymania", "infolokertegalslawibrebes",
    "bebaslinksharee", "infofreebetttt", "legitinvestmentsites0",
    "salinglikevidiotiktok", "Grupbebassharelinkantibanned", "Bebas_Sharee01",
    "Bebas_Sharee02", "Bebas_Sharee03", "LINKALTERNATIF78",
    "JOIN_SINI_GROUP_BEBAS_SHARE_LINK", "ShareLadangcuan", "Bebas Share APK Cuan"
]

PEAKAI_MESSAGE = """gajian terus tiap minggu dari peakAi bang
login pake akun Tiikktttoookkkk
tugas upload Vidio asal doang
lumayan gajian seminggu sekali😁

link daftar:
https://takeapeak.ai/invite/XqUFPmUKmMdWqgajU3PAeaVUN2Bw250a

contoh link tt jangan lupa like:
https://www.tiktok.com/@din_dev12/video/7579449861855071509?is_from_webapp=1&sender_device=pc&web_id=7522430435851945490"""

client = TelegramClient(session, api_id, api_hash)

# Global stats
total_campaigns = 0
total_sent = 0
start_time = None
running = True

def signal_handler(signum, frame):
    """Handle system signals gracefully"""
    global running
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Received signal {signum}, graceful shutdown...")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def log_with_time(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    
    # Also save to log file
    with open("auto_24_7.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

async def send_blast():
    """Send blast to all groups"""
    global total_campaigns, total_sent
    
    total_campaigns += 1
    success_count = 0
    
    log_with_time(f"🚀 AUTO CAMPAIGN #{total_campaigns} STARTED")
    
    for i, group in enumerate(target_groups, 1):
        if not running:  # Check if we should stop
            log_with_time("⏹️ Stopping campaign due to shutdown signal")
            break
            
        try:
            await client.send_message(group, PEAKAI_MESSAGE)
            success_count += 1
            total_sent += 1
            log_with_time(f"✅ Sent to {group} ({i}/{len(target_groups)})")
            
        except FloodWaitError as e:
            log_with_time(f"⏳ Flood wait {e.seconds}s for {group}")
            await asyncio.sleep(e.seconds + random.randint(5, 15))
            
        except Exception as e:
            log_with_time(f"❌ Failed {group}: {str(e)[:50]}")
        
        # Quick delay between groups
        await asyncio.sleep(random.uniform(1.0, 2.5))
    
    success_rate = (success_count / len(target_groups)) * 100
    log_with_time(f"📊 Campaign #{total_campaigns} done: {success_count}/{len(target_groups)} ({success_rate:.1f}%)")
    log_with_time(f"📈 Total messages sent: {total_sent}")
    
    return success_count

async def auto_countdown(seconds, message="Next campaign"):
    """Silent countdown without user interaction"""
    end_time = time.time() + seconds
    
    while time.time() < end_time and running:
        remaining = int(end_time - time.time())
        
        # Log every 60 seconds
        if remaining % 60 == 0 and remaining > 0:
            mins = remaining // 60
            log_with_time(f"⏳ {message} in {mins} minutes...")
        
        await asyncio.sleep(10)  # Check every 10 seconds
    
    if running:
        log_with_time(f"🔥 {message} starting now!")

async def auto_24_7_bot():
    """Main 24/7 auto bot loop"""
    global start_time, running
    
    try:
        log_with_time("🔐 Starting authentication...")
        await client.start()
        me = await client.get_me()
        
        log_with_time("🤖 AUTO 24/7 PULSA BOT ACTIVATED")
        log_with_time(f"👤 Account: {me.first_name} (@{me.username})")
        log_with_time(f"🎯 Target groups: {len(target_groups)}")
        log_with_time(f"📱 Message: PeakAI gajian promo")
        log_with_time("🔄 Running in AUTO mode - no manual intervention needed")
        
        start_time = datetime.now()
        
        # Main infinite loop
        while running:
            try:
                # Send blast campaign
                await send_blast()
                
                if not running:
                    break
                
                # Auto wait between campaigns (3-7 minutes)
                wait_time = random.randint(180, 420)
                log_with_time(f"💤 Auto-waiting {wait_time//60} minutes for next campaign...")
                
                await auto_countdown(wait_time, "Next auto campaign")
                
            except Exception as e:
                log_with_time(f"❌ Campaign error: {e}")
                log_with_time("🔄 Auto-recovery in 2 minutes...")
                await auto_countdown(120, "Recovery")
        
        log_with_time("⏹️ Auto bot stopped gracefully")
        
    except Exception as e:
        log_with_time(f"❌ Fatal error: {e}")
        log_with_time("🔄 Attempting restart in 5 minutes...")
        await asyncio.sleep(300)
        # Restart the bot
        await auto_24_7_bot()

async def main():
    """Main entry point"""
    # Clear log file on start
    with open("auto_24_7.log", "w") as f:
        f.write("")
    
    log_with_time("🚀 AUTO 24/7 PULSA BOT INITIALIZING...")
    log_with_time("🔄 This bot runs automatically without user intervention")
    log_with_time("📝 All activities logged to auto_24_7.log")
    
    try:
        await auto_24_7_bot()
    except Exception as e:
        log_with_time(f"❌ Main loop error: {e}")
    finally:
        if start_time:
            uptime = datetime.now() - start_time
            hours = int(uptime.total_seconds() // 3600)
            minutes = int((uptime.total_seconds() % 3600) // 60)
            
            log_with_time("📊 FINAL STATISTICS")
            log_with_time(f"⏰ Total uptime: {hours}h {minutes}m")
            log_with_time(f"🚀 Total campaigns: {total_campaigns}")
            log_with_time(f"📱 Total messages sent: {total_sent}")
            log_with_time("👋 Auto bot shutdown complete")

if __name__ == "__main__":
    try:
        # Disable KeyboardInterrupt handling for true auto mode
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal system error: {e}")
        with open("auto_24_7.log", "a") as f:
            f.write(f"[{datetime.now()}] FATAL: {e}\n")