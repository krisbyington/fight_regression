import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from datetime import date
import re

class FighterSpider1(CrawlSpider):
    #TODO 
    
    # add try catch blocks with and loggers to find out 
    ## how to get back some of the 973 attribute errors that stopped data
    # get a script for the new event each week and append to the data set 
    
    # add more data points to scrape
    ## add total fights in the ufc 
    ## add performance of the night bonus 
    ## add fight of the night bonus 
    ## add total octagon time in the ufc in seconds
    ## consider title fights, title wins or title defenses 
    
    # consider having different models with different groups of this data 



########################################## cobine the below examples to get the rest of the data

    
    {
    # Definition of fighter Data
    "name"  : "fighter name",
    "win"   : "number of wins",
    "loss"  : "number of losses",
    "draw"  : "number of draws",
    "tko"   : "number of wins by TKO",
    "udec"  : "number of wins by unanimous decision",
    "sdec"  : "number of wins by split decision",
    "sub"   : "number of wins by submission",
    "height": "height in inches",
    "weight": "weight in pounds",
    "reach" : "reach in inches",
    "dob"   : "year born 19XX",
    "slpm"  : "strikes landed per minute",
    "strAcc": "percent of strikes landed",
    "sapm"  : "strikes attempted per minute",
    "strDef": "percent of strikes opponet doesnt land ",
    "tdAvg" : "number of takedowns per 15 min",
    "tdAcc" : "percent of takedowns landed",
    "tdDef" : "percent of takedowns stopped",
    "subAvg": "number of submission attempts per 15 min",
    }
    
    
    name = "fighters"
    
    allowed_domains = ["ufcstats.com"]

    #allows us to make small testing batches
    #custom_settings = {'CLOSESPIDER_PAGECOUNT': 100}
    
    start_urls = ['http://www.ufcstats.com/statistics/events/completed?page=all']
    #you can also use a list for the rules instead of a generator
    rules = (
        Rule(LinkExtractor(allow="event-details", deny="fight-details"), callback=None),
        Rule(LinkExtractor(allow="fighter-details", deny="fight-details"), callback="parse_fighter")
    )
        
    # https://stackoverflow.com/questions/50919246/how-to-combine-scrapy-output
    #respons chaining example will need to expand data parameters 

    def parse_fighter(self, response):
            recordData =  response.css("div.l-page__container h2.b-content__title span.b-content__title-record::text").get().strip()
            winData = getWins(recordData)
            lossData = getLoss(recordData)
            drawData = getDraw(recordData)
            results = response.css("div.l-page__container table.b-fight-details__table.b-fight-details__table_style_margin-top.b-fight-details__table_type_event-details.js-fight-table tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click").getall() 
            tko = getTKO(results)
            uDec = getUDEC(results)
            sDec = getSDEC(results)
            subs = getSub(results)
            kd = getKd(response.css("div.l-page__container table.b-fight-details__table.b-fight-details__table_style_margin-top.b-fight-details__table_type_event-details.js-fight-table tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click p").getall())
            heightData = cleanHeightData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[0])
            weightData = cleanWeightData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[1])
            reachData = cleanReachData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[2])
            stanceData = cleanStanceData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[3])
            dobData = cleanDobData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[4])
            slpmData = cleanSlpmData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[5])
            straccData = cleanStraccData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[6])
            sapmData = cleanSapmData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[7])
            strdefData = cleanStrdefData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[8])
            tdavgData = cleanTdavgData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[10])
            tdaccData = cleanTdaccData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[11])
            tddefData = cleanTddefData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[12])
            subavgData = cleanSubavgData(response.css("li.b-list__box-list-item.b-list__box-list-item_type_block").getall()[13])
            # kd = [] below 
            yield {
                    "name":  response.css("div.l-page__container h2.b-content__title span.b-content__title-highlight::text").get().strip(),
                    "win": winData,
                    "loss": lossData,
                    "draw": drawData, 
                    "tko": tko,
                    "udec": uDec,
                    "sdec": sDec,
                    "sub":subs,
                    "kd":kd,
                    "height": heightData,
                    "weight": weightData,
                    "reach": reachData,
                    "stance": stanceData,
                    "dob": dobData ,
                    "slpm":slpmData ,
                    "strAcc":straccData,
                    "sapm": sapmData,
                    "strDef": strdefData,
                    "tdAvg": tdavgData,
                    "tdAcc": tdaccData,
                    "tdDef": tddefData,
                    "subAvg":subavgData,
                }
            
            
def cleanHeightData(input):
    match = re.findall("\d{1,2}", input)
    f = int(match[0])
    i = int(match[1])
    return (f*12 + i)

def cleanWeightData(input):
    match = re.search("\d{1,3}", input).group(0)
    return int(match)

def cleanReachData(input):
   match = re.search("\d{1,2}", input).group(0)
   return int(match)
   
def cleanStanceData(input):
    if re.search("Southpaw", input) is not None:
        match = re.search("Southpaw", input).group(0)
        return match
    if re.search("Orthodox", input) is not None:
        match = re.search("Orthodox", input).group(0)
        return match
    if re.search("Switch", input) is not None:
        match = re.search("Switch", input).group(0)
        return match
    return "N/A"
    
def cleanDobData(input):
    return int(re.search("\d{4}", input).group(0))

def cleanSlpmData(input):
    return float(re.search("\d{1}\D{1}\d{2}", input).group(0))

def cleanStraccData(input):
    percent = re.search("\d{2,3}\D{1}", input).group(0)
    value = re.search("\d{2,3}", percent).group(0)
    percent = "0.{d}".format(d = value)
    return float(percent)

def cleanSapmData(input):
    return float(re.search("\d{1}\D{1}\d{2}", input).group(0))

def cleanStrdefData(input):
    percent = re.search("\d{2,3}\D{1}", input).group(0)
    value = re.search("\d{2,3}", percent).group(0)
    percent = "0.{d}".format(d = value)
    return float(percent)
    
def cleanTdavgData(input):
    return float(re.search("\d{1}\D{1}\d{2}", input).group(0))

def cleanTdaccData(input):
    percent = re.search("\d{2,3}\D{1}", input).group(0)
    value = re.search("\d{2,3}", percent).group(0)
    percent = "0.{d}".format(d = value)
    return float(percent)

def cleanTddefData(input):
    percent = re.search("\d{2,3}\D{1}", input).group(0)
    value = re.search("\d{2,3}", percent).group(0)
    percent = "0.{d}".format(d = value)
    return float(percent)

def cleanSubavgData(input):
    return float(re.search("\d{1}\D{1}\d{1}", input).group(0))

def getWins(input):
    found = re.findall("\d{1,2}", input)
    return int(found[0])

def getLoss(input):
    found = re.findall("\d{1,2}", input)
    return int(found[1])

def getDraw(input):
    found = re.findall("\d{1,2}", input)
    return int(found[2])

def getTKO(results):
    tko = 0
    for item in results:
        if re.search("win", item) is not None:
            if re.search("KO/TKO", item) is not None:
                tko += 1
    return tko

def getSDEC(results):
    sDec = 0
    for item in results:
        if re.search("win", item) is not None:
            if re.search("S-DEC", item) is not None:
                sDec += 1
            elif re.search("M-DEC", item):
                sDec += 1
    return sDec

def getUDEC(results):
    uDec = 0
    for item in results:
        if re.search("win", item) is not None:
            if re.search("U-DEC", item) is not None:
                uDec += 1
    return uDec

def getSub(results):
    sub = 0
    for item in results:
        if re.search("win", item) is not None:
            if re.search("SUB", item) is not None:
                sub += 1
    return sub

def getKd(results):
    # function not connected to yield statement right now
    kd = 0
    r = []
    foundStart = False
    foundFirst = False
    foundSecond = False
    for item in results:       
        if foundStart and foundFirst and foundSecond:
            if re.search("\d", item) is not None:
                #r.append(re.search("\d", item).group(0))
                d = int(re.search("\d", item).group(0))
                kd = kd + d
                foundStart = False
                foundFirst = False
                foundSecond = False
    
        if re.search("win", item) or re.search("loss", item) is not None:
            # might need \b boundries 
           foundStart = True
        
        if foundStart:
            if not foundSecond and foundFirst:
                if re.search("\s+\w+\s{1}\w+", item) is not None:
                    #r.append("foundSecond    " + item)
                    foundSecond = True
            if not foundFirst:
                if re.search("\s+\w+\s{1}\w+", item) is not None:
                    #r.append("foundFirst   " + item)
                    foundFirst = True
    
    return kd