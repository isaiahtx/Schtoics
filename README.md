# Schtoics
Pronounced "Skuh-tow-icks", Schtoics is a tool that converts a UCSD WebReg schedule and the official UCSD Academic Calendar to a .ICS file that can be used in Google Calendar.

This script *should* work indefinitely, provided UCSD does not change WebReg or the [academic calendar page](https://blink.ucsd.edu/instructors/resources/academic/calendars/2020.html) in any major ways.

This was a project done for fun on my own time, I do not make any guarantees about its functionality.

# Installation

12/25/2020: .exe added! Go to [releases](https://github.com/isaiahtx/Schtoics/releases/) in order to get it. The instructions are the exact same, just run the .exe. If using a .html file, simply place the .html file in the same folder as the directory in which the .exe file is located.

Requires Python 3. Install the required python packages with `pip install -r requirements.txt`. [Geckodriver](https://github.com/mozilla/geckodriver/releases) and [Firefox](https://www.mozilla.org/en-US/firefox/) both need to be installed and added to your PATH. 

# Usage

To run, download and run the `main.py` script with python: `python main.py`. There are two options, you can have the script either sign into WebReg for you and scrape the required information, or you can provide the program with an html copy of your WebReg page or just the table with your schedule on it. **When providing the script with a copy of your WebReg page, make sure the file is located in the same directory as the script, and make sure the table is actually included in the file (double check by opening the .html file and look for the table there)**. If you do not see the table after saving the page, inspect element and copy and paste the html code for the table into a file and put it in the same document (make sure it has some sort of extension, if there is none, the script will assume you left out `.html`).

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
