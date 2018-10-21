from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import sqlite3 as sql
import csv

#SQL
database = "spaceapps.db"
secret_key='#SpaceAppsHSV'

def connect_db():
    connection = sql.connect(database)
    connection.row_factory = sql.Row 
    return connection 

def getCursor():
    return connect_db().cursor()

spn = "http://www.spaceflightinsider.com/launch-schedule/"

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
    
def create_connection(db_file):
    try:
        conn = sql.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return none
    
def remove_tags(st):
    while st.find("<") != -1:
        s = st.find("<")
        e = st.find(">")+1
        su = st[s:e]
        st = st.replace(su,"")
    return st
        
def find_by_tag(st,name):
    s = st.find(name)
    s = st.find("<td>",s)+4
    e = st.find("</td",s)
    return remove_tags(st[s:e])
        
    
conn = create_connection(database)

spnPage = simple_get(spn)
html = BeautifulSoup(spnPage, 'html.parser')
missionData = html.find_all('table', class_='launchcalendar')

for data in missionData:
    try:
        header = str(data.find('tr'))
        s = header.find("<span>")+6
        e = header.find("</span>",s)
        backup_date = header[s:e]
        s = header.find("<th col")+1
        s = header.find(">",s)+1
        e = header.find("<",s)
        mission = header[s:e]
        #print(mission)
        rawd = str(data)
        s = rawd.find("url")+5
        e = rawd.find("'",s)
        image = rawd[s:e]
        vehicle = find_by_tag(rawd,"Vehicle")
        #print(vehicle)
        location = find_by_tag(rawd,"Location")
        #print(location)
        time = find_by_tag(rawd,"Time")
        date = ""
        #print(time)
        if time != "TBD":
            s = time.find("/")+2
            e = time.find(" ",s)
            date = time[s:e]
            time = time[e+1:-1]
        else:
            date = backup_date
        #print(date)
        #print(time)
        desc = data.find('td', class_='description')
        desc = desc.find('p')
        desc = desc.text
        #print(desc)
        arts = str(data.find('ul'))
        articles = ""
        s = 0
        s = arts.find("href",s)
        while s != -1:
            s = arts.find("\"",s)+1
            e = arts.find("\"",s)
            articles = articles + arts[s:e] + ";"
            s = arts.find("href",s)
        #print(articles)
        conn = create_connection(database)
        cur = conn.cursor()
        #cur.execute('''INSERT INTO launches VALUES("''' + date + '''","''' + time + '''","''' + location + '''","''' + vehicle + '''","''' + mission + '''","''' + desc + '''","''' + articles + '''","''' + image + '''")''')
        cur.execute('''INSERT INTO launches(date, time, location, vehicle,\
                mission, Description, articles, image) values
                (?,?,?,?,?,?,?,?)''', (date, time, location, vehicle, mission, \
                desc, articles, image))
        conn.commit()
        conn.close()
    
    except Error as e:
        print(e)
    



"""try:
    cur = conn.cursor()
    cur.execute('''INSERT INTO launches VALUES(1,1,"hello","test","fda","fdaasdf","hello","test","fda","fdaasdf","last")''')
    conn.commit()
except Error as e:
    print(e)"""


"""for data in dateName:
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
            #(?,?,?,?,?,?,?,?,?,?,?)", (launchDate, 0, ))"""

