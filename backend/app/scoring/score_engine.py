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

    severity_summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
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

        severity_summary[criticality.lower()] += 1

        score -= penalty_map.get(criticality, 2)

    score = max(score, 0)

    # Risk level classification
    if score >= 90:
        risk = "low"
    elif score >= 70:
        risk = "medium"
    elif score >= 40:
        risk = "high"
    else:
        risk = "critical"

    return {
        "score": score,
        "risk_level": risk,
        "breakdown": breakdown,
        "summary": severity_summary
    }