import re
prohibited_words = [
    # English
    "fool", "idiot", "bitch", "bastard", "asshole", "douchebag", "cunt", "motherfucker",
    # Spanish
    "pendejo", "cabrón", "puta", "jodido", "maricón", "mierda", "coño", "malparido",
    # French
    "con", "salope", "enculé", "merde", "connard", "enculé", "putain", "connasse",
    # German
    "idiot", "arschloch", "schlampe", "scheiße", "verdammte", "wichser", "hurensohn",
    # Italian
    "idiota", "stronzo", "troia", "merda", "bastardo", "coglione", "cazzo", "puttana",
    # Portuguese
    "idiota", "cabrão", "puta", "filho da puta", "merda", "caralho", "desgraçado",
    # Russian
    "идиот", "урод", "жопа", "пизда", "сука", "ебать", "хуй", "блядь",
    # Chinese (Mandarin)
    "笨蛋", "傻瓜", "混蛋", "操你妈", "傻逼", "贱人", "王八蛋", "狗屎",
    # Arabic
    "أحمق", "عاهرة", "ابن القحبة", "يا حمار", "اللعنة", "النذل", "الجحيم",
    # Japanese
    "馬鹿", "バカ", "クソ", "くそ", "死ね", "くそったれ", "くそがき", "糞",
    # Korean
    "바보", "시발", "미친", "병신", "씨발", "좆까", "개새끼", "병신",
    # Hindi
    "बकवास", "बेवकूफ", "चूतिया", "मादरचोद", "भोसड़ीके", "लौड़ा", "गंद", "कुत्ता"
    # Swahili
    "mjinga", "kiburi", "mshenzi", "fala", "tupu", "mbwa", "ndege", "ng'ombe"
    # Turkish
    "aptal", "sığır", "amına koyayım", "orospu çocuğu", "göt", "piç", "sikik", "siktir"
    # Dutch
    "idioot", "klootzak", "slet", "kanker", "tering", "hoer", "kut", "lul"
    # Greek
    "βλάκας", "μαλάκας", "γαμώτο", "κωλοτούμπα", "μαλάκα", "γαμώ", "κωλοτούμπες", "κώλος"
    # Thai
    "โง่", "เหี้ย", "ควย", "ชาติหมา", "มึง", "เฮี้ยน", "เนี่ย", "สัส"
    # Vietnamese
    "đồ ngu", "điên", "địt mẹ", "đồ chó", "đụ má", "con cặc", "mẹ mày", "chó"
    # Filipino
    "tanga", "gago", "putang ina", "ulol", "hindot", "buwisit", "yawa", "hayop"
    # Malay
    "bodoh", "bangang", "pukimak", "lancau", "anjing", "cibai", "balik kampung", "gila"
    # Indonesian
    "bodoh", "tolol", "anjing", "bangsat", "kontol", "jembut", "asu", "babi"
    # Urdu
    "بیوقوف", "حمار", "کون"]


 

def detect(arr):
    prohibited_patterns = [r"\+234", "080", "090"]


    word_patterns = [re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE) for word in prohibited_words]

   
    arr = [re.sub(r'f00l', 'fool', message, flags=re.IGNORECASE) for message in arr]

    for message in arr:
        #print(message)
        for pattern in word_patterns:
            #print(pattern)
            if pattern.search(message):
                return False   

        # Check for prohibited patterns
        for pattern in prohibited_patterns:
            if re.search(pattern, message):
                return False   

    return True

# Example usage
arr = ['hello', 'world', 'checking',  'f00l']
checking = detect(arr)
print(checking)   
