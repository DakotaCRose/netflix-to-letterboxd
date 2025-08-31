# netflix-to-letterboxd
A Python script to clean Netflix viewing activity for import into Letterboxd

## Overview
This project helps convert your **Netflix viewing activity** into a clean list that can be imported into [Letterboxd](https://letterboxd.com).

### Why?
Netflix lets you download your profile’s entire history as a `.csv` file.  
You can upload that file directly to a Letterboxd list and it will import all of the **movie titles** that Letterboxd has in its database.  

What you’ll quickly notice is that **shows don’t import**.  
That’s because Netflix stores them as:  Show title: Episode title  (e.g., "DEATH NOTE: Death Note: 1.28" instead of "DEATH NOTE", "Breaking Bad: Season 5: Felina" instead of "Breaking Bad etc...).

Letterboxd doesn’t recognize these as shows, so they’re skipped.  

### What this script does
- Detects rows that look like **episodes** (anything with “Season”, “Episode”, “Limited Series”, etc.).
- Strips out the episode title and keeps only the **series name**.
- Removes duplicates so each show only appears once.
- Outputs a `.txt` file ready to import into Letterboxd.

---

## Instructions

1. Go to [netflix.com/viewingactivity](https://www.netflix.com/viewingactivity) while logged in.  
2. Scroll to the bottom → click **“Download All”** to get your `ViewingActivity.csv`.  
3. **Import that CSV file directly into Letterboxd** first.  
   - This captures all the movies Letterboxd can match.  
4. Next, run this script to generate a cleaned list of **series names**.  
   - This fills in the shows that didn’t import the first time.  

---

## Getting Started

Clone the repo:
```bash
git clone https://github.com/your-username/netflix-to-letterboxd.git
cd netflix-to-letterboxd

python script.py ViewingActivity.csv

series_only.txt

Import to Letterboxd

Go to your profile settings → Import & Export → upload series_only.txt.

This will add all the shows you’ve watched.

Note: Some titles still won’t import because Letterboxd simply doesn’t have them in its database.

Example
Input:
American Primeval: Limited Series: Episode 4, 1/26/2025
Cunk on Life, 1/19/2025
American Primeval: Limited Series: Episode 1, 1/18/2025

After import (step 3) → Cunk on Life is already in Letterboxd.
After script (step 4) → American Primeval is added.

Final combined list on Letterboxd includes both movies and shows.
