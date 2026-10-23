
import json
import os
from pathlib import Path

INPUT = Path("output/trends.json")
OUTPUT = Path("output/scripts.md")

KEYWORDS = [
    "ronaldo",
    "al-nassr",
    "futbol",
    "football",
    "superliga",
    "paxtakor",
    "neftchi",
    "messi",
    "mourinho",
]

def score(topic):
    title = str(topic.get("topic", "")).lower()
    traffic = str(
        topic.get("traffic", topic.get("approx_traffic", ""))
    )

    points = sum(
        10 for word in KEYWORDS if word in title
    )

    if "5000+" in traffic:
        points += 5
    elif "2000+" in traffic:
        points += 4
    elif "500+" in traffic:
        points += 3
    elif "200+" in traffic:
        points += 2

    return points


def create_script(title, number):
    return (
        f"## Video {number}: {title}\n\n"
        f"**Sarlavha:** {title} 😱🔥\n\n"
        "**Boshlanish (0–3 soniya):** "
        "Bu mavzuda sizni hayratda qoldiradigan narsa bor!\n\n"
        f"**Asosiy qism:** {title} mavzusi trendlar "
        "ro‘yxatida paydo bo‘ldi. "
        "Video tayyorlashdan oldin ma’lumotlarni "
        "ishonchli manbadan tekshiring.\n\n"
        "**Yakun:** Siz nima deb o‘ylaysiz? "
        "Izohlarda yozing!\n\n"
        "**Hashtaglar:** #Shorts #Trend #Uzbekistan\n\n"
        "---\n\n"
    )


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    if not INPUT.exists():
        raise FileNotFoundError(
            f"Trend fayli topilmadi: {INPUT}. "
            "Avval trend_scanner.py muvaffaqiyatli ishlashi kerak."
        )

    with INPUT.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict):
        topics = data.get("topics", [])
    elif isinstance(data, list):
        topics = data
    else:
        raise ValueError(
            "trends.json ichidagi ma'lumot formati noto‘g‘ri."
        )

    if not isinstance(topics, list):
        raise ValueError(
            "'topics' ro‘yxat shaklida bo‘lishi kerak."
        )

    valid_topics = [
        item for item in topics
        if isinstance(item, dict) and item.get("topic")
    ]

    selected_topics = sorted(
        valid_topics,
        key=score,
        reverse=True
    )[:2]

    with OUTPUT.open("w", encoding="utf-8") as file:
        file.write("# YouTube Shorts ssenariylari\n\n")

        if not selected_topics:
            file.write(
                "Hozircha ssenariy uchun mavzu topilmadi.\n"
            )
        else:
            for number, item in enumerate(
                selected_topics, start=1
            ):
                title = str(item["topic"])
                file.write(create_script(title, number))

    print(
        f"{len(selected_topics)} ta ssenariy qoralamasi "
        f"saqlandi: {OUTPUT}"
    )


if __name__ == "__main__":
    main()
