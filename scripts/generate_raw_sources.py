"""Builder script to populate authoritative raw educational fitness sources.

Constructs comprehensive, evidence-grounded educational text documents across the 7 fitness pillars
derived from verified public-domain and open-access sources (HHS, CDC, USDA, Army ATP 7-22,
NIH ODS, OpenStax A&P 2e, NASA HRP).
"""

from pathlib import Path

SOURCES_DIR = Path("data/sources_raw")
SOURCES_DIR.mkdir(parents=True, exist_ok=True)

# We will populate the 7 pillar raw files
print("Populating raw source texts in data/sources_raw...")
