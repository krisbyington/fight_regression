import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import date
import re
import random

class FighterSpider(CrawlSpider):
    #TODO 
    #capture as many bouts as possible. 
    # tweak rules so that is crawls better 
    ## I think I am grabbing a single fight per even right now
        
    name = "bout"
    
    allowed_domains = ["ufcstats.com"]

    #allows us to make small testing batches
    # custom_settings = {'CLOSESPIDER_PAGECOUNT': 100}
    
    start_urls = ['http://www.ufcstats.com/statistics/events/completed?page=all']
    #you can also use a list for the rules instead of a generator
    
    rules = (
        Rule(LinkExtractor(allow="event-details", deny=("fight-details","fighter-details")), callback="parse_bout"),
    )
    
    def parse_bout(self, response):
            allRows = getBouts(response.css("div.l-page__container table.b-fight-details__table.b-fight-details__table_style_margin-top.b-fight-details__table_type_event-details tr p").getall())
            # first  = getFirst(response.css("div.l-page__container table.b-fight-details__table.b-fight-details__table_style_margin-top.b-fight-details__table_type_event-details tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click td.b-fight-details__table-col.l-page_align_left").get())
            # second = getSecond(response.css("div.l-page__container table.b-fight-details__table.b-fight-details__table_style_margin-top.b-fight-details__table_type_event-details tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click td.b-fight-details__table-col.l-page_align_left").get())
            # winner = getWinner(response.css("div.l-page__container table.b-fight-details__table.b-fight-details__table_style_margin-top.b-fight-details__table_type_event-details tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click td.b-fight-details__table-col.b-fight-details__table-col_style_align-top").get(), first)

            for row in allRows:
                if random.random() <= 0.5:
                    first = row["fighter1"]
                    second = row["fighter2"]
                    winner = 0
                else:
                    second = row["fighter1"]
                    first = row["fighter2"]
                    winner = 1
                weight = row["weight"]
                
                yield {
                    "fighter1": first.strip(),
                    "fighter2": second.strip(),
                    "winner"  : winner,
                    "weight"  : weight
                }
                    
            
def getFirst(input):
    found = re.findall("\s+\w+\s{1}\w+", input)
    return found[0].strip()

def getSecond(input):
    found = re.findall("\s+\w+\s{1}\w+", input)
    return found[1].strip()

def getWinner(input, winner):
    win = re.findall("win", input)
    if win[0] is not None :
        return winner
    else: 
        return "none"
    
def getWeight(input):
    return input

def getBouts(input):
    fighter1 = ""
    fighter2 = ""
    weight = ""
    data = []
    i = 0
    for tr in input:
        if i == 1:
            fighter1 = tr
        if i == 2:
            fighter2 = tr
        if i == 11: 
            weight = tr 
            fighter1 = re.findall("\s+\w+\s{1}\w+", fighter1)[0]
            fighter2 = re.findall("\s+\w+\s{1}\w+", fighter2)[0]
            # fighter1 = re.findall("<a.*?>(\s+\w+\s{1}\w+\s+)<\/a>", fighter1)[0]
            # fighter2 = re.findall("<a.*?>(\s+\w+\s{1}\w+\s+)<\/a>", fighter2)[0]
            weight = re.findall("Strawweight|Flyweight|Bantamweight|Featherweight|Lightweight|Welterweight|Middleweight|Light\s{1}Heavyweight|Heavyweight", weight)[0]
            data.append({
            "fighter1": fighter1,
            "fighter2": fighter2,
            "weight": weight
            }) 
        if i == 16:
            i = 0
        i = i + 1                    
    return data           
        
    

