import subprocess
import sys

subprocess.run([sys.executable, "quick_test.py", "."])


# uvx watchfiles --target-type command "uv run python quick_test.py" .

subprocess.run([
    "uvx",
    "watchfiles",
    "--target-type",
    "command",
    "uv run python script/essays/salutation.py",
    ".",
])