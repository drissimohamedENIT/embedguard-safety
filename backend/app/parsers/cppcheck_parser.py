import re


def parse_cppcheck_output(raw_output: str):
    """
    Parses cppcheck raw stderr output into structured issue list.
    """

    issues = []

    pattern = re.compile(
        r"(?P<file>.*?):(?P<line>\d+):(?P<column>\d+): (?P<severity>\w+): (?P<message>.*?) \[(?P<rule>.*?)\]"
    )

    for line in raw_output.splitlines():
        match = pattern.search(line)
        if match:
            issues.append({
                "file": match.group("file"),
                "line": int(match.group("line")),
                "column": int(match.group("column")),
                "severity": match.group("severity"),
                "message": match.group("message"),
                "rule": match.group("rule")
            })

    return issues