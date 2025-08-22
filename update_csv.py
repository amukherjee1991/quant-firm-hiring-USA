#pylint: disable=missing-function-docstring,line-too-long
#pylint: disable=unused-import,unused-variable
"""
update_csv.py

This script downloads the raw list of quantitative trading firms from a GitHub
gist, parses the firm names and URLs, and writes a CSV file indicating
whether each firm is based in the United States and whether it is hiring.

The status information is maintained in a mapping within this script.  For
firms where reliable evidence exists, the mapping contains a tuple with two
boolean values: (us_based, hiring).  Firms absent from the mapping default to
"Unknown" for both fields.

To extend or refine the classification, edit the STATUS_MAPPING dictionary
below.  Each key should be the exact firm name as it appears in the gist,
and each value should be a tuple (us_based, hiring).  Use True for "Yes",
False for "No", and None for "Unknown".

Run this script with Python 3.  It writes a file named ``all_firms.csv`` in
the current directory.
"""

import csv
import re
from pathlib import Path
import requests


# URL of the raw gist containing the list of firms.
GIST_RAW_URL = "https://gist.githubusercontent.com/chrisaycock/8b7a37b1f97549517cb7789be5b06266/raw/firms.md"

# Mapping of firm names to (US-based, Hiring) status.  True means "Yes", False
# means "No", and None means "Unknown".  Extend this mapping as more
# information becomes available.
STATUS_MAPPING = {
    "3Red Partners": (True, True),
    "Akuna Capital": (True, True),
    "Belvedere Trading": (True, True),
    "DRW": (True, True),
    "DV Trading": (True, True),
    "Gelber Group": (True, True),
    "Geneva Trading": (True, True),
    "GTS": (True, True),
    "Headlands Technologies": (True, True),
    "Hudson River Trading": (True, True),
    "Jump Trading": (True, True),
    "Kore Trading": (True, True),
    "Quantbot Technologies": (True, True),
    "Radix Trading": (True, True),
    "Teza Technologies": (True, True),
    "Valkyrie Trading": (True, True),
    "Vatic Investments": (True, True),
    "Volant Trading": (True, False),
    "Wolverine Trading": (True, True),
    "Walleye Capital": (True, True),
    "Tower Research Capital": (True, True),
    "Tradebot": (True, True),
    "Tradelink Holdings": (True, None),
    "TransMarket Group": (True, True),
    "Trexquant Investment": (True, True),
}


def fetch_gist() -> str:
    """Download the raw gist content and return it as a string."""
    response = requests.get(GIST_RAW_URL, timeout=30)
    response.raise_for_status()
    return response.text


def parse_firms(content: str):
    """Parse the firm names and URLs from the raw gist Markdown content."""
    pattern = re.compile(r"\* \[(.+?)\]\((.+?)\)")
    for line in content.splitlines():
        m = pattern.match(line.strip())
        if m:
            name, url = m.groups()
            yield name.strip(), url.strip()


def write_csv(firms, filename="all_firms.csv"):
    """Write the firm data to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Firm", "URL", "US Based", "Hiring"])
        for name, url in firms:
            status = STATUS_MAPPING.get(name, (None, None))
            us_based, hiring = status

            def fmt(value):
                if value is True:
                    return "Yes"
                if value is False:
                    return "No"
                return "Unknown"

            writer.writerow([name, url, fmt(us_based), fmt(hiring)])
    print(f"CSV written to {filename}")


def main():
    content = fetch_gist()
    firms = list(parse_firms(content))
    write_csv(firms)


if __name__ == "__main__":
    main()
