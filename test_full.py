import re

def clean_spam_message(text):
    """Bersihkan pesan dari elemen spam"""
    if not text:
        return text
    
    # Ganti kata-kata sensitif dulu
    replacements = {
        'slot': 'game',
        'depo': 'deposit', 
        'freebet': 'bonus',
        'wd': 'withdraw'
    }
    
    for old, new in replacements.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)
    
    # Link penting yang harus dipertahankan
    important_links = ['bitly.cx', 'bit.ly', 'tinyurl.com']
    
    # Hapus link berlebihan tapi pertahankan yang penting
    lines = text.split('\n')
    new_lines = []
    main_link_count = 0
    
    for line in lines:
        # Cek apakah line punya link
        line_links = re.findall(r'https?://[^\s]+', line)
        
        if line_links:
            # Cek apakah ada link penting di line ini
            has_important = any(imp in link for link in line_links for imp in important_links)
            
            if has_important:
                # Selalu pertahankan line dengan link penting
                new_lines.append(line)
            elif main_link_count < 2:  # sisakan 2 link utama
                new_lines.append(line)
                main_link_count += 1
            # skip line dengan link berlebihan
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines).strip()

# Test dengan pesan lengkap
sample = """gasken yuk apk slot terbaru nih ,gasken dicoba sebelum rame baru rilis juga 🥱

Note :
🌟Min depo 10k jadi 25
🌟Min wd 12k
🌟freebet 79k nih gas
🌟Daftar pake nomer tlpn doang sayang 😘💕

Link :
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1

➡ INFO CUAN GRATIS ATAU CHECK PENARIKAN!!
https://bitly.cx/wyZzq"""

print("=== ORIGINAL ===")
print(sample)
print("\n=== CLEANED ===")
print(clean_spam_message(sample))
print("\n=== HASIL ===")
print("✅ Link bitly.cx TETAP ADA (penting)")
print("✅ Link rojupj dikurangi jadi 2")
print("✅ Kata sensitif diganti")