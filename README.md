# news-image-20261122 — THE WORLD TODAY

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/lycann666/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/lycann666/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for the [make.fun bounty "Sum up 22 November's world news in one image"](https://make.fun/bounty/news-image-20261122).

## What it is

`main.py` draws a one-page newspaper front page — **THE WORLD TODAY**,
Sunday 22 November 2026 — entirely procedurally: a hand-written 5x7 bitmap
font, a pure-stdlib PNG encoder, and drawing code for the masthead, a night
skyline over Ukraine, a tanker in the Gulf, a Hong Kong ballot box, a globe,
a cargo ship in the Baltic and the Estonian tricolour.
No images, fonts or data are read from disk and no network is used at
runtime, so the output is byte-identical on every run.

## The news on the page

- **Missiles rain on Ukraine overnight** — 50+ missiles, about 500 drones,
  five killed including a family of four near Lviv; Poland scrambled jets
- **Iran strikes US bases in Bahrain** — Tehran claims missiles and drones
  hit US Patriot radars at al-Riffa and Awali; Bahrain says its defences
  intercepted the attack; reported Sunday
- **Hong Kong votes** — 856 candidates contest 723 Election Committee
  seats; polls 9 AM to 6 PM
- **COP31 talks deadlocked** — UN climate talks stall over fossil fuels
  and finance as the summit nears its end
- **Drones hit a ship in the Baltic** — a Russia-bound cargo ship struck
  in the Gulf of Finland; Finland tightens security
- **Estonia to shut its border with Russia** — Moscow calls the step a
  "new Iron Curtain"
- Also, from Saturday: the EU and Indonesia sign a trade pact scrapping
  tariffs on 98% of goods; Mexico captures FBI most-wanted drug lord
  "Chapo Isidro" in Sinaloa, eleven killed

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — 1024x1024 PNG, under 1 MiB, deterministic
```

Python 3, standard library only.

## License

MIT — see [LICENSE](LICENSE).
