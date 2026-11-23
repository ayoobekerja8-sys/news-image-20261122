# The World in One Day — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/ayoobekerja8-sys/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/ayoobekerja8-sys/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-image newspaper front page summing up Sunday 22 November 2026 — 36 stories (13 illustrated features + 23 briefs), a world map with 13 numbered pins, a UTC timeline, a red-bordered date-check box and the day in six numbers. Region tabs total exactly 36: Asia 14, Europe 9, North America 7, Africa 2, South America 2, Oceania 2. Every feature carries a source and a CONFIRMED / REPORTED badge, and nothing is drawn below 9px. Built for the make.fun bounty https://make.fun/bounty/news-image-20261122

## How to run

`python3 draw.py` regenerates `entry.png` (deterministic: no clock, no randomness, no network, fixed DejaVu system fonts — two runs give byte-identical output). `main.ts` is the entrypoint: run `node main.ts` and it validates `entry.png` (PNG/JPEG, ≤ 1 MiB, ≤ 1024px per side) and copies it to `$MAKEFUN_OUTPUT_DIR` (default `/output`).
