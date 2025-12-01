import asyncio
import random
import os
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session = 'pulsa_blast_2024'  # session unik

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
blast_count = 0

async def fast_blast():
    global blast_count
    blast_count += 1
    
    success_count = 0
    start_time = datetime.now()
    
    print(f"\n=== FAST BLAST #{blast_count} ===")
    print(f"Time: {start_time.strftime('%H:%M:%S')}")
    
    for i, group in enumerate(target_groups, 1):
        try:
            await client.send_message(group, PULSA_MESSAGE)
            success_count += 1
            print(f"[{datetime.now().strftime('%H:%M:%S')}] OK {group} ({i}/{len(target_groups)})")
            
        except FloodWaitError as e:
            print(f"FLOOD {e.seconds}s: {group}")
            await asyncio.sleep(e.seconds + 5)
            
        except Exception as e:
            print(f"FAIL: {group}")
        
        await asyncio.sleep(random.uniform(0.5, 1.0))
    
    duration = (datetime.now() - start_time).total_seconds()
    success_rate = (success_count / len(target_groups)) * 100
    
    print(f"\nBLAST #{blast_count} DONE!")
    print(f"Success: {success_count}/{len(target_groups)} ({success_rate:.1f}%)")
    print(f"Time: {duration:.1f}s")
    print("="*40)
    
    return success_count

async def continuous_fast():
    try:
        me = await client.get_me()
        print(f"FAST BLAST BOT STARTED")
        print(f"Account: {me.first_name} (@{me.username})")
        print(f"Targets: {len(target_groups)} groups")
        print(f"Mode: CONTINUOUS FAST BLAST")
        print("="*40)
        
    except Exception as e:
        print(f"Login failed: {e}")
        return
    
    while True:
        try:
            await fast_blast()
            
            wait_time = random.randint(90, 180)  # 1.5-3 menit
            print(f"\nNext blast in {wait_time}s...")
            
            for remaining in range(wait_time, 0, -15):
                print(f"Next in {remaining}s...")
                await asyncio.sleep(15)
            
        except KeyboardInterrupt:
            print(f"\nStopped! Total blasts: {blast_count}")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying in 30s...")
            await asyncio.sleep(30)

async def main():
    await client.start()
    await continuous_fast()

if __name__ == "__main__":
    try:
        print("FAST BLAST BOT")
        print("Kirim terus setiap 1.5-3 menit")
        print("="*40)
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\nTotal blasts: {blast_count}")
    except Exception as e:
        print(f"Error: {e}")