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


def plot(years, terms, data, partial_year, partial_label, out, title, figsize=(11, 6),
         fontsize=10):
    plt.rcParams.update({"font.size": fontsize})
    fig, ax = plt.subplots(figsize=figsize)

    colors = plt.cm.tab10.colors[: len(terms)]
    values = [data[t] for t in terms]
    labels = [t.strip('"') for t in terms]

    ax.stackplot(years, values, labels=labels, colors=colors, alpha=0.85)

    tick_labels = [str(y) if y != partial_year else f"{y}*" for y in years]
    ax.set_xticks(years)
    ax.set_xticklabels(tick_labels)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")
    if title:
        ax.set_title(title)
    ax.legend(fontsize=fontsize - 2, loc="upper left")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3)

    if partial_year:
        fig.text(
            0.99, 0.01, f"* Jan–{partial_label} {partial_year} only",
            ha="right", va="bottom", fontsize=fontsize - 2, color="dimgray",
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
        "--figsize", nargs=2, type=float, metavar=("WIDTH", "HEIGHT"),
        default=[11, 6], help="Figure size in inches (default: 11 6)"
    )
    parser.add_argument(
        "--fontsize", type=float, default=10,
        help="Base font size; legend and footnote are 2pt smaller (default: 10)"
    )
    args = parser.parse_args()

    years, terms, data = load_csv(args.csv)
    plot(years, terms, data, args.partial_year, args.partial_label, args.out, args.title,
         figsize=tuple(args.figsize), fontsize=args.fontsize)
