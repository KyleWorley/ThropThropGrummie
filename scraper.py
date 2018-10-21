from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import sqlite3 as sql
import csv

# I AM ASHAMED TO DO DO THIS
countries = []
with open('countries.csv', 'r') as csvfile:
     reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in reader:
         countries.append(''.join(row))

#SQL
database = "spaceapps.db"
secret_key='#SpaceAppsHSV'

def connect_db():
    connection = sql.connect(database)
    connection.row_factory = sql.Row 
    return connection 

def getCursor():
    return connect_db().cursor()

spn = "https://spaceflightnow.com/launch-schedule/"

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

spnPage = simple_get(spn)

html = BeautifulSoup(spnPage, 'html.parser')

missionData = html.find_all('div', class_='missiondata')
descriptions = html.find_all('div', class_='missdescrip')
dateName = html.find_all('div', class_='datename')

#for data in missionData:
#    print(data.text)

for data in dateName:
    launchDate = data.find('span', class_='launchdate')
    print(launchDate.text)

    mission = data.find('span', class_='mission')
    missionModel = mission.text.split("•")[0]
    missionName = mission.text.split("•")[1][1:]

    print(missionModel)
    print(missionName)

    missionData = data.find_next('div', class_='missiondata')
    launchSiteLine = missionData.text.split("\n")[1]
    launchSite = launchSiteLine[13:]
    for country in countries:
        if country in launchSite:
            launchCountry = country
    print(launchSite)

    description = data.find_next('div', class_='missdescrip').text
    print(description)

   # con = connect_db()
   # date INTEGER, time INTEGER, country TEXT, state TEXT, location TEXT, Manufacturer TEXT, model TEXT, mission TEXT, Description TEXT, link TEXT, image TEXT
   #con.execute("insert into launches(date, time, country, state, location,
            #Manufacturer, model, mission, Description, link, image") values
            #(?,?,?,?,?,?,?,?,?,?,?)", (launchDate, 0, ))

