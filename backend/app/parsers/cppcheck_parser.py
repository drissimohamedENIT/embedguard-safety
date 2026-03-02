import re
import os


IGNORED_RULES = {
    "checkersReport",
    "missingIncludeSystem"
}


def parse_cppcheck_output(raw_output: str):
    issues = []

    pattern = re.compile(
        r"(?P<file>.*?):(?P<line>\d+):(?P<column>\d+): (?P<severity>\w+): (?P<message>.*?) \[(?P<rule>.*?)\]"
    )

    for line in raw_output.splitlines():
        match = pattern.search(line)
        if match:

            rule = match.group("rule")

            if rule in IGNORED_RULES:
                continue

            file_path = match.group("file")

            if file_path == "nofile":
                continue

            issues.append({
                "file": os.path.basename(file_path),
                "line": int(match.group("line")),
                "column": int(match.group("column")),
                "severity": match.group("severity"),
                "message": match.group("message"),
                "rule": rule
            })

    return issues