import subprocess


def run_cppcheck(file_path: str) -> str:
    """
    Executes cppcheck on the given file and returns raw stderr output.
    """

    try:
        result = subprocess.run(
            ["cppcheck", "--enable=all", "--quiet", file_path],
            capture_output=True,
            text=True,
            timeout=20
        )

        return result.stderr

    except subprocess.TimeoutExpired:
        return "Analysis timed out."

    except Exception as e:
        return f"Analysis error: {str(e)}"