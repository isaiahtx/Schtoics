# Schtoics
Pronounced "Skuh-tow-icks", Schtoics is a tool that converts a UCSD WebReg schedule and the official UCSD Academic Calendar to a .ICS file that can be used in Google Calendar


# Installation and usage
Requires Python 3. Install the required python packages with `pip install -r requirements.txt`. [Geckodriver](https://github.com/mozilla/geckodriver/releases) and [Firefox](https://www.mozilla.org/en-US/firefox/) both need to be installed and added to PATH. 

To run, download and run the `main.py` script with python: `python main.py` and follow the instructions.

Provided UCSD's website does not change, it should work indefinitely.


# Adding to Google Calendar
* Go to [calendar.google.com](https://calendar.google.com/)
* Click the "+" next to "Other Calendars"
* Choose "Create new Calendar"
* Name it something like "UCSD Schedule" and set the timezone to LA
* Choose "Import & Export" in the leftmost menu
* Choose "Select file from your computer" and navigate to the Calendar.ics file (should be located in the same directory as the script)
* Choose the calendar you created from the dropdown
* Click import

# License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
