# country-features.csv

One row per country with at least 30 visits (China excluded) that has every feature: 50 countries.
Built 2026-11-25/26 from the files below; `visit_ratio` = share of visits ÷ share of world population.

| Column | Source |
|---|---|
| visits, visit_ratio | GoatCounter, micjm.com, 2026-11-18 to 2026-11-25 (goatcounter-locations.csv); World Bank population 2024 |
| population, gdp_per_capita | World Bank SP.POP.TOTL and NY.GDP.PCAP.CD, 2024 |
| papers_per_million | Scientific and technical journal articles per million people, latest year since 2000. NSF Science and Engineering Indicators via World Bank, processed by Our World in Data (`scientific-publications-per-million`) |
| yc_companies | Y Combinator company directory, all batches and statuses, by first listed location (yc-companies-by-country.csv) |
| beer_litres | Litres of pure alcohol from beer per person aged 15+ per year. WHO Global Health Observatory via Our World in Data (`beer-consumption-per-person`) |
| total_alcohol_litres | Litres of pure alcohol per person aged 15+ per year. WHO via Our World in Data |
| english_pct | Wikipedia, "List of countries by English-speaking population", fetched 2026-11-25 (wikipedia-english-speakers.json) |
| social_media_min_per_day | GWI Q3 2023 (ages 16–64), via DataReportal Digital 2024; gaps filled from PISA 2022 student social-media time, calibrated to GWI with a linear fit |
| nordvpn_servers | Online servers per country from api.nordvpn.com/v1/servers, fetched 2026-11-26 |
| mullvad_servers | Active relays per country from api.mullvad.net/www/relays/all/, fetched 2026-11-26 |
| vpn_downloads_per_100 | Cybernews: VPN app downloads (top 50 apps, App Store + Google Play) per 100 people, 2024 |
| freelancers_vs_world | Oxford Online Labour Index worker sample (Freelancer.com, Guru, PeoplePerHour), Sep 2023–Aug 2024: share of profiles ÷ share of world population |
| hdi, broadband_per_100, working_hours, happiness, median_age, obesity_pct | Our World in Data (`human-development-index`, `broadband-penetration-by-country`, `annual-working-hours-per-worker`, `happiness-cantril-ladder`, `median-age`, `adult-obesity`), latest year since 2000 |
