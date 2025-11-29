import re

def clean_spam_message(text):
    """Bersihkan pesan dari elemen spam"""
    if not text:
        return text
    
    # Hapus link berlebihan (sisakan 3)
    links = re.findall(r'https?://[^\s]+', text)
    if len(links) > 3:
        # Sisakan 3 link pertama, hapus sisanya
        for i, link in enumerate(links):
            if i >= 3:  # hapus link ke-4 dan seterusnya
                text = text.replace(link, "")
        
        # Bersihkan baris kosong berlebihan
        text = re.sub(r'\n\s*\n', '\n', text)
        text = text.strip()
    
    # Ganti kata-kata sensitif
    replacements = {
        'slot': 'game',
        'depo': 'deposit', 
        'freebet': 'bonus',
        'wd': 'withdraw'
    }
    
    for old, new in replacements.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)
    
    return text

# Test dengan pesan kamu
sample = """gasken yuk apk slot terbaru nih ,gasken dicoba sebelum rame baru rilis juga

Note :
Min depo 10k jadi 25
Min wd 12k
freebet 79k nih gas
Daftar pake nomer tlpn doang sayang

Link :
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1
https://rojupj.com/indexd1.html?invite_code=VDS4CXHM1"""

print("=== ORIGINAL ===")
print(sample)
print("\n=== CLEANED ===")
print(clean_spam_message(sample))
print("\n=== HASIL ===")
print("- Link dikurangi dari 5 jadi 3")
print("- 'slot' jadi 'game'")
print("- 'depo' jadi 'deposit'") 
print("- 'freebet' jadi 'bonus'")
print("- 'wd' jadi 'withdraw'")