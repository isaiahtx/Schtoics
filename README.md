# Update: I graduated spring of 2024, so I have no way of verifying if this works anymore. Use at your own risk!


# Schtoics
Pronounced "Skuh-tow-icks", Schtoics is a tool that converts a UCSD WebReg schedule and the official UCSD Academic Calendar to a .ICS file that can be used in Google Calendar.

This script *should* work indefinitely, provided UCSD does not change WebReg or the [academic calendar page](https://blink.ucsd.edu/instructors/resources/academic/calendars/2020.html) in any major ways. **It was last checked and was working for the Spring 2024 Quarter on 04/06/2024.**

This was a project done for fun on my own time, I do not make any guarantees about its functionality.

# Features
 - Supports every kind of class type, e.g. seminars, labs, exam-only classes, summer classes, etc.
 - Automatically scrapes information from the official UCSD calendar in order to determine correct start and end dates for fall, winter, spring quarters and both summer sessions.
 - Adds holes in schedule for holidays.
 - Handles classes with multiple time-slots for an exam/discussion which make you pick one by allowing you to add either all of the options or just one to your calendar.
 - More generally, warns you if theres duplicate entries and allows you to choose which ones to keep.
 - Allows you to choose whether or not you’d like to combine the official UCSD calendar with your schedule calendar (useful if you use the program for different quarters in the same schoolyear).
 - Includes planned/waitlisted classes from your schedule.

**If you find out that your schedule doesn't work with Schtoics, send me the .html file with your class list information at isaiah@ucsd.edu and I'll make it work.**

# Usage

There are two options, you can have the script either sign into WebReg for you and scrape the required information, or you can provide the program with an html copy of your WebReg page or just the table with your schedule on it. When providing the script with a copy of your WebReg page, make sure the file is located in the same directory as the script, and make sure the table is actually included in the file (double check by opening the .html file and look for the table there). If you do not see the table after saving the page, inspect element and copy and paste the html code for just the table into a file and put it in the same document (make sure it has some sort of extension, if there is none, the script will assume you left out .html).

# How to Run

 - Download [python](https://www.python.org/downloads/) for your platform (last checked with Python 3.11)
 - Download [Firefox](https://www.mozilla.org/en-US/firefox/new/) for your platform.
 - Download the [main.py](https://github.com/isaiahtx/Schtoics/blob/master/main.py) and [requirements.txt](https://github.com/isaiahtx/Schtoics/blob/master/requirements.txt) files and place them in the same directory.
 - Open a terminal and navigate to the directory where you placed main.py and create a python environment by running `python -m venv .`
 - Install the additional required packages by running `./bin/pip install -r requirements.txt`
 - Run `./bin/python main.py` and follow the instructions.

# Adding to Google Calendar
* Go to [calendar.google.com](https://calendar.google.com/)
* Click the "+" next to "Other Calendars"
* Choose "Create new Calendar"
* Name it something like "UCSD Schedule" and set the timezone to LA
* Choose "Import & Export" in the leftmost menu
* Choose "Select file from your computer" and navigate to the Calendar.ics file (should be located in the same directory as the script)
* Choose the calendar you created from the dropdown
* Click import

**IT IS VERY IMPORTANT THAT YOU MAKE A NEW CALENDAR FOR THIS FILE, AS MY PROGRAM IS NOT PERFECT AND CAN SOMETIMES BREAK**

If you have problems you can try using an incognito window or use another browser (Firefox seems to work best).

# License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
