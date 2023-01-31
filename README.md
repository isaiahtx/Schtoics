# Schtoics
Pronounced "Skuh-tow-icks", Schtoics is a tool that converts a UCSD WebReg schedule and the official UCSD Academic Calendar to a .ICS file that can be used in Google Calendar.

This script *should* work indefinitely, provided UCSD does not change WebReg or the [academic calendar page](https://blink.ucsd.edu/instructors/resources/academic/calendars/2020.html) in any major ways. **It was last checked and was working for the Winter 2023 Quarter on 01/31/2023.**

This was a project done for fun on my own time, I do not make any guarantees about its functionality.

# WARNING:

**The current Windows executable listed in releases does not work and is broken.**

# Usage

There are two options, you can have the script either sign into WebReg for you and scrape the required information, or you can provide the program with an html copy of your WebReg page or just the table with your schedule on it. When providing the script with a copy of your WebReg page, make sure the file is located in the same directory as the script, and make sure the table is actually included in the file (double check by opening the .html file and look for the table there). If you do not see the table after saving the page, inspect element and copy and paste the html code for the table into a file and put it in the same document (make sure it has some sort of extension, if there is none, the script will assume you left out .html).

# How to Run

 - Download [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) for your platform.
 - Download [Firefox](https://www.mozilla.org/en-US/firefox/new/) for your platform.
 - Download the [main.py](https://github.com/isaiahtx/Schtoics/blob/master/main.py) and [requirements.txt](https://github.com/isaiahtx/Schtoics/blob/master/requirements.txt) files and place them in the same directory.
 - Download the latest version of [geckodriver](https://github.com/mozilla/geckodriver/releases) for your platform and add the executable to your PATH.
 - Open a terminal and navigate to the directory where you placed main.py and requirements.txt; run `pip install -r requirements.txt`
 - Run `python main.py` and follow the instructions.

I am currently working on creating an executable that comes bundled with geckodriver that can simply be clicked.

# Adding to Google Calendar
* Go to [calendar.google.com](https://calendar.google.com/)
* Click the "+" next to "Other Calendars"
* Choose "Create new Calendar"
* Name it something like "UCSD Schedule" and set the timezone to LA
* Choose "Import & Export" in the leftmost menu
* Choose "Select file from your computer" and navigate to the Calendar.ics file (should be located in the same directory as the script)
* Choose the calendar you created from the dropdown
* Click import

If you have problems you can try using an incognito window or use another browser (Firefox seems to work best).

# License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
