# This is literally the definition of spaghetti code. But it works! Good luck trying to follow it

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import datetime
import sys
import os
import requests


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def aria_find(desc, index):
    return rows[index].find('td', {'aria-describedby': desc}).text.replace(
           '    ', ' ').replace('   ', ' ').replace('  ', ' ').strip()


def remove_line(text, line_start) -> str:
    i = text.find(line_start)
    while True:
        if i != -1:
            text = text[:i - 1] + text[text.find('\n', i):]
            i = text.find(line_start, i)
        else:
            break
    return text


class Meeting:
    def __init__(self, code, name, type, sect, prof, days, time, bldg, room):
        self.code = code
        self.name = name
        self.type = type
        self.sect = sect
        self.prof = prof
        self.days = days
        self.time = time
        self.bldg = bldg
        self.room = room


class Final:
    def __init__(self, code, name, prof, date, time, bldg, room, type):
        self.code = code
        self.name = name
        self.prof = prof
        self.date = date
        self.time = time
        self.bldg = bldg
        self.room = room
        self.type = type


current_class = ''
class_rows = 0
meetings = []
finals = []
i = 0

clear()
choice = input('Would you like to extract the information from:\n[1] The WebReg website\n[2] A file\n')
clear()
print('------------------------------------------------------------------------')

if choice == '1':
    print('Extracting from WebReg: ')
    print('------------------------------------------------------------------------')

    options = Options()
    options.headless = True

    print('ALL INFO IS STORED LOCALLY AND NEVER PLACED ANYWHERE BUT UCSD\'S WEBSITE')
    print('------------------------------------------------------------------------')

    user = input('What is your UCSD username: ')
    password = input('What is your password: ')

    censored_password = '*' * len(password)

    clear()
    print('------------------------------------------------------------------------\n'
          'Extracting from WebReg:\n'
          '------------------------------------------------------------------------\n'
          'ALL INFO IS STORED LOCALLY AND NEVER PLACED ANYWHERE BUT UCSD\'S WEBSITE\n'
          '------------------------------------------------------------------------\n'
          'What is your UCSD username: ' + user + '\n' +
          'What is your password: ' + censored_password)

    print('------------------------------------------------------------------------')
    print('Starting webdriver, be patient, this process may take long...')

    driver = webdriver.Firefox(options=options)

    print('Connecting to WebReg...')
    driver.get('https://act.ucsd.edu/webreg2/start')
    print('Entering username and password...')
    elem = driver.find_element_by_name('urn:mace:ucsd.edu:sso:username')
    elem.clear()
    elem.send_keys(user)
    elem = driver.find_element_by_name('urn:mace:ucsd.edu:sso:password')
    elem.clear()
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    print('Verifying...')

    while True:
        try:
            assert 'UCSD SSO' in driver.title
            print('Sign-in Successful.')
            print('Waiting for page to load...')
            break
        except AssertionError:
            try:
                driver.find_element_by_id('_login_error_message')
                print('Password and username incorrect.\nExiting...')
                sys.exit()
            except NoSuchElementException:
                pass

    while True:
        try:
            driver.find_element_by_xpath('/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button')
            break
        except NoSuchElementException:
            while True:
                try:
                    driver.switch_to.default_content()
                    iframes = driver.find_element_by_id('duo_iframe')
                    driver.switch_to.frame(iframes)
                    break
                except Exception as e:
                    pass
            pass

    while True:
        try:
            driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div/button')
            break
        except Exception as e:
            try:
                driver.find_element_by_xpath('/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button').click()
            except Exception as e:
                pass
        pass

    while True:
        try:
            print(driver.find_element_by_xpath('//span[@class=\'message-text\']').text)
            break
        except Exception as e:
            pass

    while True:
        try:
            if 'Success' in driver.find_element_by_xpath('//span[@class=\'message-text\']').text:
                print(driver.find_element_by_xpath('//span[@class=\'message-text\']').text)
                break
            else:
                raise SystemError
        except Exception as e:
            pass

    while True:
        try:
            driver.switch_to.default_content()
            if driver.find_element_by_id('startpage-select-term').text != '':
                break
        except Exception as e:
            pass

    select = driver.find_element_by_id('startpage-select-term')

    dropdown_options = []

    for i in select.find_elements_by_tag_name('option'):
        if 'med' not in (i.text.lower()) and 'special' not in (i.text.lower()):
            dropdown_options.append(i)

    select = Select(select)

    print('------------------------------------------------------------------------')
    print('Select desired quarter:')
    for i in range(len(dropdown_options)):
        print('[' + str(i + 1) + '] ' + dropdown_options[i].text)

    try:
        option = int(input('').replace(' ', '')) - 1
    except Exception as e:
        print('Invalid input.\nExiting...')
        sys.exit()

    print('------------------------------------------------------------------------')
    print('Waiting for page to load...')

    selection = dropdown_options[option].text.lower().replace('quarter', '').replace('session', '')
    selection = selection.replace(' i ', ' 1 ').replace(' ii ', ' 2 ').replace(' ', '')
    select.select_by_visible_text(dropdown_options[option].text)

    while True:
        try:
            driver.find_element_by_id('list-id-table')
            print('Gathering data...')
            input_source = BeautifulSoup(driver.page_source, 'html.parser')
            print('Closing webdriver...')
            driver.close()
            break
        except Exception as e:
            while True:
                try:
                    if driver.find_element_by_id('startpage-msgs').text != '':
                        print(driver.find_element_by_id('startpage-msgs').text.replace('\n', ' '))
                        sys.exit()
                    driver.switch_to.default_content()
                    driver.find_element_by_id('startpage-button-go').click()
                    break
                except Exception as e:
                    pass
            pass

    try:
        year = int(selection[len(selection) - 4:])
        quarter = selection[:len(selection) - 4]
    except Exception as e:
        print('That is not a valid option.\nExiting...')
        sys.exit()

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


elif choice == '2':
    print('Extracting from a file:')
    print('------------------------------------------------------------------------')
    print('Go to https://act.ucsd.edu/webreg2/main?p1=FA20&p2=UN#tabs-0, make sure')
    print('your schedule is shown on the page. Right click, \'Save Page As\', and')
    print('save the file.')
    print('------------------------------------------------------------------------')
    filename = input('Please type the path to the file location:\n')

    if filename == '':
        filename = 'example_input'

    if '.htm' not in filename:
        filename = filename + '.html'

    print('------------------------------------------------------------------------')

    try:
        quarter = int(input('What quarter is the selected schedule from?\n[1] Fall\n[2] Winter\n[3] Spring\n[4] '
                            'Summer Session 1\n[5] Summer Session 2\n'))
        print('------------------------------------------------------------------------')
        year = int(input('What year is the selected schedule from?\n'))
        print('------------------------------------------------------------------------')
    except Exception as e:
        print('Invalid input.\nExiting...')
        sys.exit()

    f1 = open(filename, 'r')
    input_source = BeautifulSoup(f1.read(), 'html.parser')
    f1.close()


else:
    print('Invalid input.\nExiting...')
    sys.exit()

if quarter == 1:
    years = str(year) + '-' + str(int(year + 1))
elif quarter == 2:
    years = str(int(year - 1)) + '-' + str(year)
elif quarter == 3:
    years = str(int(year - 1)) + '-' + str(year)
elif quarter == 4:
    years = str(int(year - 1)) + '-' + str(year)
elif quarter == 5:
    years = str(int(year - 1)) + '-' + str(year)
else:
    print('Invalid input.\nExiting...')
    sys.exit()

print('Downloading UCSD ' + years + ' Academic Calendar')
r = requests.get('https://blink.ucsd.edu/_files/SCI-tab/' + years + '-academic-calendar.ics')

with open(years + '-academic-calendar.ics', 'wb+') as f2:
    f2.write(r.content)

f2 = open(str(years) + '-academic-calendar.ics', 'r')
academic_calendar = f2.read()
f2.close()

if '<!DOCTYPE html>' in academic_calendar:
    print('Too far in the future or too far in the past.\nExiting...')
    sys.exit()

academic_calendar = academic_calendar[academic_calendar.find('BEGIN:VEVENT'):].replace('BEGIN:VEVENT', '\nBEGIN:VEVENT')

input_source = input_source.find('table', id='list-id-table')
number_of_rows = len(input_source.find_all('tr', role='row', tabindex='-1'))
rows = input_source.find_all('tr', role='row', tabindex='-1')

academic_calendar = remove_line(academic_calendar, 'LAST-MODIFIED:')
academic_calendar = remove_line(academic_calendar, 'PRIORITY:')
academic_calendar = remove_line(academic_calendar, 'SEQUENCE:')
academic_calendar = remove_line(academic_calendar, 'UID:')
academic_calendar = remove_line(academic_calendar, 'X-MICROSOFT-CDO-BUSYSTATUS:')
academic_calendar = remove_line(academic_calendar, 'X-MICROSOFT-CDO-IMPORTANCE')
academic_calendar = remove_line(academic_calendar, 'X-MS-OLK-AUTOFILLLOCATION:')
academic_calendar = remove_line(academic_calendar, 'TRANSP:')
academic_calendar = remove_line(academic_calendar, 'DTSTAMP:')

quarter_starts = []
quarter_ends = []
all_holidays = []

i = academic_calendar.find('SUMMARY:')
while True:
    if i != -1:
        if ('begin' in academic_calendar[i + 8:academic_calendar.find('\n', i)]) \
                and ('struction' in academic_calendar[i + 8:academic_calendar.find('\n', i)]):
            quarter_starts.append(datetime.date(int(academic_calendar[i - 9:i - 5]),
                                                int(academic_calendar[i - 5:i - 3]),
                                                int(academic_calendar[i - 3:i - 1])))
        i = academic_calendar.find('SUMMARY:', i + 8)
    else:
        break

i = academic_calendar.find('SUMMARY:')
while True:
    if i != -1:
        if ('end' in academic_calendar[i + 8:academic_calendar.find('\n', i)]) \
                and ('struction' in academic_calendar[i + 8:academic_calendar.find('\n', i)]):
            quarter_ends.append(datetime.date(int(academic_calendar[i - 9:i - 5]),
                                              int(academic_calendar[i - 5:i - 3]),
                                              int(academic_calendar[i - 3:i - 1])))
        i = academic_calendar.find('SUMMARY:', i + 8)
    else:
        break


for i in range(len(quarter_starts)):
    if i + 1 == quarter:
        quarter_starts = quarter_starts[i]
        quarter_ends = quarter_ends[i]
        break


i = academic_calendar.find('SUMMARY:')
while True:
    if i != -1:
        if 'day' in academic_calendar[i + 8:academic_calendar.find('\n', i)].lower():
            all_holidays.append(datetime.date(int(academic_calendar[i - 9:i - 5]),
                                              int(academic_calendar[i - 5:i - 3]),
                                              int(academic_calendar[i - 3:i - 1])))

            holiday_start_date = datetime.date(int(academic_calendar[i - 9:i - 5]),
                                               int(academic_calendar[i - 5:i - 3]),
                                               int(academic_calendar[i - 3:i - 1]))
            holiday_end_date = datetime.date(int(academic_calendar[i - 37:i - 33]),
                                             int(academic_calendar[i - 33:i - 31]),
                                             int(academic_calendar[i - 31:i - 29]))
            if (holiday_end_date - holiday_start_date).days > 1:
                for j in range((holiday_end_date - holiday_start_date).days - 1):
                    all_holidays.append(holiday_start_date + datetime.timedelta(days=j + 1))
        i = academic_calendar.find('SUMMARY:', i + 8)
    else:
        break

holidays = []
for i in all_holidays:
    if quarter_starts <= i <= quarter_ends:
        holidays.append(i)

i = 0

print('Parsing data...')

while True:
    if i >= number_of_rows:
        break

    if aria_find('list-id-table_colsubj', i) != '':

        current_class = aria_find('list-id-table_colsubj', i)

        if current_class[len(current_class):] == ' ':
            current_class = current_class[:len(current_class) - 1]

        name = aria_find('list-id-table_CRSE_TITLE', i)
        prof = aria_find('list-id-table_PERSON_FULL_NAME', i)

        j = 1
        while True:
            if i + j < number_of_rows:
                if aria_find('list-id-table_colsubj', i + j) == '':
                    class_rows = i + j
                else:
                    if j == 1:
                        class_rows = i
                    break
            else:
                class_rows = number_of_rows - 1
                break
            j += 1

        j = i
        while j <= class_rows:
            if aria_find('list-id-table_FK_CDI_INSTR_TYPE', j) == '':
                j += 1

            type = rows[j].find('td', {'aria-describedby': 'list-id-table_FK_CDI_INSTR_TYPE'}).get('title')
            sect = aria_find('list-id-table_SECT_CODE', j)
            days = aria_find('list-id-table_DAY_CODE', j).replace('M', 'MO,').replace('Tu', 'TU,').replace('W', 'WE,')
            days = days.replace('Th', 'TH,').replace('F', 'FR,').replace('Sa', 'SA,').replace('Su', 'SU,')
            days = days[:len(days) - 1]
            time = aria_find('list-id-table_coltime', j).replace('a', '').replace(':', '')
            bldg = aria_find('list-id-table_BLDG_CODE', j)
            room = aria_find('list-id-table_ROOM_CODE', j)

            if type == 'Final Exam':
                days = aria_find('list-id-table_DAY_CODE', j)[2:].replace(' ', '')
                finals.append(Final(current_class, name, prof, days, time, bldg, room, type))
            elif type == 'Make-up Sessions':
                days = aria_find('list-id-table_DAY_CODE', j)[2:].replace(' ', '')
                finals.append(Final(current_class, name, prof, days, time, bldg, room, 'Make-Up Session'))
            else:
                meetings.append(Meeting(current_class, name, type, sect, prof, days, time, bldg, room))
            j += 1
    else:
        exit()

    i = class_rows + 1

print('Creating \'Calendar.ics\'...')

f3 = open('Calendar.ics', 'w+')
f3.write(
    'BEGIN:VCALENDAR\nPRODID:-//Google Inc//Google Calendar '
    '70.9054//EN\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:'
    'Calendar\nX-WR-TIMEZONE:America/Los_Angeles\nX-WR-CALDESC:\n\nBEGIN:VTIMEZONE\nTZID:America/Los_Angeles\nX-LIC'
    '-LOCATION:America/Los_Angeles\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0800\nTZOFFSETTO:-0700\nTZNAME:PDT\nDTSTART'
    ':19700308T020000\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0700'
    '\nTZOFFSETTO:-0800\nTZNAME:PST\nDTSTART:19701101T020000\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\nEND:STANDARD'
    '\nEND:VTIMEZONE\n')

for i in meetings:
    start = i.time[:i.time.find('-')]
    end = i.time[i.time.find('-') + 1:]

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

    weekdays = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    new_weekdays = []

    for j in range(7):
        new_weekdays.append(weekdays[j + quarter_starts.weekday()])

    for j in range(len(new_weekdays)):
        if new_weekdays[j] in i.days:
            num_days = j
            break

    f3.write('\nBEGIN:VEVENT\n')
    f3.write('DTSTART;TZID=America/Los_Angeles:' +
             str(quarter_starts + datetime.timedelta(days=num_days)).replace('-', '') + 'T' + start + '00\n')
    f3.write('DTEND;TZID=America/Los_Angeles:'
             + str(quarter_starts + datetime.timedelta(days=num_days)).replace('-', '') + 'T' + end + '00\n')

    if i.bldg == 'RCLAS':
        f3.write('SUMMARY:' + i.code + ' ' + i.type + ' (ONLINE)' + '\n')
    else:
        f3.write('SUMMARY:' + i.code + ' ' + i.type + '\n')

    f3.write('RRULE:FREQ=WEEKLY;WKST=SU;UNTIL='
             + str(quarter_ends + datetime.timedelta(days=1)).replace('-', '') + 'T000000Z;BYDAY=' + i.days + '\n')

    for j in holidays:
        if weekdays[j.weekday()] in i.days:
            f3.write('EXDATE;TZID=America/Los_Angeles:' + str(j).replace('-', '') + 'T' + start + '00\n')

    if i.bldg == 'TBA':
        f3.write('LOCATION:TBA\n')
    else:
        f3.write('LOCATION:' + i.bldg + ' ' + i.room + '\n')

    f3.write('STATUS:CONFIRMED\n')
    f3.write('END:VEVENT\n')

for i in finals:
    start = i.time[:i.time.find('-')]
    end = i.time[i.time.find('-') + 1:]

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

    f3.write('\nBEGIN:VEVENT\n')
    f3.write('DTSTART;TZID=America/Los_Angeles:' + str(year) + i.date[0:2] + i.date[3:5] + 'T' + start + '00\n')
    f3.write('DTEND;TZID=America/Los_Angeles:' + str(year) + i.date[0:2] + i.date[3:5] + 'T' + end + '00\n')

    if i.bldg == 'RCLAS' and i.type == 'Make-Up Session':
        f3.write('SUMMARY:' + i.code + ' ' + i.type + ' (ONLINE)' + '\n')
    else:
        f3.write('SUMMARY:' + i.code + ' ' + i.type + '\n')

    if i.bldg == 'TBA':
        f3.write('LOCATION:TBA\n')
    else:
        f3.write('LOCATION:' + i.bldg + ' ' + i.room + '\n')

    f3.write('STATUS:CONFIRMED\n')
    f3.write('END:VEVENT\n')

f3.write(academic_calendar)
f3.close()

os.remove(years+'-academic-calendar.ics')

print('------------------------------------------------------------------------')
print(str(len(meetings) + len(finals)) + ' Unique Calendar Events Created:')
print('------------------------------------------------------------------------')
for i in meetings:
    print('Recurring Event:........' + i.code + ' ' + i.type + ' on ' + i.days)
for i in finals:
    print('One-Time Event:.........' + i.code + ' ' + i.type + ' on ' + i.date[:6] + str(year))
print('------------------------------------------------------------------------')
input('Finished, press return to close.')
