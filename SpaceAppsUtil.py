# SpaceAppsUtil
import math

def dateToWords(self, dateNum):
    # get day
    day = dateNum % 100
    dateNum = dateNum / 100
    # get month
    m = dateNum %100
    dateNum = dateNum/100
    if m == 1:
        month = "January"
    elif m == 2:
        month = "February"
    elif m == 3:
        month = "March"
    elif m == 4:
        month = "April"
    elif m == 5:
        month = "May"
    elif m == 6:
        month = "June"
    elif m == 7:
        month = "July"
    elif m == 8:
        month = "August"
    elif m == 9:
        month = "September"
    elif m == 10:
        month = "October"
    elif m == 11:
        month = "November"
    elif m == 12:
        month = "December"
    else:
        month = m
    # get year
    year = dateNum
    self.dateWords = month + day + year
    return self.dateWords
    
    
