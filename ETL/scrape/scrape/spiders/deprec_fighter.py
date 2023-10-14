import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import date
import re

class FighterSpider(CrawlSpider):
    #TODO 
    # expand regex for more complex names like
    ## rafael dos "blank" in current data 
    ## George St "blank" in current data 
    
    # add try catch blocks with and loggers to find out 
    ## how to get back some of the 973 attribute errors that stopped data
    # get a script for the new event each week and append to the data set 
    
    # add more data points to scrape
    ## add total fights in the ufc 
    ## add performance of the night bonus 
    ## add fight of the night bonus 
    ## add total octagon time in the ufc in seconds or rounds
    ## time since last comp
    ## consider title fights, title wins or title defenses 
    ## reversals
    ## knockdowns
    ## win streak 
    ## lose streak
    ## rank velocity?
    ## current rank or highest rank or average rank in the last 2(few) years?
    
    # consider having different models with different groups of this data 
        
    name = "fighterString"
    
    allowed_domains = ["ufcstats.com"]

    #allows us to make small testing batches
    # custom_settings = {'CLOSESPIDER_PAGECOUNT': 100}
    
    start_urls = ['http://www.ufcstats.com/statistics/events/completed?page=all']
    #you can also use a list for the rules instead of a generator
    rules = (
        Rule(LinkExtractor(allow="event-details", deny="fight-details"), callback=None),
        Rule(LinkExtractor(allow="fighter-details", deny="fight-details"), callback="parse_fighter")
    )
    
    def parse_fighter(self, response):
                    
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
            
            yield {
                    "name":  response.css("div.l-page__container h2.b-content__title span.b-content__title-highlight::text").get().strip(),
                    "record": response.css("div.l-page__container h2.b-content__title span.b-content__title-record::text").get().strip(),
                    "height": heightData,
                    "weight": weightData,
                    "reach": reachData,
                    "stance": stanceData,
                    "dob": dobData ,
                    "SLpM":slpmData ,
                    "Str. Acc":straccData,
                    "SApM": sapmData,
                    "Str. Def": strdefData,
                    "TD Avg": tdavgData,
                    "TD Acc": tdaccData,
                    "TD Def": tddefData,
                    "Sub. Avg":subavgData,
                }
            
def cleanHeightData(input):
    match = re.search("\d{1}\D{2}\d{1,2}", input).group(0)
    return match

def cleanWeightData(input):
    match = re.search("\d{1,3}", input).group(0)
    return match

def cleanReachData(input):
   match = re.search("\d{1,2}", input).group(0)
   return match
   
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
    return re.search("\d{4}", input).group(0)

def cleanSlpmData(input):
    return re.search("\d{1}\D{1}\d{2}", input).group(0)

def cleanStraccData(input):
    return re.search("\d{2,3}\D{1}", input).group(0)

def cleanSapmData(input):
    return re.search("\d{1}\D{1}\d{2}", input).group(0)

def cleanStrdefData(input):
    return re.search("\d{2,3}\D{1}", input).group(0)
    
def cleanTdavgData(input):
    return re.search("\d{1}\D{1}\d{2}", input).group(0)    

def cleanTdaccData(input):
    return re.search("\d{2,3}\D{1}", input).group(0)

def cleanTddefData(input):
    return re.search("\d{2,3}\D{1}", input).group(0)

def cleanSubavgData(input):
    return re.search("\d{1}\D{1}\d{1}", input).group(0) 