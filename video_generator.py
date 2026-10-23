
name: Shorts Bot

on:
  workflow_dispatch:
  schedule:
    - cron: '30 1 * * *'
    - cron: '0 10 * * *'

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Kodni yuklash
        uses: actions/checkout@v4

      - name: Python sozlash
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: FFmpeg o'rnatish
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg

      - name: Kutubxonalarni o'rnatish
        run: pip install -r requirements.txt

      - name: Trendlarni topish
        run: python trend_scanner.py

      - name: Ssenariylarni yaratish
        run: python script_generator.py

      - name: ASMR video yaratish
        run: python video_generator.py

      - name: Natijalarni saqlash
        uses: actions/upload-artifact@v4
        with:
          name: shorts-asmr-videos
          path: output/
          if-no-files-found: error
          retention-days: 7
