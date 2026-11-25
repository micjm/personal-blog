+++
title = "Which models beat humans at the code golf benchmark"
slug = "code-golf-human-records"
date = "2026-11-25T00:00:00-06:00"
draft = false
showFooter = true
summary = "Seven models beat the 2015 human records when all 32 problems get equal weight and every language with a human solution counts."
+++

On November 22, a [post hit Hacker News](https://news.ycombinator.com/item?id=50601280) that claimed GPT-6.2 Astra was the first model to beat humans on a benchmark called code golf. A quick glance at the table showed that the weights were broken. Haskell got zero weight in the human comparison even though humans had solved all 32 problems in it. Gemini 4 Neon, at least, looked like it should also be beating humans.

I recalculated the table below, giving each problem equal weight and only including problem and language combinations that humans had solved.

{{< code-golf-table >}}
| Rank | Competitor | Score |
| ---: | :--- | ---: |
| 1 | GPT-6.2 Astra (max) | 92.69% |
| 2 | **Gemini 4 Neon (xhigh)** | 87.37% |
| 3 | Claude Fable 5.2 (xhigh) | 87.32% |
| 4 | Gemini 4 Carbon (high) | 86.36% |
| 5 | GPT-6.2 Sol (max) | 86.28% |
| 6 | Gemini 4 Argon (high) | 84.89% |
| 7 | Claude Opus 5.5 (xhigh) | 84.42% |
| 8 | **2015 human records** | 83.50% |
| 9 | GPT-6 Astra (max) | 79.35% |
| 10 | GPT-6.1 Terra (max) | 79.08% |
| 11 | Claude Sonnet 5.5 (xhigh) | 77.73% |
| 12 | GPT-6.1 Sol (max) | 76.23% |
| 13 | Gemini 4 Hydrogen (xhigh) | 75.60% |
| 14 | Claude Opus 5 (xhigh) | 73.18% |
| 15 | GPT-5.6 Sol (max) | 71.81% |
| 16 | GPT-5.5 (xhigh) | 71.11% |
| 17 | GPT-5.6 Terra (max) | 67.09% |
| 18 | Gemini 3.8 Flash (high) | 65.79% |
| 19 | Claude Haiku 5.5 (max) | 64.91% |
| 20 | GPT-6 Sol (max) | 62.18% |
| 21 | Claude Haiku 5.5 (xhigh) | 59.17% |
| 22 | GPT-5.6 Luna (max) | 57.52% |
| 23 | GPT-6 Luna (max) | 52.45% |
{{< /code-golf-table >}}

## Scoring

Each of the 32 problems counts for 1/32 of the final score. For each problem, I averaged the scores in the languages where humans had a solution. For all 32, those were JavaScript, Python, C++ and Haskell.

I kept the benchmark’s scoring formula. A solution earns 100% × (best known byte count ÷ submitted byte count)². Matching the shortest known solution earns 100%, using twice as many bytes earns 25%, and an unsolved entry earns zero. The human row uses the shortest recorded human solution for each problem and language.

[Source byte counts (November 25 snapshot)](https://github.com/bjin/go-codegolf-benchmark/blob/e962571532c03f4ef4d64d9f371e0770216f7975/data.json) · [Original leaderboard](https://bjin.github.io/go-codegolf-benchmark/#leaderboard) · [Author’s rationale for the three-language comparison](https://bjin.github.io/go-codegolf-benchmark/#about/overall-and-js-py-c)
