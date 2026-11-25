+++
title = "Code golf rankings across all four languages with human records"
slug = "code-golf-human-records"
date = "2026-11-25T00:00:00-06:00"
draft = false
showFooter = true
summary = "32 problems in JavaScript, Python, C++ and Haskell. Gemini 4 Neon ranks second and the 2015 human records rank eighth."
+++

**Four-language weights** · JavaScript 25%, Python 25%, C++ 25%, Haskell 25%. Each language has 32 problems with 2015 human records. Each of the 128 entries has equal weight for every competitor.

**Three-language comparison** · JavaScript, Python and C++ each receive one third of the weight. The original benchmark uses these 96 entries for its human comparison because fewer people competed in Haskell.

**Scoring** · Each entry earns 100% × (best known bytes ÷ submitted bytes)². An unsolved entry earns zero. Both rankings use the average of the entry scores. The human row combines the shortest recorded human submission for each entry.

{{< code-golf-table >}}
| Rank (4 langs) | Competitor | Score (4 langs) | Rank (3 langs) | Score (3 langs) |
| ---: | :--- | ---: | ---: | ---: |
| 1 | GPT-6.2 Astra (max) | 92.69% | 1 | 92.26% |
| 2 | **Gemini 4 Neon (xhigh)** | 87.37% | 4 | 86.55% |
| 3 | Claude Fable 5.2 (xhigh) | 87.32% | 3 | 86.63% |
| 4 | Gemini 4 Carbon (high) | 86.36% | 6 | 85.12% |
| 5 | GPT-6.2 Sol (max) | 86.28% | 5 | 86.21% |
| 6 | Gemini 4 Argon (high) | 84.89% | 7 | 84.83% |
| 7 | Claude Opus 5.5 (xhigh) | 84.42% | 8 | 83.52% |
| 8 | **2015 human records** | 83.50% | 2 | 87.53% |
| 9 | GPT-6 Astra (max) | 79.35% | 9 | 79.47% |
| 10 | GPT-6.1 Terra (max) | 79.08% | 10 | 78.54% |
| 11 | Claude Sonnet 5.5 (xhigh) | 77.73% | 11 | 77.25% |
| 12 | GPT-6.1 Sol (max) | 76.23% | 12 | 75.53% |
| 13 | Gemini 4 Hydrogen (xhigh) | 75.60% | 13 | 74.29% |
| 14 | Claude Opus 5 (xhigh) | 73.18% | 14 | 72.31% |
| 15 | GPT-5.6 Sol (max) | 71.81% | 15 | 71.58% |
| 16 | GPT-5.5 (xhigh) | 71.11% | 16 | 71.34% |
| 17 | GPT-5.6 Terra (max) | 67.09% | 17 | 67.06% |
| 18 | Gemini 3.8 Flash (high) | 65.79% | 18 | 65.93% |
| 19 | Claude Haiku 5.5 (max) | 64.91% | 19 | 63.99% |
| 20 | GPT-6 Sol (max) | 62.18% | 20 | 63.17% |
| 21 | Claude Haiku 5.5 (xhigh) | 59.17% | 21 | 58.65% |
| 22 | GPT-5.6 Luna (max) | 57.52% | 22 | 57.87% |
| 23 | GPT-6 Luna (max) | 52.45% | 23 | 52.91% |
{{< /code-golf-table >}}

[Source byte counts (November 25 snapshot)](https://github.com/bjin/go-codegolf-benchmark/blob/e962571532c03f4ef4d64d9f371e0770216f7975/data.json) · [Original leaderboard](https://bjin.github.io/go-codegolf-benchmark/#leaderboard) · [Author’s rationale for the three-language comparison](https://bjin.github.io/go-codegolf-benchmark/#about/overall-and-js-py-c)
