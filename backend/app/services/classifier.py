def classify_issue(issue: dict) -> dict:
    """
    Classifies cppcheck issue into safety category and criticality.
    """

    message = issue["message"].lower()
    rule = issue["rule"].lower()
    severity = issue["severity"].lower()

    category = "Rule Violation"
    criticality = "LOW"

    # MEMORY SAFETY
    if "memleak" in rule or "memory" in message:
        category = "Memory Safety"
        criticality = "HIGH"

    elif "uninitialized" in message:
        category = "Memory Safety"
        criticality = "HIGH"

    elif "unusedallocatedmemory" in rule:
        category = "Memory Safety"
        criticality = "MEDIUM"

    # CONCURRENCY
    elif "race" in message:
        category = "Concurrency Risk"
        criticality = "CRITICAL"

    # INTERRUPT / REAL-TIME
    elif "interrupt" in message or "isr" in message:
        category = "Interrupt Handling Risk"
        criticality = "HIGH"

    # STYLE / RULE
    elif severity == "style":
        category = "Coding Rule Violation"
        criticality = "LOW"

    # DEFAULT SEVERITY BASED ADJUSTMENT
    if severity == "error" and criticality == "LOW":
        criticality = "MEDIUM"

    return {
        **issue,
        "category": category,
        "criticality": criticality
    }