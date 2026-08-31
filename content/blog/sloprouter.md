+++
title = "SlopRouter, or How to Lie with Benchmarks"
slug = "sloprouter"
date = "2026-08-31T00:00:00-07:00"
draft = false
+++

**Learning about benchmark saturation - the hard way**

It’s 2026, so I built an LLM product that aimed to improve performance. I had a problem, though: how to show that I was actually making an improvement? A benchmark, of course! Unfortunately, no matter how hard I tried, I could not get the benchmark I chose to move. I eventually gave up.

I kept my eye on the leaderboard, though, and noticed strange things start to happen. First, a tiny open weight model nearly matched the frontier for pennies per question. Weird, but maybe AI was advancing that fast. Next, Fable scored worse than Opus.

Finally, it hit me: the benchmark was saturated! Nobody could do better than ~94% because the remaining 6% of questions were funky!

**The inspiration behind SlopRouter**

Armed with my new understanding, I prowled Hacker News looking for launches to ruin. Just kidding, but barely!

The thing that kept launching was LLM routers that showed a cost savings with no drop in quality. Sure enough, every one was run on a saturated benchmark. Of course these routers saved cost without a loss of quality, because the underlying models all performed roughly the same!

**Introducing SlopRouter**

I noticed this pattern enough times that I thought that there wasn’t enough understanding of how saturated benchmarks behave. To illustrate this point more clearly, and as a joke, I built SlopRouter, which randomly chooses models and low and behold beats the benchmark!

[work in progress]
