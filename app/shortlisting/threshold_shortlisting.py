SHORTLIST_THRESHOLD = 0.5
REVIEW_THRESHOLD = 0.4


def assign_status(score: float) -> str:
    """
    Assign hiring decision based on score.
    """

    if score >= SHORTLIST_THRESHOLD:
        return "SHORTLISTED"

    elif score >= REVIEW_THRESHOLD:
        return "REVIEW"

    return "REJECT"


def apply_shortlisting(results: list):
    """
    Add decision label to ranked results.
    """

    updated_results = []

    for res in results:

        status = assign_status(res["final_score"])

        res["status"] = status

        updated_results.append(res)

    return updated_results