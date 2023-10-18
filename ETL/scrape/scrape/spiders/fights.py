import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from datetime import date
import re
import logging
import random

logging.basicConfig(
    filename="log.txt", format="%(levelname)s: %(message)s", level=logging.INFO
)

log = logging.getLogger()

class FighterSpider2(CrawlSpider):
    name = "fights"
    allowed_domains = ["ufcstats.com"]
    
    #allows us to make small testing batches
    #custom_settings = {'CLOSESPIDER_PAGECOUNT':50 }

    start_urls = ['http://www.ufcstats.com/statistics/events/completed?page=all']
    #you can also use a list for the rules instead of a generator
    rules = (
        Rule(LinkExtractor(allow="event-details",deny="fight-details"),callback=None ),
        Rule(LinkExtractor(allow="fight-details", deny="fighter-details"), callback="parse_data")
    )
    
    def parse_data(self, response):
        nameList = response.css("div.l-page__container div.b-fight-details__person a.b-link.b-fight-details__person-link::text").getall()
        letter = response.css("div.b-fight-details div.b-fight-details__persons.clearfix div.b-fight-details__person i.b-fight-details__person-status::text").get().strip()
        winner = ""
        # something like 1% of fights loose winner and strike data together
        # no clear pattern yet 
        if letter == "W":
            winner = nameList[0]
        elif letter == "L":
            winner = nameList[1]
            
        div = getDivision(response.css("div.l-page__container div.b-fight-details__fight div.b-fight-details__fight-head").get())
        timeData = response.css("div.l-page__container div.b-fight-details__fight div.b-fight-details__content").get()
        timeList = response.css("div.l-page__container div.b-fight-details__fight div.b-fight-details__content i.b-fight-details__text-item::text").getall()
        timeData = cleanTime(timeList)
        format = getFormat(timeData)
        dur = getDuration(timeData)
        ctrlTable = response.css("section.b-fight-details__section.js-fight-section tbody.b-fight-details__table-body tr.b-fight-details__table-row p").getall()
        ctrlList = getCtrl(ctrlTable)
        ctrl1 = cleanCtrl(ctrlList, 1)
        ctrl2 = cleanCtrl(ctrlList, 2)
        strTable = response.css("table").getall()
        sigR1 = cleanSigStr(strTable,1)
        sigR2 = cleanSigStr(strTable,2)
        strList1 = strikeData(strTable,1)
        strList2 = strikeData(strTable,2)
        # the data is skewed toward the first fighter being the winner 
        # this last step is to mix the name fields to eliminate bias and overfitting 
        # the else statement has all fighter 1 and two data swapped so winne is second
        if random.random() <= 0.5:
            yield {
                "winner": winner.strip(),
                "name1": nameList[0].strip(),
                "name2": nameList[1].strip(),
                "division": div,
                "rounds": format,
                "duration":dur,
                "ctrl1":ctrl1,
                "ctrl2":ctrl2,
                "sigRatio1":sigR1,
                "sigRatio2":sigR2,
                "sigLand1":cleanLanded(strList1[0]),
                "sigLand2":cleanLanded(strList2[0]),
                "sigAmpt1":cleanAmpt(strList1[0]),
                "sigAmpt2":cleanAmpt(strList2[0]),
                "headLand1":cleanLanded(strList1[1]),
                "headLand2":cleanLanded(strList2[1]),
                "headAmpt1":cleanAmpt(strList1[1]),
                "headAmpt2":cleanAmpt(strList2[1]),
                "bodyLand1":cleanLanded(strList1[2]),
                "bodyLand2":cleanLanded(strList2[2]),
                "bodyAmpt1":cleanAmpt(strList1[2]),
                "bodyAmpt2":cleanAmpt(strList2[2]),
                "legLand1":cleanLanded(strList1[3]),
                "legLand2":cleanLanded(strList2[3]),
                "legAmpt1":cleanAmpt(strList1[3]),
                "legAmpt2":cleanAmpt(strList2[3]),
                "distanceLand1":cleanLanded(strList1[4]),
                "distanceLand2":cleanLanded(strList2[4]),
                "distanceAmpt1":cleanAmpt(strList1[4]),
                "distanceAmpt2":cleanAmpt(strList2[4]),
                "clinchLand1":cleanLanded(strList1[5]),
                "clinchLand2":cleanLanded(strList2[5]),
                "clinchAmpt1":cleanAmpt(strList1[5]),
                "clinchAmpt2":cleanAmpt(strList2[5]),
                "groundLand1":cleanLanded(strList1[6]),
                "groundLand2":cleanLanded(strList2[6]),
                "groundAmpt1":cleanAmpt(strList1[6]),
                "groundAmpt2":cleanAmpt(strList2[6])
            }
        else:
            yield {
            "winner": winner.strip(),
            "name1": nameList[1].strip(),
            "name2": nameList[0].strip(),
            "division": div,
            "rounds": format,
            "duration":dur,
            "ctrl1":ctrl2,
            "ctrl2":ctrl1,
            "sigRatio1":sigR2,
            "sigRatio2":sigR1,
            "sigLand1":cleanLanded(strList2[0]),
            "sigLand2":cleanLanded(strList1[0]),
            "sigAmpt1":cleanAmpt(strList2[0]),
            "sigAmpt2":cleanAmpt(strList1[0]),
            "headLand1":cleanLanded(strList2[1]),
            "headLand2":cleanLanded(strList1[1]),
            "headAmpt1":cleanAmpt(strList2[1]),
            "headAmpt2":cleanAmpt(strList1[1]),
            "bodyLand1":cleanLanded(strList2[2]),
            "bodyLand2":cleanLanded(strList1[2]),
            "bodyAmpt1":cleanAmpt(strList2[2]),
            "bodyAmpt2":cleanAmpt(strList1[2]),
            "legLand1":cleanLanded(strList2[3]),
            "legLand2":cleanLanded(strList1[3]),
            "legAmpt1":cleanAmpt(strList2[3]),
            "legAmpt2":cleanAmpt(strList1[3]),
            "distanceLand1":cleanLanded(strList2[4]),
            "distanceLand2":cleanLanded(strList1[4]),
            "distanceAmpt1":cleanAmpt(strList2[4]),
            "distanceAmpt2":cleanAmpt(strList1[4]),
            "clinchLand1":cleanLanded(strList2[5]),
            "clinchLand2":cleanLanded(strList1[5]),
            "clinchAmpt1":cleanAmpt(strList2[5]),
            "clinchAmpt2":cleanAmpt(strList1[5]),
            "groundLand1":cleanLanded(strList2[6]),
            "groundLand2":cleanLanded(strList1[6]),
            "groundAmpt1":cleanAmpt(strList2[6]),
            "groundAmpt2":cleanAmpt(strList1[6])
        }

def getDivision(result):
    found = re.findall("Strawweight|Flyweight|Bantamweight|Featherweight|Lightweight|Welterweight|Middleweight|Light\s{1}Heavyweight|Heavyweight", result)
    return found[0].strip()

def cleanTime(result):
    i = 0 
    r = []
    for item in result:
        if i == 1:
            r.append(item.strip())
        if i == 3:
            r.append(item.strip())
        if i == 5:
            r.append(item.strip())
        if i > 5: 
            continue
        i = i + 1
    return r

def getFormat(timeData):
    f = int(timeData[2][0:1])
    return f


def getDuration(timeData):
    rounds = int(timeData[0])
    min = int(timeData[1][0:1])
    sec = int(timeData[1][2:])
    dur = 0
    dur = ((rounds - 1) * 60 * 5)
    dur = dur + (min * 60) + sec
    return dur
      

def getCtrl(result):
    i = 0
    l = []
    for r in result:
        if i >= 18 and i < 20:
            if re.search("\d\D{1}\d{2}", r) is not None:
                l.append(re.search("\s+\d\D{1}\d{2}", r).group(0).strip())
        i = i + 1
    return l

def cleanCtrl(cList, which):
    c = cList[which - 1]
    time = c[1]
    min = int(c[0:1])
    sec = int(c[2:])
    return (min * 60) + sec

def strikeData(result,which):
    # uses a regex to group all numeric data for all remaining metrics 
    # then splits into a list of 7 items for each fighter 
    # this flattens the data and makes the last step cleaner 
    m = []
    r = []
    if re.search("(\d{1,2}\s\w{2}\s\d{1,3})", result[2]) is not None:
                m = re.findall("(\d{1,2}\s\w{2}\s\d{1,3})", result[2])
    # make a list with all data in order per fighter 
    # i = 0,1 -> sig strikes take 
    # i = 2,3 -> head 
    # i = 4,5 -> body 
    # i = 6,7 -> leg 
    # i = 8,9 -> distance 
    # i = 10,11 -> clinch 
    # i = 12,13 -> ground
    if which == 1:
        r.append(m[0])
        r.append(m[2])
        r.append(m[4])
        r.append(m[6])
        r.append(m[8])
        r.append(m[10])
        r.append(m[12])
    elif which == 2:
        r.append(m[1])
        r.append(m[3])
        r.append(m[5])
        r.append(m[7])
        r.append(m[9])
        r.append(m[11])
        r.append(m[13])
    return r
   
def cleanSigStr(result,which):
    l = []
    p = ""
    if re.search("(\d{2,3}(%))", result[2]) is not None:
        l = re.findall("(\d{2,3}(%))", result[2])
        if len(l) >= 1:
            if which == 1:
                p = "0." + l[0][0]
                return float(p[0:-1])
            elif which == 2:
                p = "0." + l[1][0]
                return float(p[0:-1])
    return None
#  result[2] # <--- this table has all the data on strikes 
# sigstrike/sigstrike%/head/body/leg/distance/clinch/ground
# go throught this with a regex for \d{1,2}\s(of)\s\d{1,3} for strike ratios 
# use a percent regex for percent data 
# store each fighters strike data
                        
                        
                        
def cleanLanded(result):
    m = []
    if re.search("\d{1,3}", result) is not None:
                m = re.findall("\d{1,3}", result)
    return int(m[0])

def cleanAmpt(result):
    m = []
    if re.search("\d{1,3}", result) is not None:
                m = re.findall("\d{1,3}", result)
    return int(m[1])
  
                        