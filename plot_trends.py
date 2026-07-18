"""Plot a stacked area chart from multi_term_search.py output.

Usage:
    python plot_trends.py data/results_by_term.csv \\
        --partial-year 2026 --partial-label Jul \\
        --title "Pluralistic Alignment Research — Google Scholar Counts" \\
        --out figures/scholar_trends.png
"""

import argparse
import csv

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def load_csv(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    years = [int(r["year"]) for r in rows]
    terms = [k for k in rows[0].keys() if k != "year"]
    data = {term: [int(r[term]) for r in rows] for term in terms}
    return years, terms, data


def stacked_total_at(years, data, x):
    """Linear interpolation of the stacked total at fractional year x."""
    totals = [sum(data[t][i] for t in data) for i in range(len(years))]
    if x <= years[0]:
        return totals[0]
    if x >= years[-1]:
        return totals[-1]
    for i in range(len(years) - 1):
        if years[i] <= x <= years[i + 1]:
            frac = (x - years[i]) / (years[i + 1] - years[i])
            return totals[i] + frac * (totals[i + 1] - totals[i])
    return totals[-1]


def plot(years, terms, data, partial_year, partial_label, out, title, annotate=None):
    fig, ax = plt.subplots(figsize=(11, 6))

    colors = plt.cm.tab10.colors[: len(terms)]
    values = [data[t] for t in terms]
    labels = [t.strip('"') for t in terms]

    ax.stackplot(years, values, labels=labels, colors=colors, alpha=0.85)

    tick_labels = [str(y) if y != partial_year else f"{y}*" for y in years]
    ax.set_xticks(years)
    ax.set_xticklabels(tick_labels)
    ax.set_xlabel("Year")
    ax.set_ylabel("Google Scholar Results (CS/Engineering, excl. patents)")
    ax.set_title(title)
    ax.legend(fontsize=8, loc="upper left")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3)

    if annotate:
        label, x_pos = annotate
        y_pos = stacked_total_at(years, data, x_pos)
        y_max = max(sum(data[t][i] for t in data) for i in range(len(years)))
        ax.annotate(
            label,
            xy=(x_pos, y_pos),
            xytext=(x_pos - 0.55, y_pos + 0.35 * y_max),
            fontsize=9, color="black", ha="center",
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
        )

    if partial_year:
        fig.text(
            0.99, 0.01, f"* Jan–{partial_label} {partial_year} only",
            ha="right", va="bottom", fontsize=8, color="dimgray",
        )

    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"Saved: {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Stacked area chart of multi-term Scholar results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("csv", help="Path to results_by_term.csv")
    parser.add_argument(
        "--partial-year", type=int, default=None,
        help="Mark this year with * and add a 'partial year' footnote"
    )
    parser.add_argument(
        "--partial-label", default="Jun",
        help="End month for the partial-year footnote, e.g. 'Jul' (default: Jun)"
    )
    parser.add_argument("--out", default="figures/scholar_trends.png",
                        help="Output image path (default: figures/scholar_trends.png)")
    parser.add_argument("--title", default="Google Scholar Counts by Search Term",
                        help="Plot title")
    parser.add_argument(
        "--annotate", nargs=2, metavar=("LABEL", "YEAR"), default=None,
        help='Annotate an event with an arrow, e.g. --annotate "Roadmap released" 2024.12'
    )
    args = parser.parse_args()

    annotate = (args.annotate[0], float(args.annotate[1])) if args.annotate else None
    years, terms, data = load_csv(args.csv)
    plot(years, terms, data, args.partial_year, args.partial_label, args.out, args.title,
         annotate=annotate)
