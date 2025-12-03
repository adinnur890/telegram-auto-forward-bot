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
session = 'loop_bot_session'

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

async def send_to_all():
    success = 0
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting blast...")
    
    for i, group in enumerate(target_groups, 1):
        try:
            await client.send_message(group, PEAKAI_MESSAGE)
            success += 1
            print(f"[{datetime.now().strftime('%H:%M:%S')}] OK {group} ({i}/{len(target_groups)})")
            await asyncio.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] FAIL {group}")
            await asyncio.sleep(1)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Blast done! Success: {success}/{len(target_groups)}")
    return success

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Bot started: {me.first_name}")
    print(f"Target groups: {len(target_groups)}")
    
    round_num = 0
    while True:
        try:
            round_num += 1
            print(f"\n=== ROUND {round_num} ===")
            
            await send_to_all()
            
            wait_time = random.randint(120, 300)  # 2-5 menit
            print(f"\nWaiting {wait_time}s for next round...")
            
            # Countdown setiap 30 detik
            for remaining in range(wait_time, 0, -30):
                print(f"Next round in {remaining}s...")
                await asyncio.sleep(30)
            
        except KeyboardInterrupt:
            print(f"\nStopped at round {round_num}")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying in 60s...")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print("LOOP BLAST BOT")
    print("Kirim terus setiap 2-5 menit")
    print("="*30)
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error: {e}")
        input("Press Enter to exit...")