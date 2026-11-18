"""Run the harness: `uv run python -m ci gates`."""

import sys

from ci.cli.main import main

if __name__ == "__main__":
    sys.exit(main())
