import csv
import os
from datetime import datetime


EXPORT_DIR = "outputs"


def export_results_to_csv(results: list, filename: str = None):
    """
    Export ranked resume results to CSV.
    """

    os.makedirs(EXPORT_DIR, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_ranking_{timestamp}.csv"

    filepath = os.path.join(EXPORT_DIR, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        # ---------- HEADER ----------
        writer.writerow([
            "Rank",
            "Resume",
            "Final Score",
            "JD Score",
            "Market Score",
            "Status",
            "Best Section"
        ])

        # ---------- ROWS ----------
        for rank, res in enumerate(results, start=1):

            writer.writerow([
                rank,
                res["resume"],
                round(res["final_score"], 4),
                round(res["jd_score"], 4),
                round(res["market_score"], 4),
                res["status"],
                res["best_section"]
            ])

    print(f"\nResults exported to: {filepath}")

    return filepath