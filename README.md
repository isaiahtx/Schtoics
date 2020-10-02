# Schtoics
Pronounced "Skuh-tow-icks", Schtoics is a tool that converts a UCSD WebReg schedule and the official UCSD Academic Calendar to a .ICS file that can be used in Google Calendar.

This script *should* work indefinitely, provided UCSD does not change WebReg or the [academic calendar page](https://blink.ucsd.edu/instructors/resources/academic/calendars/2020.html) in any major ways.


# Installation

Requires Python 3. Install the required python packages with `pip install -r requirements.txt`. [Geckodriver](https://github.com/mozilla/geckodriver/releases) and [Firefox](https://www.mozilla.org/en-US/firefox/) both need to be installed and added to your PATH. 

# Usage

To run, download and run the `main.py` script with python: `python main.py`. There are two options, you can have the script either sign into WebReg for you and scrape the required information, or you can provide the program with an html copy of your WebReg page or just the table with your schedule on it.

**If you are providing the script with an html file, it might not accept the file unless it is located in the same directory as the script itself.**

When the script is finished, the completed Calendar.ics file will be placed in the same directory as the script.

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
