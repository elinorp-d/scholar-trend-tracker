# Historic word occurrence in academic papers

## Summary

This script extracts the historic word occurrence of a search term in
academic papers (from Google Scholar). It allows for spotting trends
in research and analyzing the relevance of a topic over time.

## Usage

`python extract_occurrences.py '<keyword>' <start date> <end date>`

This command lists the number of publications for every year using
this keyword. The script just searches for articles and excludes
patents and citations.

### Alternative: Usage with Docker

You can use [Docker](https://www.docker.com/) to run this script, without the need of having Python or its dependencies installed.

1. Update the `command` with your search term and time range in `docker-compose.yml`
2. run `docker-compose up`

## Example

- Search term: 'bitcoin'
- Desired time span: 2000 to 2015
- Command: `python extract_occurrences.py 'bitcoin' 2000 2015`
- Output: `out.csv`, with the following contents:

| year | results |
|------|---------|
| ...  | ...     |
| 2011 | 141     |
| 2012 | 292     |
| 2013 | 889     |
| 2014 | 2370    |
| 2015 | 2580    |

![bitcoin chart](https://raw.githubusercontent.com/Pold87/academic-keyword-occurrence/master/bitcoin_chart.png "bitcoin chart")

## Credits

Created by Volker Strobel - volker.strobel87@gmail.com

If you use this code in academic papers, please cite this repository via Zenodo (http://doi.org/10.5281/zenodo.1218409):

Volker Strobel. (2018, April 14). Pold87/academic-keyword-occurrence: First release (Version v1.0.0). Zenodo. http://doi.org/10.5281/zenodo.1218409

---

## Extensions (this fork)

Two additional scripts for multi-term search and visualization, built on top of `extract_occurrences.py`.

### Installation

```bash
pip install -r requirements.txt
```

### `multi_term_search.py` — search across multiple terms

Runs multiple queries year-by-year and writes a single CSV with one column per term.
Uses `as_sdt=1,5` (Engineering/CS/Mathematics, excludes patents). Stops immediately
if rate-limited rather than silently recording incorrect counts.

```bash
python multi_term_search.py \
    --terms '"pluralistic alignment"' '"pluralistic AI"' '"overton pluralism"' \
    --start 2021 --end 2026 \
    --out data/results_by_term.csv
```

| flag | default | description |
|------|---------|-------------|
| `--terms` | required | Search terms; wrap phrases in inner quotes |
| `--start` | required | Start year (inclusive) |
| `--end` | required | End year (inclusive) |
| `--delay` | `3.0` | Seconds between requests; increase if rate-limited |
| `--out` | `data/results_by_term.csv` | Output CSV path |

### `plot_trends.py` — stacked area chart

Reads the CSV produced by `multi_term_search.py` and produces a stacked area chart.

```bash
python plot_trends.py data/results_by_term.csv \
    --partial-year 2026 \
    --title "Pluralistic Alignment Research — Google Scholar Counts" \
    --out figures/scholar_trends.png
```

| flag | default | description |
|------|---------|-------------|
| `csv` | required | Path to results CSV |
| `--partial-year` | None | Marks this year with `*` and adds a partial-year footnote |
| `--title` | `"Google Scholar Counts by Search Term"` | Plot title |
| `--out` | `figures/scholar_trends.png` | Output image path |

### Included dataset

`data/pluralistic_alignment_2021_2026.csv` contains counts for six pluralistic
alignment search terms (2021–2026), collected June 2026. The corresponding figure
is at `figures/pluralistic_alignment_2021_2026.png`.

### Rate limiting

Google Scholar blocks repeated requests from the same IP. Practical limits:
- ~30–40 requests per session before hitting a block
- Blocks typically clear within a few hours
- Switching VPN exit node clears blocks immediately
- Do not reduce `--delay` below `2.0`
