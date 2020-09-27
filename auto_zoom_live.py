import auto_zoom
import datetime
import selenium.webdriver
import time
import pprint

Scraper = auto_zoom.ScrapeDocs()
Scraper.auth()
Scraper.read_table_data()

schedule = Scraper.time_link_data
pprint.pprint(schedule)

# create credentials for registration link
creds = {
    "FNAME": "Peter",
    "LNAME": "Gutkovich",
    "EMAIL": "petergutkovich@nestmk12.net"
}

# create ids for inputs
input_ids = {
    "input1": "question_first_name",
    "input2": "question_last_name",
    "input3": "question_email",
    "input4": "question_confirm_email"
}

# create webdriver path
PATH = "C:\\Users\\peter\\chromedriver_win32\\chromedriver.exe"


# function for register
def register(d):
    # find all inputs
    input1 = d.find_elements_by_id(input_ids['input1'])[0]
    input2 = d.find_elements_by_id(input_ids['input2'])[0]
    input3 = d.find_elements_by_id(input_ids['input3'])[0]
    input4 = d.find_elements_by_id(input_ids['input4'])[0]

    # print(input1, input2, input3, input4)
    # value inputs
    input1.send_keys(creds['FNAME'])
    input2.send_keys(creds['LNAME'])
    input3.send_keys(creds['EMAIL'])
    input4.send_keys(creds['EMAIL'])


# set weekends
weekends = [5, 6]

# get letter day (A or B)
letter_day = input("today's(or last) letter name(A day or B day): ")

# get day that the program started running
day = datetime.datetime.now().strftime("%d")

while True:
    # now time
    now = datetime.datetime.now()

    # get weekday
    weekday = datetime.datetime.today().weekday()

    # check if it's a weekday
    weekend = False
    if weekday in weekends:
        weekend = True

    if not weekend:
        # get time
        hour_min = now.strftime("%H:%M:%S")
        # print("time: " + hour_min)

        # get the day
        today = now.strftime("%d")

        # if it's a weekday day(this is true when program is ran for more than 1 day)
        if today != day:
            # change letter day
            if letter_day == "A":
                letter_day = "B"

            else:
                letter_day = "A"

            # reset day and rescan schedule
            day = today
            Scraper.read_table_data()
            schedule = Scraper.time_link_data

        # check if it's time to connect to the zoom
        if hour_min in schedule:
            print("IT'S ALREADY TIME YOU BRUH")
            zoom_link = schedule[hour_min]

            # check for A day or B day
            if len(zoom_link) > 1:
                if letter_day == "A":
                    zoom_link = zoom_link[0]

                if letter_day == "B":
                    zoom_link = zoom_link[1]

            else:
                zoom_link = zoom_link[0]

            # start web driver and check links
            driver = selenium.webdriver.Chrome(PATH)
            # check if the link is a join link or a register link
            if ".zoom.us/j/" in zoom_link:
                driver.get(zoom_link)

            if ".zoom.us/meeting/register" in zoom_link:
                driver.get(zoom_link)
                register(driver)

            # give user time until driver closes
            time.sleep(20)

            # close driver
            try:
                driver.close()

            except Exception:
                print("Driver Was Already Closed")

    # delay
    time.sleep(1)
