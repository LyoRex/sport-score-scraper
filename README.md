# sport-score-scraper
Command line python program using web scraping to get sports scores.
The program currently supports NBA and NFL scores. Use to get scores from any day of any season of the NBA or scores from any week in any season of the NFL.

Install:
  1. Download ss.py file
  2. Place ss.py file in desired directory

Use:
  1. Open command prompt
  2. cd into directory containing ss.py file
  3. NBA and NFL score commands differ ('or' means the two arguments are interchangeable. ';' separates possible argumets)

***Commands***

**NBA scores:**
  * Command 1: *python ss.py <"b" or "basketball"> <"y" or "yesterday" ; "t" or "today> <{number of days back}>*
    * {number of days back}: only valid when selecting the "y" input. This determines how many days back to go
  * Command 2: *python ss.py <"b" or "basketball"> <{month}> <{day}> <{year}>*

**NFL scores:**
  * Command 1: *python ss.py <"f" or "football"> <"y" or "yesterday" ; "t" or "today> <{number of days back}>*
    * {number of days back}: only valid when selecting the "y" input. This determines how many days back to go
  * Command 2: *python ss.py <"f" or "football"> <{season year}> <{week}>*
