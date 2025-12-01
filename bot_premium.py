import asyncio
import random
import os
import re
import json
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === CONFIG ===
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session = os.getenv('SESSION_NAME', 'bot_session')
source_channel = os.getenv('SOURCE_CHANNEL', 'cuanonline2024_2025')

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

# === ADVANCED SETTINGS ===
MIN_DELAY = 2
MAX_DELAY = 5
SPAM_DELAY_MULTIPLIER = 3
CHECK_INTERVAL = 20
STATS_FILE = "bot_stats.json"

client = TelegramClient(session, api_id, api_hash)
stats = {"total_sent": 0, "success_rate": 0, "last_run": None}

def load_stats():
    global stats
    try:
        with open(STATS_FILE, 'r') as f:
            stats = json.load(f)
    except:
        pass

def save_stats():
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def smart_clean_message(text):
    """AI-powered message cleaning"""
    if not text:
        return text
    
    # Preserve important links
    important_domains = ['bitly.cx', 'bit.ly', 'tinyurl.com', 't.me']
    
    # Smart word replacement
    replacements = {
        r'\bslot\b': 'game', r'\bdepo\b': 'deposit', 
        r'\bfreebet\b': 'bonus', r'\bwd\b': 'withdraw',
        r'\bbet\b': 'main', r'\bjudi\b': 'game'
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Smart link management
    lines = text.split('\n')
    new_lines = []
    link_count = 0
    max_links = 3
    
    for line in lines:
        line_links = re.findall(r'https?://[^\s]+', line)
        
        if line_links:
            has_important = any(domain in link for link in line_links for domain in important_domains)
            
            if has_important or link_count < max_links:
                new_lines.append(line)
                if not has_important:
                    link_count += 1
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines).strip()

def is_high_risk_spam(text):
    """Advanced spam detection"""
    if not text:
        return False
    
    risk_factors = [
        len(re.findall(r'https?://', text)) > 8,  # too many links
        len(text.split('\n')) > 25,  # too long
        text.count('🌟') > 5,  # too many stars
        len(re.findall(r'[A-Z]{3,}', text)) > 3,  # too much caps
    ]
    
    return sum(risk_factors) >= 2

async def smart_forward(message):
    """Intelligent forwarding with adaptive delays"""
    success_count = 0
    failed_groups = []
    
    is_spam = is_high_risk_spam(message.text)
    delay_multiplier = SPAM_DELAY_MULTIPLIER if is_spam else 1
    
    if is_spam:
        print("🤖 AI detected high-risk content, using enhanced protection...")
    
    start_time = datetime.now()
    
    for i, group in enumerate(target_groups, 1):
        try:
            # Smart message processing
            if message.text and is_spam:
                cleaned_text = smart_clean_message(message.text)
                await client.send_message(group, cleaned_text)
                print(f"🧠 [{datetime.now().strftime('%H:%M:%S')}] AI-cleaned → {group} ({i}/{len(target_groups)})")
            else:
                await client.forward_messages(group, message)
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Direct forward → {group} ({i}/{len(target_groups)})")
            
            success_count += 1
            
        except FloodWaitError as e:
            print(f"⏳ Flood protection: waiting {e.seconds}s for {group}")
            await asyncio.sleep(e.seconds + random.randint(5, 15))
            failed_groups.append(group)
            
        except Exception as e:
            print(f"❌ Failed: {group} - {str(e)[:50]}...")
            failed_groups.append(group)
        
        # Adaptive delay
        if i < len(target_groups):
            base_delay = random.uniform(MIN_DELAY, MAX_DELAY)
            smart_delay = base_delay * delay_multiplier * random.uniform(0.8, 1.2)
            
            print(f"⚡ Smart delay: {smart_delay:.1f}s...")
            await asyncio.sleep(smart_delay)
    
    # Performance stats
    duration = (datetime.now() - start_time).total_seconds()
    success_rate = (success_count / len(target_groups)) * 100
    
    print(f"\n📊 PERFORMANCE REPORT")
    print(f"✅ Success: {success_count}/{len(target_groups)} ({success_rate:.1f}%)")
    print(f"⏱️ Duration: {duration:.1f}s")
    print(f"🚀 Speed: {len(target_groups)/duration*60:.1f} groups/min")
    
    if failed_groups:
        print(f"⚠️ Failed groups: {', '.join(failed_groups[:3])}{'...' if len(failed_groups) > 3 else ''}")
    
    # Update global stats
    stats["total_sent"] += success_count
    stats["success_rate"] = success_rate
    stats["last_run"] = datetime.now().isoformat()
    save_stats()
    
    return success_count

async def premium_monitor():
    """Premium monitoring with real-time events"""
    try:
        me = await client.get_me()
        print(f"🚀 PREMIUM BOT ACTIVATED")
        print(f"👤 Account: {me.first_name} (@{me.username})")
        print(f"📡 Monitoring: {source_channel}")
        print(f"🎯 Targets: {len(target_groups)} groups")
        print(f"📈 Total sent: {stats.get('total_sent', 0)} messages")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    last_message_id = None
    
    while True:
        try:
            # Get latest message
            messages = await client.get_messages(source_channel, limit=1)
            if not messages:
                await asyncio.sleep(CHECK_INTERVAL)
                continue
                
            latest = messages[0]
            
            if last_message_id is None:
                last_message_id = latest.id
                print(f"🎯 Baseline set: Message ID {last_message_id}")
                
                # Premium feature: Forward latest message on startup
                print("🚀 PREMIUM: Auto-forwarding latest message...")
                await smart_forward(latest)
                print("="*60)
                continue
            
            # Check for new messages
            if latest.id > last_message_id:
                print(f"\n🆕 NEW MESSAGE DETECTED!")
                print(f"📝 ID: {latest.id}")
                print(f"📄 Preview: {(latest.text or 'Media')[:80]}...")
                print(f"🕐 Time: {latest.date}")
                
                await smart_forward(latest)
                last_message_id = latest.id
                print("="*60)
            else:
                # Smart status update
                now = datetime.now()
                print(f"💤 [{now.strftime('%H:%M:%S')}] Monitoring... (Last: {last_message_id})")
            
            await asyncio.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            await asyncio.sleep(30)

async def main():
    load_stats()
    await client.start()
    await premium_monitor()

if __name__ == "__main__":
    try:
        print("🤖 TELEGRAM PREMIUM AUTO-FORWARDER v2.0")
        print("🔥 Enhanced AI • Smart Delays • Real-time Stats")
        print("="*60)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Premium bot stopped by user")
        save_stats()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        save_stats()