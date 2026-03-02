def calculate_safety_score(issues: list) -> dict:
    """
    Calculates firmware safety score based on issue criticality.
    Score starts at 100 and decreases depending on severity.
    """

    score = 100

    breakdown = {
        "Memory Safety": 0,
        "Concurrency Risk": 0,
        "Interrupt Handling Risk": 0,
        "Coding Rule Violation": 0,
        "Rule Violation": 0
    }

    penalty_map = {
        "CRITICAL": 20,
        "HIGH": 12,
        "MEDIUM": 6,
        "LOW": 1
    }

    for issue in issues:
        category = issue.get("category", "Rule Violation")
        criticality = issue.get("criticality", "LOW")

        breakdown[category] = breakdown.get(category, 0) + 1
        score -= penalty_map.get(criticality, 2)

    # Prevent negative scores
    score = max(score, 0)

    return {
        "score": score,
        "breakdown": breakdown
    }