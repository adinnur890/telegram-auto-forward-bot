import asyncio
import random
import os
import time
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from dotenv import load_dotenv

load_dotenv()

# Config
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session = 'pro_bot_session'

target_groups = [
    "snack_video_group_diskusi", "SHARELINK06RATU", "BEBAS_SHARE_Link_Apk", 
    "sharefreebetgratis", "apajalah88", "ponzymania", "infolokertegalslawibrebes",
    "bebaslinksharee", "infofreebetttt", "legitinvestmentsites0",
    "salinglikevidiotiktok", "Grupbebassharelinkantibanned", "Bebas_Sharee01",
    "Bebas_Sharee02", "Bebas_Sharee03", "LINKALTERNATIF78",
    "JOIN_SINI_GROUP_BEBAS_SHARE_LINK", "ShareLadangcuan", "Bebas Share APK Cuan"
]

PULSA_MESSAGE = """gas apk terbaru modal spin bisa dapetin pulsa gratis tanpa modal gasken Mayan pulsa gratis 

note : link kalo ngga bisa di akses pake vpn 

link: https://www.in22.online/?code=9XLF6R
https://www.in22.online/?code=9XLF6R"""

client = TelegramClient(session, api_id, api_hash)

# Stats
total_sent = 0
total_failed = 0
start_time = None
campaign_count = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("    PULSA GRATIS BLAST BOT PRO v2.0")
    print("    Advanced Auto-Sender with Real-Time Stats")
    print("=" * 60)

def print_stats():
    global total_sent, total_failed, start_time, campaign_count
    
    if start_time:
        uptime = datetime.now() - start_time
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        
        success_rate = (total_sent / (total_sent + total_failed) * 100) if (total_sent + total_failed) > 0 else 0
        
        print(f"\n📊 LIVE STATISTICS")
        print(f"┌─────────────────────────────────────────────────────┐")
        print(f"│ Campaigns Completed: {campaign_count:>4}                        │")
        print(f"│ Messages Sent:       {total_sent:>4}                        │")
        print(f"│ Failed Attempts:     {total_failed:>4}                        │")
        print(f"│ Success Rate:        {success_rate:>5.1f}%                      │")
        print(f"│ Uptime:              {hours:>2}h {minutes:>2}m                     │")
        print(f"│ Target Groups:       {len(target_groups):>4}                        │")
        print(f"└─────────────────────────────────────────────────────┘")

def progress_bar(current, total, width=40):
    progress = int(width * current / total)
    bar = "█" * progress + "░" * (width - progress)
    percentage = (current / total) * 100
    return f"[{bar}] {percentage:5.1f}% ({current}/{total})"

async def blast_campaign():
    global total_sent, total_failed, campaign_count
    
    campaign_count += 1
    success_count = 0
    failed_count = 0
    
    clear_screen()
    print_header()
    print(f"\n🚀 CAMPAIGN #{campaign_count} INITIATED")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target: {len(target_groups)} groups")
    print("\n" + "─" * 60)
    
    start_blast = time.time()
    
    for i, group in enumerate(target_groups, 1):
        # Update progress
        print(f"\r🔄 {progress_bar(i-1, len(target_groups))} Processing...", end="", flush=True)
        
        try:
            await client.send_message(group, PULSA_MESSAGE)
            success_count += 1
            total_sent += 1
            status = "✅"
            
        except FloodWaitError as e:
            print(f"\n⏳ Flood protection: {e.seconds}s delay for {group}")
            await asyncio.sleep(e.seconds + random.randint(5, 15))
            failed_count += 1
            total_failed += 1
            status = "⏳"
            
        except Exception as e:
            failed_count += 1
            total_failed += 1
            status = "❌"
        
        # Smart delay
        delay = random.uniform(1.5, 3.0)
        await asyncio.sleep(delay)
    
    # Final progress
    print(f"\r🔄 {progress_bar(len(target_groups), len(target_groups))} Complete!   ")
    
    blast_duration = time.time() - start_blast
    success_rate = (success_count / len(target_groups)) * 100
    speed = len(target_groups) / blast_duration * 60
    
    print("\n" + "─" * 60)
    print(f"📈 CAMPAIGN #{campaign_count} RESULTS")
    print(f"┌─────────────────────────────────────────────────────┐")
    print(f"│ ✅ Successful:       {success_count:>4} / {len(target_groups):<4} ({success_rate:5.1f}%)        │")
    print(f"│ ❌ Failed:           {failed_count:>4}                        │")
    print(f"│ ⏱️  Duration:         {blast_duration:>5.1f}s                     │")
    print(f"│ 🚀 Speed:            {speed:>5.1f} groups/min             │")
    print(f"└─────────────────────────────────────────────────────┘")
    
    print_stats()
    
    return success_count

async def countdown_timer(seconds, message="Next campaign"):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer = f"{mins:02d}:{secs:02d}"
        
        # Animated countdown
        spinner = "|/-\\"[remaining % 4]
        print(f"\r{spinner} {message} in {timer} | Press Ctrl+C to stop", end="", flush=True)
        await asyncio.sleep(1)
    
    print(f"\r✨ {message} starting now!" + " " * 30)

async def main():
    global start_time
    
    clear_screen()
    print_header()
    print("\n🔐 Authenticating...")
    
    try:
        await client.start()
        me = await client.get_me()
        
        clear_screen()
        print_header()
        print(f"\n✅ Authentication successful!")
        print(f"👤 Account: {me.first_name} (@{me.username})")
        print(f"🎯 Ready to blast {len(target_groups)} groups")
        print(f"📱 Message: Pulsa gratis promo")
        
        start_time = datetime.now()
        
        await asyncio.sleep(3)
        
        while True:
            try:
                await blast_campaign()
                
                # Smart wait time based on success rate
                base_wait = random.randint(180, 300)  # 3-5 minutes
                
                print(f"\n💤 Preparing next campaign...")
                await countdown_timer(base_wait, "Next blast")
                
            except KeyboardInterrupt:
                clear_screen()
                print_header()
                print(f"\n👋 Bot stopped by user")
                print_stats()
                print(f"\n🎉 Thank you for using Pulsa Blast Bot Pro!")
                break
                
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("🔄 Auto-recovery in 60 seconds...")
                await countdown_timer(60, "Recovery")
    
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        input("Press Enter to exit...")