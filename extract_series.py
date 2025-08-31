# Import standard Python libraries
import csv, re, sys, pathlib

# Determine the input file:
# - If the user gave a filename as the first argument when running the script, use that
# - Otherwise, default to "input.csv"
INFILE = sys.argv[1] if len(sys.argv) > 1 else "input.csv"

# Output file name where the cleaned results will be written
OUTFILE = "series_only.txt"

# Regular expression pattern that detects rows that look like episodes
# (?i) = case-insensitive
# \b   = word boundary (so "Seasoning" won't match)
# Matches words like Season, Episode, Limited Series, or patterns like S01E02, Ep. 4, Part, Chapter
episode_pat = re.compile(r'(?i)\b(Season|Episode|Limited Series|S\d+\s*E\d+|E\d+|Ep\.?\s*\d+|Part|Chapter)\b')

def normalize(s: str) -> str:
    """
    Cleans up a text string (title).
    - Fixes common encoding issues (mojibake like “â€¦”)
    - Collapses multiple spaces/tabs into one
    - Strips whitespace at the ends
    """
    try:
        # Attempt to re-encode and decode to fix badly encoded characters
        s = s.encode('latin1').decode('utf-8')
    except Exception:
        # If that fails, just leave the string as-is
        pass
    # Replace runs of whitespace with a single space, and strip leading/trailing spaces
    return re.sub(r'\s+', ' ', s).strip()

# Use a set to store series names because sets automatically prevent duplicates
series = set()

# Open the input file safely with context manager
with open(INFILE, newline='', encoding='utf-8', errors='replace') as f:
    # Read the first few KB to guess what delimiter is used (tab, comma, or semicolon)
    sample = f.read(4096)
    f.seek(0)  # go back to start of file
    dialect = csv.Sniffer().sniff(sample, delimiters="\t,;")

    # Try reading the file as a dictionary (column names → values)
    reader = csv.DictReader(f, dialect=dialect)

    # If no headers are found, or if there is no "Title" column, fall back to simple row access
    if not reader.fieldnames or 'Title' not in reader.fieldnames:
        f.seek(0)  # rewind again
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            if not row: 
                continue  # skip empty rows
            title = normalize(row[0])  # assume first column is the Title
            # If this row looks like an episode
            if episode_pat.search(title):
                # Split on the first colon and keep only the base show name
                base = title.split(":", 1)[0].strip()
                series.add(base)
    else:
        # Otherwise, process rows normally with the "Title" column
        for row in reader:
            title = normalize(row.get('Title', ''))
            if not title:
                continue
            # If this row looks like an episode
            if episode_pat.search(title):
                # Keep only the series name (before the first colon)
                base = title.split(":", 1)[0].strip()
                series.add(base)

# Write all the collected series names to the output file
with open(OUTFILE, "w", encoding="utf-8") as out:
    # Sort alphabetically (case-insensitive)
    for name in sorted(series, key=str.lower):
        out.write(name + "\n")

# Print a summary message
print(f"Wrote {len(series)} series to {OUTFILE}")
