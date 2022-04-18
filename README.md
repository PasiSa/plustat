# plustat - Collector and visualization of A+ statistics

Plustat is a small tool for collecting and visualizing submission statistics
from A+ LMS using the A+ REST API. Plustat aims to avoid redundant queries by
storing the query results in small local **sqlite3** database, to be reused is needed
in different visualisations.

The code is developed incrementally after needed graphs and lacks overall nice design.
It does not aim to win coding beaty contests.

The code is mainly distributed in two directories:

  * `lib`: common functions used for accessing A+ API and producing graphs

  * `scripts`: that can be called from shell to do various things

## Command line usage

The following scripts can be run from the command line (assuming plustat root).
All scripts require configuration file as command line argument. Configuration
file is a python file, but the .py suffix is left out from command line.

  * `python3 -m scripts.create_tables <config_file>`: Creates needed database tables
  for collecting data. Typically needed only once, when setting up the system.

  * `python3 -m scripts.update_courses <config_file>`: Update the list of courses in plustat database by fetching all current courses from A+ API.

  * `python3 -m scripts.recent_daily <config_file>`: Produce daily submission graphs
  for last 30 days of submissions.

  * `python3 -m scripts.recent_weekly <config_file>`: Produce weekly submission graphs
  for the current semester.


## Configuration parameters

*TBD: create a sample configuration file*

Following parameters are needed:

  * `BASE_URL`: Base URL of the A+ server. Most likely `"https://plus.cs.aalto.fi/"`
  for Aalto users.

  * `AUTH_TOKEN`: API token that can be found in A+ user profile.

  * `DB_FILE`: location of sqlite3 database file.

  * `OUTPUT_DIR`: directory where the produced graphs are stored.

  * `RECENT_DAYS`: how many days are shown by recent_daily script.
