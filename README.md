# The World in One Day — Wednesday 25 November 2026

make.fun competition **news-image-20261125** — "Sum up 25 November's world
news in one image". Prize pool $100 (50 places, 1st $20). Entry free.
Deadline: Friday 27 November 2026, 00:00 UTC (07:00 WIB).

## The image

A one-page front page, drawn entirely in code with PIL (no photographs, no
copied artwork):

- Masthead with the date **WEDNESDAY 25 NOVEMBER 2026** prominent.
- Hero: **Ukraine hits Russia's ships on two seas** — Zelenskiy confirms
  drone strikes on the cargo ship Sparta II in the Gulf of Finland and a
  Russian warship off Benghazi, Libya. Drawn scene: the burning cargo ship
  at dusk.
- **40 stories across 7 regions** (Europe, Middle East, Asia–Pacific,
  Africa, North America, Latin America, Science · Tech · Sport), each with
  its source.
- A UTC timeline strip of first reports, and a date-check line.

## Files

- `entry.png` — the submitted image (1024×1024, ≤ 1 MiB).
- `main.py` — stdlib-only entrypoint: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), deterministically.
- `compose.py` — the PIL script that drew the image (plus `stories.py`,
  the verified story list).
- `ladder/` — the 18 candidate images of the G1 ladder; see `LADDER.md`.
- `SOURCES.md` — every story with its source and first-report date evidence.
- `LADDER.md` — how the winning candidate was chosen.

## Honest count

Built at ~01:30 UTC on 25 November 2026, so only the overnight /
early-morning wire was verifiable then: events first reported late on
24 Nov UTC (already 25 Nov in Asia–Pacific time zones) plus events of
25 Nov itself. A second sweep before the 27 Nov deadline is needed to add
the day's later stories. See SOURCES.md.

## License

MIT — see `LICENSE`.
