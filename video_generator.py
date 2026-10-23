
import math
import random
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

W, H = 360, 640
FPS = 20
DURATION = 12
FRAMES = FPS * DURATION
OUT = Path("output")
OUT.mkdir(exist_ok=True)

VIDEO = OUT / "kinetic_sand_asmr.mp4"
AUDIO = OUT / "asmr_sound.wav"

COLORS = [
    (255, 100, 150),
    (255, 170, 80),
    (255, 220, 100),
    (100, 220, 180),
    (100, 160, 255),
    (190, 120, 255),
]

def make_audio():
    rate = 44100
    count = rate * DURATION
    audio = np.zeros(count, dtype=np.float32)
    rng = np.random.default_rng(42)

    for _ in range(100):
        start = int(rng.integers(0, count - 5000))
        length = int(rng.integers(500, 5000))
        end = min(start + length, count)
        noise = rng.normal(0, 1, end - start)
        envelope = np.linspace(1, 0, end - start)
        audio[start:end] += noise * envelope * 0.035

    audio = audio / max(np.max(np.abs(audio)), 0.001) * 0.65
    pcm = (audio * 32767).astype(np.int16)

    with wave.open(str(AUDIO), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(pcm.tobytes())

def make_frame(i):
    img = Image.new("RGB", (W, H), (23, 26, 43))
    d = ImageDraw.Draw(img)

    for y in range(H):
        c = (23 + y // 40, 26 + y // 50, 43 + y // 35)
        d.line((0, y, W, y), fill=c)

    d.rounded_rectangle(
        (22, 130, W - 22, 500),
        radius=25,
        fill=(52, 55, 75),
        outline=(130, 135, 165),
        width=3,
    )

    color = COLORS[(i // 40) % len(COLORS)]
    top, bottom = 240, 455

    d.rectangle((40, top, W - 40, bottom), fill=color)

    progress = (i % 80) / 80
    cut_x = int(50 + progress * (W - 100))

    d.polygon(
        [
            (cut_x - 12, top),
            (cut_x + 12, top),
            (cut_x + 22, bottom),
            (cut_x - 2, bottom),
        ],
        fill=(38, 40, 58),
    )

    rng = random.Random(i)
    for _ in range(120):
        x = rng.randint(42, W - 42)
        y = rng.randint(top, bottom)
        r = rng.choice([1, 2])
        lighter = tuple(min(255, v + rng.randint(5, 35)) for v in color)
        d.ellipse((x, y, x + r, y + r), fill=lighter)

    tool_x = int(65 + (i / FRAMES) * 230)
    d.rounded_rectangle(
        (tool_x - 6, 155, tool_x + 6, 270),
        radius=5,
        fill=(225, 225, 235),
    )

    d.text(
        (W // 2, 555),
        "KINETIC SAND ASMR",
        fill=(245, 245, 255),
        anchor="mm",
    )

    return img

def make_video():
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}",
        "-r", str(FPS),
        "-i", "-",
        "-an",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(VIDEO),
    ]

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        for i in range(FRAMES):
            proc.stdin.write(make_frame(i).tobytes())
    finally:
        proc.stdin.close()

    error = proc.stderr.read().decode(errors="replace")
    code = proc.wait()

    if code:
        raise RuntimeError("FFmpeg video xatosi: " + error[-3000:])

def add_audio():
    temp = OUT / "video_silent.mp4"
    VIDEO.replace(temp)

    try:
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(temp),
                "-i", str(AUDIO),
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                "-movflags", "+faststart",
                str(VIDEO),
            ],
            check=True,
        )
    finally:
        temp.unlink(missing_ok=True)

if __name__ == "__main__":
    print("ASMR ovozi yaratilmoqda...")
    make_audio()
    print("Vertikal video yaratilmoqda...")
    make_video()
    print("Ovoz birlashtirilmoqda...")
    add_audio()
    print(f"Video tayyor: {VIDEO}")
