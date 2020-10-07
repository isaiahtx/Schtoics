from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, \
                                       ElementNotInteractableException, \
                                       StaleElementReferenceException, \
                                       WebDriverException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import datetime
import sys
import os
import requests


# Defines a function to clear the console based on the OS being used
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


# The information in the table created by WebReg identifies all of its information by the 'aria-describedby' tag,
# this function returns the text of the element with the desired identifier and cleans it up, so to speak.
def aria_find(desc, element):
    return element.find('td', {'aria-describedby': desc}).text.replace(
        '    ', ' ').replace('   ', ' ').replace('  ', ' ').strip()


# This function, given a multi-line string, removes all lines that start with the selected substring.
def remove_line(text, line_start) -> str:
    i_keep_running_out_of_indices = text.find(line_start)
    while True:
        if i_keep_running_out_of_indices != -1:
            text = text[:i_keep_running_out_of_indices - 1] + text[text.find('\n', i_keep_running_out_of_indices):]
            i_keep_running_out_of_indices = text.find(line_start, i_keep_running_out_of_indices)
        else:
            break
    return text


# This class is used to store the identifying information for any recurring event
class Recurring:
    def __init__(self, code, _name, _type, section, professor, _days, _time, building, _room):
        self.code = code
        self.name = _name
        self.type = _type
        self.sect = section
        self.prof = professor
        self.days = _days
        self.time = _time
        self.bldg = building
        self.room = _room


# This class is used to store the identifying information for any one-time event
class OneTime:
    def __init__(self, code, _name, professor, date, _time, building, _room, _type):
        self.code = code
        self.name = _name
        self.prof = professor
        self.date = date
        self.time = _time
        self.bldg = building
        self.room = _room
        self.type = _type


# Asks the user if they want to get the information from a file or from a website
clear()
choice = input('Would you like to extract the information from:\n[1] The WebReg website\n[2] A file\n') # TODO add quit option esc, ^c, q
clear()

print('--------------------------------------------------------------------------------')

if choice == '1':  # If the user decides to extract the schedule information from WebReg:
    print('Extracting from WebReg: ')
    print('--------------------------------------------------------------------------------')
    print('ALL INFO IS STORED LOCALLY AND NEVER PLACED ANYWHERE BUT UCSD\'S WEBSITE')
    print('--------------------------------------------------------------------------------')

    # TODO: Find a way to not show the password as the user is typing it, instead show dots or asterisks
    # Asks the user for their UCSD username and password
    user = input('What is your UCSD username: ')
    password = input('What is your password: ')

    # 'Censors' the password, so to speak.
    clear()
    print('--------------------------------------------------------------------------------\n'
          'Extracting from WebReg:\n'
          '--------------------------------------------------------------------------------\n'
          'ALL INFO IS STORED LOCALLY AND NEVER PLACED ANYWHERE BUT UCSD\'S WEBSITE\n'
          '--------------------------------------------------------------------------------\n'
          'What is your UCSD username: ' + user + '\n' +
          'What is your password: ' + '*' * len(password))

    print('--------------------------------------------------------------------------------')
    print('Starting webdriver, be patient, this process may take long...')

    # Initializes the scraper as headless
    options = Options()
    options.headless = True

    # Initialize the webdriver using Firefox and the earlier outlined options
    driver = webdriver.Firefox(options=options)

    # Navigates to WebReg
    print('Connecting to WebReg...')
    driver.get('https://act.ucsd.edu/webreg2/start')

    # Enters the username and password in their respective fields
    print('Entering username and password...')
    elem = driver.find_element_by_name('urn:mace:ucsd.edu:sso:username')
    elem.clear()
    elem.send_keys(user)
    elem = driver.find_element_by_name('urn:mace:ucsd.edu:sso:password')
    elem.clear()
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    # This loop checks to see if the next page has loaded or if the password and username are incorrect.
    print('Verifying...')
    while True:
        try:
            assert 'UCSD SSO' in driver.title  # Check if we've reached the authentication page
            print('Sign-in Successful.')
            print('Waiting for page to load...')
            break  # If it is there, then break the loop, continue on
        except AssertionError:  # If 'UCSD SSO' is not in the title, check to see if the password is wrong
            try:
                driver.find_element_by_id('_login_error_message')  # Look for an error message
                print('Password and username incorrect.\nExiting...')
                driver.close()
                sys.exit()  # If the error message is found exit the program
            except NoSuchElementException:
                # If there is no error message found then check if we've reached the authentication page again
                # Rinse and repeat
                pass

    # This loop looks for the button that sends a 2FA push to Duo, clicks it, and then makes sure that the request
    # actually went through.
    while True:
        try:
            driver.switch_to.default_content()  # Switch scope back to the main page
            driver.switch_to.frame(driver.find_element_by_id('duo_iframe'))  # Switch to Duo iframe where the button is
            driver.find_element_by_css_selector('button.auth-button.positive').click()  # Click the auth button
            # Look for the 'cancel request' button, which only comes up when the 2FA request button has been clicked
            driver.find_element_by_css_selector('button.btn-cancel')
            break
        except (ElementNotInteractableException, NoSuchElementException):
            pass  # If any of the above steps fail, run through the whole thing repeatedly until it works

    # This loop checks to make sure that the 2FA request was successfully sent
    while True:
        try:
            # Check to make sure that the 2FA request was sent
            if 'Pushed a login request' in driver.find_element_by_xpath('//span[@class=\'message-text\']').text:
                print(driver.find_element_by_xpath('//span[@class=\'message-text\']').text)
                break
            else:  # If a message is given saying that something other than the request was sent, exit
                sys.exit()
        except SystemExit:  # TODO: Fix this monstrosity below lol
            if driver.find_element_by_xpath('//span[@class=\'message-text\']').text == '':
                pass
            else:
                if 'Pushed a login request' in driver.find_element_by_xpath('//span[@class=\'message-text\']').text:
                    print(driver.find_element_by_xpath('//span[@class=\'message-text\']').text)
                    break
                else:
                    print(driver.find_element_by_xpath('//span[@class=\'message-text\']').text)
                    print('If you see a blank line above, there was an error with the script. Try running it again')
                    print('\nExiting...')
                    driver.close()
                    sys.exit()
        except NoSuchElementException:  # If no message has come up, assume it's still loading and try again
            pass

    # This loop checks to see if the 2FA request was confirmed or not
    while True:
        try:
            # If we get a success message, continue on!
            if 'Success' in driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div/span').text:
                print(driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div/span').text)
                break
            # If the message still says 'Pushed a login request...' then we're still waiting on the user, try again
            elif 'Pushed a login request' in driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div/span').text:
                pass
            # If the message says it's denied, exit
            elif 'denied' in driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div/span').text:
                print('Error: ' + driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div/span').text)
                driver.close()
                sys.exit()
            # If none of the above work, it's still loading or being changed, try again
            else:
                pass
        # If there is no message, it's in the process of being changed, keep checking for success
        except (StaleElementReferenceException, NoSuchElementException):
            pass
        except WebDriverException:  # This is weird, but if we get a WebDriver error, that means the sign in work.
            print("Success! Logging you in...")
            break
        except SystemExit:
            print('Exiting...')
            sys.exit()

    # This loop looks for the dropdown on WebReg which has list of available quarters that we can pull a schedule from
    while True:
        try:
            driver.switch_to.default_content()  # Make sure we're out of the Duo iframe
            # If we find the dropdown, continue on!
            if driver.find_element_by_id('startpage-select-term').text != '':
                break
        # If the dropdown isn't found, it's still loading, try again
        except NoSuchElementException:
            pass

    # Initialize array that stores the quarter options available in the dropdown
    dropdown_options = []

    # Now we need to actually get all of the quarter options available, but only if they're fall, winter, spring, or a
    # regular summer session.
    for i in driver.find_element_by_id('startpage-select-term').find_elements_by_tag_name('option'):
        # More exclusions might need to be added beyond med school and special sessions
        if 'med' not in (i.text.lower()) and 'special' not in (i.text.lower()):
            dropdown_options.append(i)

    # We use Selenium's select class to actually be able to select the user's desired option before continuing to the
    # schedule.
    select = Select(driver.find_element_by_id('startpage-select-term'))

    # Display the dropdown options to the user
    print('--------------------------------------------------------------------------------')
    print('Select desired quarter:')
    for i in range(len(dropdown_options)):
        print('[' + str(i + 1) + '] ' + dropdown_options[i].text)

    # If the user's input cannot be converted to an integer or is not a valid dropdown index, exit
    try:
        user_selection = dropdown_options[int(input('').replace(' ', '')) - 1]
    except ValueError:
        print('Invalid input.\nExiting...')
        driver.close()
        sys.exit()

    select.select_by_visible_text(user_selection.text)  # Select the user's desired option

    # Cleans up the input by getting rid of extra words and spaces among other things
    user_selection = user_selection.text.lower().replace('quarter', '').replace('session', '')
    user_selection = user_selection.replace(' i ', ' 1 ').replace(' ii ', ' 2 ').replace(' ', '')

    # Get the year and quarter from the dropdown choice the user chose earlier.
    # The last four digits are the year, the rest is the quarter.
    try:
        year = int(user_selection[len(user_selection) - 4:])
        quarter = user_selection[:len(user_selection) - 4]
    except ValueError:
        # If somehow the last four digits aren't all numbers, the dropdown option the user selected is either not
        # supported or was changed in a way that I didn't anticipate.
        print('That is not a valid option.\nExiting...')
        sys.exit()

    print('--------------------------------------------------------------------------------')
    print('Waiting for page to load...')

    # This loop clicks "go", gathers the page source, and checks for any error message
    while True:
        try:
            driver.find_element_by_id('list-id-table')  # Look for the table schedule
            print('Gathering data...')
            # If the table schedule is found, save the page source as 'input_source' and close the webdriver
            # We are going to use BeautifulSoup for the rest as I like it better than Selenium
            input_source = BeautifulSoup(driver.page_source, 'html.parser')
            print('Closing webdriver...')
            driver.close()
            break
        except NoSuchElementException:
            # If we can't find the table (which we won't the first time as we haven't clicked go yet), then find and
            # click go after checking there are no error messages (which there will not be the first time).
            try:
                if driver.find_element_by_id('startpage-msgs').text != '':
                    # Look for non-blank error message, if found, print the error message to the user and exit
                    print(driver.find_element_by_id('startpage-msgs').text.replace('\n', ' '))
                    driver.close()
                    sys.exit()
                # Click the 'go' button if there's no error message
                driver.switch_to.default_content()
                driver.find_element_by_id('startpage-button-go').click()
            except (ElementNotInteractableException, NoSuchElementException):
                # If we can't click or can't find the go button or the error message element, the page is still
                # loading, try again.
                pass
            except SystemExit:  # Exit if we find a non-blank error message
                sys.exit()
            pass

    # It should be obvious what this bit does, we need the quarters as integers for later logic
    if quarter == 'fall':
        quarter = 1
    elif quarter == 'winter':
        quarter = 2
    elif quarter == 'spring':
        quarter = 3
    elif quarter == 'summer1':
        quarter = 4
    elif quarter == 'summer2':
        quarter = 5
    else:
        print('That is not a valid option.\nExiting...')
        sys.exit()


elif choice == '2':  # If the user decides to extract the schedule information from a file:
    print('Extracting from a file:')
    print('--------------------------------------------------------------------------------')
    print('Go to https://act.ucsd.edu/webreg2/start, sign in, make sure your')
    print('schedule is shown on the page. Right click, \'Save Page As\', and save')
    print('the file.')
    print('--------------------------------------------------------------------------------')
    filename = input('Please type the path to the file location:\n')

    # If the user doesn't specify a filename, resort to the example_input.html file provided
    if filename == '':
        filename = 'example_input'

    # If the user doesn't specify a file extension, add '.html' to the end of the filename
    if '.' not in filename:
        filename = filename + '.html'

    print('--------------------------------------------------------------------------------')

    # We need to manually ask the user for the quarter and year of their schedule
    try:
        quarter = int(input('What quarter is the selected schedule from?\n[1] Fall\n[2] Winter\n[3] Spring\n[4] '
                            'Summer Session 1\n[5] Summer Session 2\n'))
        if quarter - 1 not in range(5):
            raise ValueError
        print('--------------------------------------------------------------------------------')
        year = int(input('What year is the selected schedule from?\n'))
        print('--------------------------------------------------------------------------------')
    except ValueError:  # If the input is not an integer 1-5, then exit
        print('Invalid input.\nExiting...')
        sys.exit()

    # Grab the source from the file
    # We are going to use BeautifulSoup for the rest as I like it better than Selenium
    try:
        f1 = open(filename, 'r')  # Open the file provided by the user
        input_source = BeautifulSoup(f1.read(), 'html.parser')  # Create a BeautifulSoup html object from the file
        f1.close()  # Close the file
    except FileNotFoundError:  # If an invalid file is given, then exit
        print('File not found.\nExiting...')
        sys.exit()

else:  # If the user doesn't input 1 or 2 (WebReg or file), then exit
    print('Invalid input.\nExiting...')
    sys.exit()

# Next we need to download the academic calendar from UCSD's official website in order to get important dates from it.
# UCSD typically has them available for download at https://blink.ucsd.edu/_files/SCI-tab/<years>-academic-calendar.ics.
# <years> is the school year range, i.e., 2020-2021.
if quarter == 1:
    # If the selected quarter is fall, it's at the beginning of the school year, so we want the calendar that starts
    # with the selected year. For example, to see start and end dates of the Fall 2020 quarter, we want the 2020-2021
    # calendar, not the 2019-2020 calendar.
    years = str(year) + '-' + str(int(year + 1))
elif quarter == 2:
    # If the selected quarter is *not* fall, it's at the end of the school year, so we want the calendar that starts
    # the year *before* the selected year. For example, to see start and end dates of the Winter 2021 quarter, we want
    # the 2020-2021 calendar, not the 2021-2022 calendar.
    years = str(int(year - 1)) + '-' + str(year)
elif quarter == 3:
    years = str(int(year - 1)) + '-' + str(year)
elif quarter == 4:
    years = str(int(year - 1)) + '-' + str(year)
elif quarter == 5:
    years = str(int(year - 1)) + '-' + str(year)
else:  # If somehow 'quarter' is not an integer 1-5, then exit, although I believe that the script would exit sooner.
    print('Invalid input.\nExiting...')
    sys.exit()

# Gets the chosen academic calendar and saves it to a file
print('Downloading UCSD ' + years + ' Academic Calendar')
r = requests.get('https://blink.ucsd.edu/_files/SCI-tab/' + years + '-academic-calendar.ics')
with open(years + '-academic-calendar.ics', 'wb+') as f2:
    f2.write(r.content)

# Opens the file just downloaded and stores its contents as a string to academic_calendar variable
# There's probably a better way to do this then saving the academic calendar file, reading from the file, and then
# deleting the file, but I have yet to figure it out on my own and I'm too lazy to look it up.
f2 = open(str(years) + '-academic-calendar.ics', 'r')
academic_calendar = f2.read()
f2.close()
os.remove(years + '-academic-calendar.ics')

# If the selected calendar file does not exist, instead of getting an .ics file we'll get an html file of UCSD's
# website saying "this page does not exist". In that case, the user chose a year for which a calendar doesn't exist.
if '<!DOCTYPE html>' in academic_calendar:
    print('Too far in the future or too far in the past.\nExiting...')
    sys.exit()

# Removes ICS header information from academic_calendar, as well as adds a newline before every event for readability's
# sake.
academic_calendar = academic_calendar[academic_calendar.find('BEGIN:VEVENT'):].replace('BEGIN:VEVENT', '\nBEGIN:VEVENT')

# Remove all the unnecessary lines from academic_calendar
academic_calendar = remove_line(academic_calendar, 'LAST-MODIFIED:')
academic_calendar = remove_line(academic_calendar, 'PRIORITY:')
academic_calendar = remove_line(academic_calendar, 'SEQUENCE:')
academic_calendar = remove_line(academic_calendar, 'UID:')
academic_calendar = remove_line(academic_calendar, 'X-MICROSOFT-CDO-BUSYSTATUS:')
academic_calendar = remove_line(academic_calendar, 'X-MICROSOFT-CDO-IMPORTANCE')
academic_calendar = remove_line(academic_calendar, 'X-MS-OLK-AUTOFILLLOCATION:')
academic_calendar = remove_line(academic_calendar, 'TRANSP:')
academic_calendar = remove_line(academic_calendar, 'DTSTAMP:')

# TODO: Reassess the location of any initialization variables
# Initialize some variables for later

quarter_starts = None
quarter_ends = None
holidays = []

# This loop looks for any event in academic_calendar that has 'begin' and 'struction' (from 'instruction') in it, finds
# the date of that event, checks to make sure that it is the same number event as quarter. To explain what that means,
# if quarter = 4, meaning Summer Session I, then we want the 4th event that includes 'begin' and 'struction' in
# academic calendar.
# This loop assumes that the events in the .ics file are in order, which they always have been and should always be.
i = academic_calendar.find('SUMMARY:')
j = 1
while True:
    if i != -1:
        if ('begin' in academic_calendar[i + 8:academic_calendar.find('\n', i)]) \
                and ('struction' in academic_calendar[i + 8:academic_calendar.find('\n', i)]):
            # If 'begin', 'struction', both in the selected event summary, check to make sure it's start date of the
            # selected quarter
            if j == quarter:
                # If we found the desired quarter start date, save it, leave the loop and continue on
                quarter_starts = datetime.date(int(academic_calendar[i - 9:i - 5]),  # year
                                               int(academic_calendar[i - 5:i - 3]),  # month
                                               int(academic_calendar[i - 3:i - 1]))  # day
                break
            j += 1
        i = academic_calendar.find('SUMMARY:', i + 8)
    else:
        # If i == -1 then there are no more lines that start with "SUMMARY:", meaning, we've reached the end, break.
        break

# Does the same as the above loop but looks for 'end' instead of 'begin' and saves to quarter_ends
i = academic_calendar.find('SUMMARY:')
j = 1
while True:
    if i != -1:
        if ('end' in academic_calendar[i + 8:academic_calendar.find('\n', i)]) \
                and ('struction' in academic_calendar[i + 8:academic_calendar.find('\n', i)]):
            if j == quarter:
                quarter_ends = datetime.date(int(academic_calendar[i - 9:i - 5]),  # year
                                             int(academic_calendar[i - 5:i - 3]),  # month
                                             int(academic_calendar[i - 3:i - 1]))  # day
                break
            j += 1
        i = academic_calendar.find('SUMMARY:', i + 8)
    else:
        break

# Looks for any event with 'day' in the summary, checks to see if said event is within the quarter start-end date
# range, and adds a datetime.date object to holidays. I checked all the calendars can see, without fail, as far as I
# could tell, any event with the word 'day' in it was a holiday.
i = academic_calendar.find('SUMMARY:')
while True:
    if i != -1:
        if 'day' in academic_calendar[i + 8:academic_calendar.find('\n', i)].lower():
            # If we find 'day' in the event summary, then check to make sure that said day is actually in the quarter
            # of interest.
            holiday_start_date = datetime.date(int(academic_calendar[i - 9:i - 5]),  # year
                                               int(academic_calendar[i - 5:i - 3]),  # month
                                               int(academic_calendar[i - 3:i - 1]))  # day
            holiday_end_date = datetime.date(int(academic_calendar[i - 37:i - 33]),  # year
                                             int(academic_calendar[i - 33:i - 31]),  # month
                                             int(academic_calendar[i - 31:i - 29]))  # day
            for j in range((holiday_end_date - holiday_start_date).days):
                # For multi-day holidays, we need to add an individual holiday date object for every day within that
                # holiday.
                if quarter_starts <= holiday_start_date + datetime.timedelta(days=j) <= quarter_ends:
                    # If the holiday resides within the quarter of interest, add it to holidays list
                    holidays.append(holiday_start_date + datetime.timedelta(days=j))
        i = academic_calendar.find('SUMMARY:', i + 8)
    else:
        # If i == -1 then there are no more lines that start with "SUMMARY:", meaning, we've reached the end, break.
        break

print('Parsing data...')

# Initializing some variables used for later:
# Narrows down the html input to just the table of interest
input_source = input_source.find('table', id='list-id-table')

# Stores the number of rows in the table
number_of_rows = len(input_source.find_all('tr', role='row', tabindex='-1'))

# This creates a list of every row element
rows = input_source.find_all('tr', role='row', tabindex='-1')

# The table has multiple meetings per class, each on its own row. This variable stores the 'current class' that we're
# dealing with. For example, your Math class may have three rows in the table: one for lectures, one for discussions,
# and one for the class final. As the script iterates through the rows, it needs to know which class said row actually
# belongs to.
current_class = ''

# This stores which rows of the table have to do with the current class. For example, if the loop is looking at row 0
# (meaning, i = 0) and class_rows = 3, then we know that rows 0-3 are all for the same class. After looking over how
# the main parsing loop works, the use of this variable should become more clear.
class_rows = 0

# Used for iterative purposes (duh)
i = 0

# These lists are going to store all of the Recurring/OneTime objects that we'll use to make the calendar events later
recurring_events = []
one_time_events = []

# This is the main loop that runs through the each row and picks out important information and makes the calendar
# events. Basically the actual core of the program.
while i < number_of_rows:
    # This assumes the first row contains a class row, which it should.
    # Note that current_class is a string and also the class code
    current_class = aria_find('list-id-table_colsubj', rows[i])

    # If 'current_class' ends in a space, remove it
    if current_class[len(current_class):] == ' ':
        current_class = current_class[:len(current_class) - 1]

    # This loop figures out up to which number row has to do with current_class and saves that number to class_rows
    # Rows with non-empty cells with the tag aria-describedby='list-id-table_colsubj' contain the name of the class
    # itself. For example, if I have a class 'MATH 31AH' with a lecture, discussion, and final, there will be three
    # rows for each one of those events, but only the first row will actually say 'MATH 31AH'. We can use that fact
    # to find out which rows belong to which class.
    j = 1
    while True:
        if i + j < number_of_rows:
            if aria_find('list-id-table_colsubj', rows[i + j]) == '':
                # If we found a non-blank colsubj cell in the row, then that's the next class, class_rows = all
                # the rows from i to the one before this row.
                class_rows = i + j
            else:
                if j == 1:
                    # If j = 1, then that means the current_class only has one row, so class_rows = i, break
                    class_rows = i
                break
        else:
            # If we reached the last row, then we're done, we know that all remaining rows have to do with
            # current_class.
            class_rows = number_of_rows - 1
            break
        j += 1

    # This loop adds the event objects to recurring_events and one_time_events
    j = i
    while j <= class_rows:
        if aria_find('list-id-table_FK_CDI_INSTR_TYPE', rows[j]) == '':
            # Make sure that the selected row actually has a lecture type (i.e., lecture, final, discussion, etc.)
            # If it doesn't have a lecture type, skip that row as it's not an event.
            j += 1

        # TODO: Either make sure all of these attributes are used somewhere or get rid of them
        name = aria_find('list-id-table_CRSE_TITLE', rows[j])  # The name of the event's class

        prof = aria_find('list-id-table_PERSON_FULL_NAME', rows[j])  # The class professor

        # The event type (i.e., 'Lecture', 'Discussion', 'Final')
        _type = rows[j].find('td', {'aria-describedby': 'list-id-table_FK_CDI_INSTR_TYPE'}).get('title')

        sect = aria_find('list-id-table_SECT_CODE', rows[j])  # The event section

        # The days of the week on which the class takes place or the date of the event if it's a OneTime object
        days = aria_find('list-id-table_DAY_CODE', rows[j]).replace('M', 'MO,').replace('Tu', 'TU,').replace('W', 'WE,')
        days = days.replace('Th', 'TH,').replace('F', 'FR,').replace('Sa', 'SA,').replace('Su', 'SU,')
        days = days[:len(days) - 1]

        # The time at which the event takes place
        time = aria_find('list-id-table_coltime', rows[j])

        # The building in which the event takes place
        bldg = aria_find('list-id-table_BLDG_CODE', rows[j])

        # The room in which the event takes place
        room = aria_find('list-id-table_ROOM_CODE', rows[j])

        # If the event days attribute has a slash in it, it happens on a specific date, so it's a OneTime object
        if '/' in days:
            days = aria_find('list-id-table_DAY_CODE', rows[j])[2:].replace(' ', '')  # Remove weekday from date
            if _type == 'Make-up Sessions':
                # I don't like how 'Make-up Sessions' is plural when the event only happens once, so I fixed it.
                _type = 'Make-up Session'
            # Add OneTime object to one_time_events
            one_time_events.append(OneTime(current_class, name, prof, days, time, bldg, room, _type))
        else:
            # Add Recurring event object to recurring_events
            recurring_events.append(Recurring(current_class, name, _type, sect, prof, days, time, bldg, room))
        j += 1

    i = class_rows + 1

# ---------------------------------------------------------------------------------------------------------
# BEGIN DISGUSTING SECTION, PREPARE FOR MAXIMUM SPAGHETTI

print('Searching for duplicate events...')

# Stores a list of lists with [class, type, days] for each recurring event
meeting_names = []
for i in recurring_events:
    meeting_names.append([i.code, i.type, i.days])

# Stores only the duplicates from meeting_names in a new variable duplicates
duplicates = []
for i in meeting_names:
    if meeting_names.count(i) > 1 and i not in duplicates:
        duplicates.append(i)

# For every recurring event list in duplicates, add the times of all the events that mach that event to the event list
# I.e., now duplicates is full of lists that look like: [class, type, days, meeting_time_1, meeting_time_2, etc.)
for i in range(len(recurring_events)):
    for j in duplicates:
        if recurring_events[i].code == j[0] and recurring_events[i].type == j[1] and recurring_events[i].days == j[2]:
            j.append(recurring_events[i].time)

if len(duplicates) == 0:  # If we've reached this points and duplicates is empty, then there are no duplicates (duh)
    print('None found.')
else:  # If duplicate events are found,
    print('--------------------------------------------------------------------------------')
    for i in duplicates:  # For every list in duplicates,
        print('Duplicate events found, which one would you like to keep:')
        k = 1
        for j in range(3, len(i)):  # Print each event with its times
            print('(' + str(k) + ') ' + i[0] + ' ' + i[1] + ' on ' + i[2] + ' at ' + i[j])
            k += 1
        print('(' + str(k) + ') Keep All')
        print('(' + str(k + 1) + ') Keep None')

        try:  # Get input, make sure it's gucci
            keep = int(input('').replace(' ', ''))
        except ValueError:
            print('Invalid input.\nExiting...')
            sys.exit()

        #  Now decide what to do based on the number the user selected
        removals = []
        m = True
        if keep == k + 1:  # Mark everything for removal
            for x in range(len(recurring_events)):
                if recurring_events[x].code == i[0] and recurring_events[x].type == i[1] \
                                                    and recurring_events[x].days == i[2]:
                    removals.append(x)
                    m = True
        elif keep == k:  # Mark nothing for removal
            pass
        elif keep <= 0 or keep >= k + 2:  # Invalid input
            print('Invalid input.\nExiting...')
            sys.exit()
        else:  # Mark everything but the selected one for removal
            for x in range(len(recurring_events)):
                if recurring_events[x].code == i[0] and recurring_events[x].type == i[1] \
                                                    and recurring_events[x].days == i[2]:
                    removals.append(x)
            for x in range(len(recurring_events)):
                if recurring_events[x].code == i[0] and recurring_events[x].type == i[1] \
                                                    and recurring_events[x].days == i[2] \
                                                    and i[keep + 2] == recurring_events[x].time:
                    removals.remove(x)
                    break
        print('--------------------------------------------------------------------------------')
        #  Actually removes items marked for removal
        for index in sorted(removals, reverse=True):
            del recurring_events[index]
# END DISGUSTING SECTION, NOW BACK TO YOUR REGULARLY SCHEDULED CODE THAT'S HAS A NORMAL AMOUNT OF SPAGHETTI
# ---------------------------------------------------------------------------------------------------------

# We'll need this later
for i in recurring_events:
    i.time = i.time.replace('a', '').replace(':', '')

for i in one_time_events:
    i.time = i.time.replace('a', '').replace(':', '')

print('Creating \'Calendar.ics\'...')

# TODO: Let the user choose where they want to save the file BY DEFAULT SAVE WHERE WEBREG FILE IS
# Now we create the actual Calendar.ics file, finally.
f3 = open('Calendar.ics', 'w+')  # Open the file, create if it doesn't exist
f3.write(
    'BEGIN:VCALENDAR\nPRODID:-//Google Inc//Google Calendar '
    '70.9054//EN\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:'
    'Calendar\nX-WR-TIMEZONE:America/Los_Angeles\nX-WR-CALDESC:\n\nBEGIN:VTIMEZONE\nTZID:America/Los_Angeles\nX-LIC'
    '-LOCATION:America/Los_Angeles\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0800\nTZOFFSETTO:-0700\nTZNAME:PDT\nDTSTART'
    ':19700308T020000\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0700'
    '\nTZOFFSETTO:-0800\nTZNAME:PST\nDTSTART:19701101T020000\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\nEND:STANDARD'
    '\nEND:VTIMEZONE\n')  # Basic initialization stuff about timezone, the type of calendar, etc.

# This loop goes through every Recurring event object and adds a calendar event to the Calendar.ics file
for i in recurring_events:
    f3.write('\nBEGIN:VEVENT\n')  # Initialize the calendar event

    # Currently, each event's time attribute is a string which looks like '1100-300p', '830-1230p'. Notice there is no
    # A.M. indicator, no colons, and no spaces. We need to get the start and end time each in the format HHMMSS
    start = i.time[:i.time.find('-')]  # The start time is made up by the digits to the left of the dash
    end = i.time[i.time.find('-') + 1:]  # The end time is made up by the digits to the right of the dash

    # Formats start variable appropriately, I'm too lazy to explain each step
    if start.find('p') == -1:
        if len(start) == 3:
            start = '0' + start
    else:
        if len(start) == 4:
            start = str(int(start[0]) + 12) + start[1:]
        else:
            if start[0:2] == '12':
                start = start[0:4]
            else:
                start = str(int(start[0:2]) + 12) + ':' + start[2:]
        start = start.replace('p', '')
    start = start + '00'

    # Formats end variable appropriately, I'm too lazy to explain each step
    if end.find('p') == -1:
        if len(end) == 3:
            end = '0' + end
    else:
        if len(end) == 4:
            end = str(int(end[0]) + 12) + end[1:]
        else:
            if end[0:2] == '12':
                end = end[0:4]
            else:
                end = str(int(end[0:2]) + 12) + ':' + end[2:]
        end = end.replace('p', '')
    end = end + '00'

    # This is really hacky and hard to explain and there's definitely a better way to do it. Basically, we have this
    # dilemma: We know the date and weekday that the quarter starts on. For example, FA2020 quarter starts on Thursday,
    # October 1st. But many classes don't meet on Thursday, so we can't just tell the calendar that I have an event
    # that starts on October 1st that repeats every Monday, Wednesday, and Friday, or it'll create an event for a class
    # that doesn't exist! So instead, in order to tell the calendar the correct starting date, we have to add the
    # number of days between the day of the week that the quarter starts on and the first day of the week that the
    # class meets. For example, if I have a class that meets every Monday and Wednesday but the first day of the
    # quarter is a Thursday, then the starting day of that class is the starting day of the quarter, plus the number of
    # days between a Thursday and a Monday. I hope that makes sense...

    # TODO: Rename these variables in a way that makes more clear their use
    # First we have a list of the weekdays, twice.
    weekdays = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    new_weekdays = []
    num_days = 0

    # We need a new list of the weekdays, but we want this list to start on the weekday that the quarter starts on
    for j in range(7):
        new_weekdays.append(weekdays[j + quarter_starts.weekday()])

    # Now, we iterate through the new list of weekdays, starting with the day the quarter starts on, checking to see
    # if that weekday is in the Recurring event object's days attribute. The index on which a day is first found is
    # saved to num_days. For example, if the quarter starts on a Thursday, and the recurring event object we're
    # looking at meets every Wednesday and Friday, the for loop will stop at 'FR', the second weekday in the
    # new_weekdays list, resulting in a num_days of 1, meaning, the start date of the event is quarter_start + 1 day.
    for j in range(len(new_weekdays)):
        if new_weekdays[j] in i.days:
            num_days = j
            break

    # Tells the calendar program when the event starts
    # The start date, as explained earlier, is the day the quarter starts plus num_days
    f3.write('DTSTART;TZID=America/Los_Angeles:'
             + str(quarter_starts + datetime.timedelta(days=num_days)).replace('-', '') + 'T' + start + '\n')

    # Tells the calendar program when the event ends
    f3.write('DTEND;TZID=America/Los_Angeles:'
             + str(quarter_starts + datetime.timedelta(days=num_days)).replace('-', '') + 'T' + end + '\n')

    # Tells the calendar program on what weekdays the recurring event happens and on what date it stops.
    f3.write('RRULE:FREQ=WEEKLY;WKST=SU;UNTIL='
             + str(quarter_ends + datetime.timedelta(days=1)).replace('-', '') + 'T000000Z;BYDAY=' + i.days + '\n')

    # Writes the event summary with the class code and type
    # If the event's building is is an online class, let the user know by putting 'ONLINE' in the event summary
    if i.bldg == 'RCLAS':
        f3.write('SUMMARY:' + i.code + ' ' + i.type + ' (ONLINE)' + '\n')
    else:
        f3.write('SUMMARY:' + i.code + ' ' + i.type + '\n')

    # If an event has a meeting on a weekday that is shared by a holiday, then add an exclusion date on that holiday.
    # For example, if a Fall 2020 event meets every Thursday, then we will need to add an exclusion date on
    # Thanksgiving, which is a Thursday.
    for j in holidays:
        if weekdays[j.weekday()] in i.days:
            f3.write('EXDATE;TZID=America/Los_Angeles:' + str(j).replace('-', '') + 'T' + start + '\n')

    # Write the location as the building and room
    # If the building is TBA, then don't show the user the room, as the room is obviously TBA as well.
    if i.bldg == 'TBA':
        f3.write('LOCATION:TBA\n')
    else:
        f3.write('LOCATION:' + i.bldg + ' ' + i.room + '\n')

    f3.write('STATUS:CONFIRMED\n')  # I don't know if this is necessary, but I'm adding it just in case
    f3.write('END:VEVENT\n')  # Let's the calendar program that we're done with this event

# Basically the same thing as the above loop, but for OneTime event objects instead of Recurring event objects.
for i in one_time_events:
    f3.write('\nBEGIN:VEVENT\n')  # Initialize the calendar event

    # See code block in previous for-loop
    start = i.time[:i.time.find('-')]
    end = i.time[i.time.find('-') + 1:]

    # See code block in previous for-loop
    if start.find('p') == -1:
        if len(start) == 3:
            start = '0' + start
    else:
        if len(start) == 4:
            start = str(int(start[0]) + 12) + start[1:]
        else:
            if start[0:2] == '12':
                start = start[0:4]
            else:
                start = str(int(start[0:2]) + 12) + ':' + start[2:]
        start = start.replace('p', '')
    start = start + '00'

    # See code block in previous for-loop
    if end.find('p') == -1:
        if len(end) == 3:
            end = '0' + end
    else:
        if len(end) == 4:
            end = str(int(end[0]) + 12) + end[1:]
        else:
            if end[0:2] == '12':
                end = end[0:4]
            else:
                end = str(int(end[0:2]) + 12) + ':' + end[2:]
        end = end.replace('p', '')
    end = end + '00'

    # Tells the calendar program when the event starts and ends
    f3.write('DTSTART;TZID=America/Los_Angeles:' + str(year) + i.date[0:2] + i.date[3:5] + 'T' + start + '\n')
    f3.write('DTEND;TZID=America/Los_Angeles:' + str(year) + i.date[0:2] + i.date[3:5] + 'T' + end + '\n')

    # Writes the event summary with the class code and type
    # If the event's building is is an online class and it's a make-up session, let the user know by putting 'ONLINE'
    # in the event summary.
    if i.bldg == 'RCLAS' and i.type == 'Make-up Session':
        f3.write('SUMMARY:' + i.code + ' ' + i.type + ' (ONLINE)' + '\n')
    else:
        f3.write('SUMMARY:' + i.code + ' ' + i.type + '\n')

    # Write the location as the building and room
    # If the building is TBA, then don't show the user the room, as the room is obviously TBA as well.
    if i.bldg == 'TBA':
        f3.write('LOCATION:TBA\n')
    else:
        f3.write('LOCATION:' + i.bldg + ' ' + i.room + '\n')

    f3.write('STATUS:CONFIRMED\n')  # I don't know if this is necessary, but I'm adding it just in case
    f3.write('END:VEVENT\n')  # Let's the calendar program that we're done with this event

print('--------------------------------------------------------------------------------')
try:
    # Ask the user if they want to add the events from the academic calendar to the calendar upload.
    include_academic_calendar = input('Do you want to include the academic calendar events in the calendar file? If\n'
                                      'you have used this tool before, choose no. Otherwise, choose yes (Y/n): ').lower()
    if include_academic_calendar == 'y' or include_academic_calendar == 'yes' or include_academic_calendar == '':
        f3.write(academic_calendar)  # Write the entirety of the contents of academic_calendar to the file
        f3.close()  # Close the file, we're done!
    elif include_academic_calendar == 'n' or include_academic_calendar == 'no':
        f3.write('END:VCALENDAR')  # Only write the calendar ending statement to the file
        f3.close()  # Close the file, we're done!
    else:
        raise ValueError
    print('--------------------------------------------------------------------------------')
except ValueError:  # If the user inputs something other than nothing, 'y', 'yes', 'n', or 'no', then exit
    print('Invalid input.\nExiting...')
    f3.close()
    sys.exit()


# Tell the user the unique events we created:
print(str(len(recurring_events) + len(one_time_events)) + ' Unique Calendar Events Created:')
print('--------------------------------------------------------------------------------')
for i in recurring_events:
    print('Recurring Event:........' + i.code + ' ' + i.type + ' on ' + i.days)
for i in one_time_events:
    print('One-Time Event:.........' + i.code + ' ' + i.type + ' on ' + i.date[:6] + str(year))
print('--------------------------------------------------------------------------------')