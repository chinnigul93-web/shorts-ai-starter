
import json
import os

INPUT = "output/trends.json"
OUTPUT = "output/scripts.md"

KEYWORDS = [
    "ronaldo", "al-nassr", "futbol", "football",
    "superliga", "paxtakor", "neftchi", "messi",
    "mourinho"
]

def score(topic):
    title = topic.get("topic", "").lower()
    traffic = topic.get("traffic", topic.get("approx_traffic", ""))
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

def main():
    if not os.path.exists(INPUT):
        raise FileNotFoundError(
            "Trend fayli topilmadi: " + INPUT
        )

    with open(INPUT, encoding="utf-8") as f:
        data = json.load(f)

    topics = sorted(
        data.get("topics", []),
        key=score,
        reverse=True
    )[:2]

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("# YouTube Shorts ssenariylari\n\n")

        for i, item in enumerate(topics, 1):
            title = item.get("topic", "Noma'lum mavzu")

            f.write(f"## Video {i}: {title}\n\n")
            f.write("**Boshlanish:** Bugungi qiziqarli mavzu!\n\n")
            f.write(
                f"**Asosiy qism:** {title} mavzusi trendlar "
                "ro'yxatida paydo bo'ldi. "
                "Video tayyorlashdan oldin faktlarni ishonchli "
                "manbadan tekshiring.\n\n"
            )
            f.write(
                "**Yakun:** Siz bu haqda nima deb o'ylaysiz? "
                "Izohlarda yozing!\n\n"
            )
            f.write("#Shorts #Trend #Uzbekistan\n\n---\n\n")

    print(f"{len(topics)} ta ssenariy qoralamasi yaratildi.")

if __name__ == "__main__":
    main()
