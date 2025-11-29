import re

def clean_spam_message(text):
    """Bersihkan pesan dari elemen spam"""
    if not text:
        return text
    
    # Hapus link berlebihan (sisakan 2-3)
    links = re.findall(r'https?://[^\s]+', text)
    if len(links) > 3:
        # Ganti link berlebihan dengan placeholder
        for i, link in enumerate(links[3:], 3):
            text = text.replace(link, f"[Link-{i+1}]")
    
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

# Test
if __name__ == "__main__":
    sample = """gasken yuk apk slot terbaru nih ,gasken dicoba sebelum rame baru rilis juga 🥱

Note :
🌟Min depo 10k jadi 25
🌟Min wd 12k
🌟freebet 79k nih gas"""
    
    print("Original:")
    print(sample)
    print("\nCleaned:")
    print(clean_spam_message(sample))