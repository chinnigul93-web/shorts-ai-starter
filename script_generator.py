
import json
import os
import random

INPUT = "output/trends.json"
OUTPUT = "output/scripts.md"

# Futbolga oid mavzularga ustunlik beramiz.
KEYWORDS = [
    "ronaldo", "al-nassr", "al-nasr", "football",
    "futbol", "superliga", "paxtakor", "neftchi",
    "messi", "mourinho", "champion"
]

def score(topic):
    title = topic.get("topic", "").lower()
    traffic = topic.get("approx_traffic", "")
    points = sum(word in title for word in KEYWORDS) * 10

    if "5000+" in traffic:
        points += 5
    elif "2000+" in traffic:
        points += 4
    elif "500+" in traffic:
        points += 3
    elif "200+" in traffic:
        points += 2

    return points

def make_script(topic):
    title = topic["topic"]
    hooks = [
        f"Futbol olamidagi bu mavzuni ko‘rdingizmi? {title}!",
        f"Bugungi trenddagi mavzulardan biri — {title}!",
        f"Bu mavzu futbol muxlislarining e’tiborini tortmoqda: {title}!"
    ]

    return f"""# {title}

## Video sarlavhasi
{title}: muxlislar bilishi kerak bo‘lgan mavzu!

## Ssenariy (qoralama)
{random.choice(hooks)}

Bu mavzu hozir qidiruv trendlarida ko‘rinmoqda.
Video tayyorlashdan oldin voqea tafsilotlarini
ishonchli manbalardan tekshiring.

Eng qiziqarli tasdiqlangan ma’lumotni ko‘rsating
va tomoshabinlardan o‘z fikrini izohlarda yozishni so‘rang.

## Ekrandagi matn
{title}

## Tavsiya etilgan hashtaglar
#Shorts #Futbol #Trend #Uzbekistan

## Muhim
Bu avtomatik yaratilgan qoralama.
Tasdiqlanmagan natija, hisob yoki yangilikni fakt sifatida bermang.
"""

def main():
    if not os.path.exists(INPUT):
        raise FileNotFoundError(
            f"{INPUT} topilmadi. Avval trend_scanner.py ni ishga tushiring."
        )

    with open(INPUT, encoding="utf-8") as f:
        data = json.load(f)

    topics = data.get("topics", [])
    selected = sorted(topics, key=score, reverse=True)[:2]

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("# YouTube Shorts — ssenariy qoralamalari\n\n")
        for i, topic in enumerate(selected, 1):
            f.write(f"## Video {i}\n\n")
            f.write(make_script(topic))
            f.write("\n\n---\n\n")

    print(f"{len(selected)} ta ssenariy qoralamasi yozildi: {OUTPUT}")

if __name__ == "__main__":
    main()
