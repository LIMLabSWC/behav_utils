# Golden values

Every number the library produces on one small, frozen dataset, pinned from 0.10.0. `tests/test_golden.py`
recomputes them and fails when one moves, so a refactor that should change nothing is checked against
the numbers themselves, not only against the unit tests.

- `data/` — two animals × three sessions × 400 trials in the on-disk layout the loader reads, with laser,
  abort and no-response trials. Written once by `make_fixture.py` and committed; never regenerated (numpy
  does not promise identical random streams across versions).
- `config.yaml` — the config that loads it; `data_dir` is relative to the config file.
- `outputs.py` — the one computation: all statistics pooled per animal and trial type, per-session
  statistics, the five readouts, a laser-vs-off contrast (bootstrap and permutation, fixed seed) and rolling
  statistics.
- `expected/` — its output, written by `make_golden.py`, with the numpy, scipy and pandas versions used.

Tolerances: closed-form values must agree to 1e-12 everywhere. Values that come out of an optimiser
(psychometric and history fits, PSE dynamics, the fitted readouts) are compared to a relative 1e-6 on the
reference machine: the one the values were pinned on, with the same numpy, scipy and pandas and the same platform
(`versions.json` records them). Anywhere else, macOS against Linux or another library build, an optimiser can
stop at a slightly different point (PSE dynamics on one animal's laser trials moved 0.47% between macOS and
Linux, while two Linux machines agreed to every digit), most of all for a poorly determined parameter such as
`pse_tau`. There, fitted values are compared to a relative 2e-2 with an absolute floor of 1e-3, and bootstrap and
permutation summaries of fitted statistics (CI bounds and p-values in the contrast table) to a relative 5e-2 with
a floor of 2e-2. A failure names the row, the column, the relative difference and whether the value is fitted.

Regenerate only for a change that is meant to move numbers, marked ▲ in the changelog, and only the tables that
change, on the reference machine:

```bash
python tests/golden/make_golden.py --table delta
```

`--table` takes one or more of the table names and rewrites those files alone; the other tables and
`versions.json` stay as they were, so they keep their provenance. Then `git diff --stat tests/golden/expected`
should list only the tables the change was meant to move. Without `--table` every table is rewritten and
`versions.json` records the current versions: a new pin of everything.

Provenance: the 2-AFC values were pinned at 0.10.0. At 1.1.0 the session-unit rows of `delta.csv` (interval
bounds and bootstrap p) were regenerated, when the session bootstrap began to draw the sessions two phases share
once for both; the trial-unit rows and every other table are unchanged from 0.10.0.

## The continuous-response family

`continuous/` holds a second frozen fixture: reproduction sessions (a dot on a 0-100 line and a poke) written
once by `continuous/make_fixture.py` with numpy only. `continuous/expected/` pins the family's statistics (per
animal pooled and per session) and its three readouts. These were pinned at 1.0, when the family arrived, not from
0.10.0, and are all closed-form, so they are compared to 1e-12. `python tests/golden/make_golden.py --family
continuous` rewrites only them; the 2-AFC values and their provenance are untouched.
