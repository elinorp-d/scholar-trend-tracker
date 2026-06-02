"""Multi-term Google Scholar trend tracker.

Runs multiple exact-phrase search queries year-by-year and writes results to CSV.
Builds on extract_occurrences.py (Strobel & Hofmann, 2018).

Usage:
    python multi_term_search.py \\
        --terms '"pluralistic alignment"' '"pluralistic AI"' '"overton pluralism"' \\
        --start 2021 --end 2026 \\
        --out data/results_by_term.csv

Notes:
    - Uses as_sdt=1,5: restricts to Engineering/CS/Mathematics, excludes patents.
    - Stops immediately on rate limiting rather than recording wrong counts.
    - Default delay is 3s between requests; increase if hitting blocks.
"""

import argparse
import csv
import sys
import time

from extract_occurrences import get_num_results


def safe_get(term, year):
    """Wraps get_num_results with a try/except for network errors."""
    try:
        count, success = get_num_results(term, year, year)
        return (int(count) if success else None), success
    except Exception:
        return None, False


def run(terms, start, end, out, delay):
    years = list(range(start, end + 1))
    results = {term: {} for term in terms}

    for term in terms:
        print(f"\n{term}")
        for year in years:
            count, success = safe_get(term, year)
            if not success:
                print(f"  {year}: RATE LIMITED — stopping. Wait a few hours and retry.")
                sys.exit(1)
            results[term][year] = count
            print(f"  {year}: {count}", flush=True)
            time.sleep(delay)

    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["year"] + terms)
        for year in years:
            writer.writerow([year] + [results[term].get(year, "") for term in terms])

    print(f"\nSaved: {out}")

    # Summary table
    col_w = 22
    print("\nSummary:")
    header = f"{'year':<6}" + "".join(f"{t[:col_w-2]:<{col_w}}" for t in terms) + "TOTAL"
    print(header)
    for year in years:
        vals = [results[term].get(year, 0) for term in terms]
        print(f"{year:<6}" + "".join(f"{v:<{col_w}}" for v in vals) + str(sum(vals)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multi-term Google Scholar trend tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--terms", nargs="+", required=True,
        help='Search terms. Wrap phrases in inner quotes, e.g. \'"pluralistic alignment"\''
    )
    parser.add_argument("--start", type=int, required=True, help="Start year (inclusive)")
    parser.add_argument("--end",   type=int, required=True, help="End year (inclusive)")
    parser.add_argument("--delay", type=float, default=3.0,
                        help="Seconds between requests (default: 3). Increase if rate-limited.")
    parser.add_argument("--out", default="data/results_by_term.csv",
                        help="Output CSV path (default: data/results_by_term.csv)")
    args = parser.parse_args()

    run(args.terms, args.start, args.end, args.out, args.delay)
