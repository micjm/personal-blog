+++
title = "HN Hiring Index v0.1"
slug = "hn-hiring-index-agent-duel"
date = "2026-11-04T00:00:00-08:00"
draft = false
description = "A simple, seasonally adjusted index of the Hacker News job market."
showFooter = true
+++

For a second, let's pretend Hacker News is a self-contained economy. How is the job market?

We can estimate this using comment counts on the monthly Who is Hiring post for employers and Who Wants to be Hired post for would-be employees.

I built a simple version here: [HN Hiring Index v0.1](https://micjm.github.io/hn-hiring-index/).

**Doesn't this exist?**

Yes! [HN Hiring Pulse](https://hn-pulse-ed21c883b05f.herokuapp.com/) and [Santiago Basulto’s analysis](https://github.com/santiagobasulto/hn-who-is-hiring-analysis/blob/main/Analysis.ipynb).

My only contribution is seasonal adjustment, which the other posts do not include. (What can I say, my introduction to coding was an econometrics class.)

**Seasonality**

Who is Hiring comments see typical seasonality you see in economic data. They are 13% lower in January and 14% higher in May.

Who Wants to be Hired comments see somewhat reversed seasonality, with January being 33% higher than November.

Altogether, seasonal adjustments lower deviation from trend a lot (16.1% to 5.4% for hiring and from 15.3% to 11.7% for jobseekers).
