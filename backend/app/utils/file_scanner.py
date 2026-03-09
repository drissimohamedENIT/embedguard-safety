import os

SUPPORTED_EXTENSIONS = (".c", ".cpp", ".h", ".hpp")


def discover_source_files(directory: str):

    files = []

    for root, _, filenames in os.walk(directory):
        for f in filenames:
            if f.endswith(SUPPORTED_EXTENSIONS):
                files.append(os.path.join(root, f))

    return files