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
    "JOIN_SINI_GROUP_BEBAS_SHARE_LINK", "ShareLadangcuan",
    "Bebas Share APK Cuan", "SHARE BEBAS WEB CUAN"
]

PULSA_MESSAGE = """gas apk terbaru modal spin bisa dapetin pulsa gratis tanpa modal gasken Mayan pulsa gratis 

note : link kalo ngga bisa di akses pake vpn 

link: https://www.in22.online/?code=9XLF6R
https://www.in22.online/?code=9XLF6R"""

client = TelegramClient(session, api_id, api_hash)
round_count = 0

async def instant_blast():
    """Kirim instant ke semua grup tanpa delay panjang"""
    global round_count
    round_count += 1
    
    success_count = 0
    start_time = datetime.now()
    
    print(f"\n🚀 INSTANT BLAST #{round_count}")
    print(f"🕐 {start_time.strftime('%H:%M:%S')}")
    print("="*50)
    
    for i, group in enumerate(target_groups, 1):
        try:
            await client.send_message(group, PULSA_MESSAGE)
            success_count += 1
            print(f"📱 [{datetime.now().strftime('%H:%M:%S')}] ✅ {group} ({i}/{len(target_groups)})")
            
        except FloodWaitError as e:
            print(f"⏳ Flood {e.seconds}s: {group}")
            await asyncio.sleep(e.seconds + 5)
            
        except Exception as e:
            print(f"❌ Failed: {group}")
        
        # Super quick delay
        await asyncio.sleep(random.uniform(0.5, 1.5))
    
    duration = (datetime.now() - start_time).total_seconds()
    success_rate = (success_count / len(target_groups)) * 100
    
    print(f"\n📊 BLAST #{round_count} DONE!")
    print(f"✅ Success: {success_count}/{len(target_groups)} ({success_rate:.1f}%)")
    print(f"⏱️ Time: {duration:.1f}s")
    print("="*50)
    
    return success_count

async def continuous_blast():
    """Blast terus menerus tanpa henti"""
    try:
        me = await client.get_me()
        print(f"🔥 INSTANT CONTINUOUS BLAST BOT")
        print(f"👤 Account: {me.first_name} (@{me.username})")
        print(f"🎯 Targets: {len(target_groups)} groups")
        print(f"⚡ Mode: CONTINUOUS BLAST")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    while True:
        try:
            # Blast langsung
            await instant_blast()
            
            # Delay singkat sebelum blast berikutnya
            wait_time = random.randint(60, 120)  # 1-2 menit
            print(f"\n💤 Next blast in {wait_time}s...")
            
            # Countdown
            for remaining in range(wait_time, 0, -10):
                print(f"⏳ Next blast in {remaining}s...")
                await asyncio.sleep(10)
            
        except KeyboardInterrupt:
            print(f"\n👋 Stopped! Total blasts: {round_count}")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Retrying in 30s...")
            await asyncio.sleep(30)

async def main():
    await client.start()
    await continuous_blast()

if __name__ == "__main__":
    try:
        print("🔥 INSTANT CONTINUOUS BLAST BOT")
        print("⚡ Kirim terus menerus setiap 1-2 menit")
        print("🚀 No waiting, pure speed!")
        print("="*50)
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n👋 Total blasts completed: {round_count}")
    except Exception as e:
        print(f"❌ Error: {e}")