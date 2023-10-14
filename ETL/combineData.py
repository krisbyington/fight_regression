import os 
import sys
import re
import json
import pandas as pd

#to test json format correctness 
# f = open('modelData.json')
# test = json.load(f)
# print(test)


            #data to add  
            ###### get total fight time for average metric 
            ### head , body ,leg strikes per minute or as total percentage 
            ### distance, clinch, ground strikes per minute or as total 
            ### average controltime per 15 min
            ### knockdowns per 15 min
            ### average time to win 
            ### average controltime which implies octogon time 
            ### number of fights in weight class <--- no 
            ### stance encoded in 1,2,3 <--- probably not useful in regression but worth a singular test later 
            
def getWeightString(weight):
    ###### LOOK INTO PROPER SLITTING 
    try:
        if int(weight) < 125:
            return "Strawweight"
        elif int(weight) >=126 and weight < 135:
            return "Flyweight"
        elif int(weight) >=136 and weight < 145:
            return "Bantamweight"
        elif int(weight) >=146 and weight < 155:
            return "Featherweight"
        elif int(weight) >=156 and weight < 170:
            return "Lightweight"
        elif int(weight) >=171 and weight < 185:
            return "Welterweight"
        elif int(weight) >=186 and weight < 200:
            return "Middleweight"
        elif int(weight) >=201 and weight < 206:
            return "Light Heavyweight"
        elif int(weight) >=206 :
            return "Heavyweight" 
    except:
        print(weight)
            
def winPercent(win, loss, draw):
    #make a percent of wins and feed that in 
    # just changed from 2 -> 3 decimal places 
    return round(win / (win + loss + draw), 3)

def tkoPercent(tko, win, loss, draw):
    return round(tko/ (win + loss + draw), 3)

def udecPercent(udec, win, loss, draw):
    return round(udec/ (win + loss + draw), 3)

def sdecPercent(sdec, win, loss, draw):
    return round(sdec/ (win + loss + draw), 3)

def subPercent(sub, win, loss, draw):
    return round(sub/ (win + loss + draw), 3)

def countWeights(division, data):
        print(len(data[0][0]))
 
    # with open(fileName, 'w') as d:
    #     d.write(json.dumps(dataList[i]))

def makeModelData(division,fighters, bouts):
    data = {}
    combinedData = []
    for bout in bouts:
        found1 = False
        found2 = False
        #  bout["weight"]
        if(bout["division"] == division):
            name1  = bout['name1']
            name2  = bout['name2']
            winner = bout['winner']
            for fighter in fighters:
                if fighter['name'] == name1:
                    fighter1 = fighter
                    found1 = True
                elif fighter['name'] == name2:
                    fighter2 = fighter
                    found2 = True
            if found1 and found2:
                combinedData.append(
                    {
                    "name"    : fighter1["name"],
                    "wins"    : fighter1["wins"],
                    "tko"     : fighter1["tko"],
                    "sub"     : fighter1["sub"],
                    "udec"    : fighter1["udec"],
                    "sdec"    : fighter1["sdec"],
                    "height"  : fighter1["height"],
                    "weight"  : fighter1["weight"],
                    "reach"   : fighter1["reach"],
                    "dob"     : fighter1["dob"],
                    "slpm"    : fighter1["slpm"],
                    "sapm"    : fighter1["sapm"],
                    "strAcc"  : fighter1["strAcc"],
                    "strDef"  : fighter1["strDef"],
                    "hslpm"   : fighter1["hslpm"],
                    "hsapm"   : fighter1["hsapm"],
                    "hstrAcc" : fighter1["hstrAcc"],
                    "bslpm"   : fighter1["bslpm"],
                    "bsapm"   : fighter1["bsapm"],
                    "bstrAcc" : fighter1["bstrAcc"],
                    "lslpm"   : fighter1["lslpm"],
                    "lsapm"   : fighter1["lsapm"],
                    "lstrAcc" : fighter1["lstrAcc"],
                    "dslpm"   : fighter1["dslpm"],
                    "dsapm"   : fighter1["dsapm"],
                    "dstrAcc" : fighter1["dstrAcc"],
                    "cslpm"   : fighter1["cslpm"],
                    "csapm"   : fighter1["csapm"],
                    "cstrAcc" : fighter1["cstrAcc"],
                    "gslpm"   : fighter1["gslpm"],
                    "gsapm"   : fighter1["gsapm"],
                    "gstrAcc" : fighter1["gstrAcc"],
                    "tdAvg"   : fighter1["tdAvg"],
                    "tdAcc"   : fighter1["tdAcc"],
                    "tdDef"   : fighter1["tdDef"],
                    "subAvg"  : fighter1["subAvg"],
                    "ctrlAvg" : fighter1["ctrlAvg"],
                    "name1"   : fighter2["name"],
                    "wins1"   : fighter2["wins"],
                    "tko1"    : fighter2["tko"],
                    "sub1"    : fighter2["sub"],
                    "udec1"   : fighter2["udec"],
                    "sdec1"   : fighter2["sdec"],
                    "height1" : fighter2["height"],
                    "weight1" : fighter2["weight"],
                    "reach1"  : fighter2["reach"],
                    "dob1"    : fighter2["dob"],
                    "slpm1"   : fighter2["slpm"],
                    "sapm1"   : fighter2["sapm"],
                    "strAcc1" : fighter2["strAcc"],
                    "strDef1" : fighter2["strDef"],
                    "hslpm1"  : fighter2["hslpm"],
                    "hsapm1"  : fighter2["hsapm"],
                    "hstrAcc1": fighter2["hstrAcc"],
                    "bslpm1"  : fighter2["bslpm"],
                    "bsapm1"  : fighter2["bsapm"],
                    "bstrAcc1": fighter2["bstrAcc"],
                    "lslpm1"  : fighter2["lslpm"],
                    "lsapm1"  : fighter2["lsapm"],
                    "lstrAcc1": fighter2["lstrAcc"],
                    "dslpm1"  : fighter2["dslpm"],
                    "dsapm1"  : fighter2["dsapm"],
                    "dstrAcc1": fighter2["dstrAcc"],
                    "cslpm1"  : fighter2["cslpm"],
                    "csapm1"  : fighter2["csapm"],
                    "cstrAcc1": fighter2["cstrAcc"],
                    "gslpm1"  : fighter2["gslpm"],
                    "gsapm1"  : fighter2["gsapm"],
                    "gstrAcc1": fighter2["gstrAcc"],
                    "tdAvg1"  : fighter2["tdAvg"],
                    "tdAcc1"  : fighter2["tdAcc"],
                    "tdDef1"  : fighter2["tdDef"],
                    "subAvg1" : fighter2["subAvg"],
                    "ctrlAvg1": fighter2["ctrlAvg"],
                    "winner"  : winner
                    }
                )
    print("length",len(combinedData ))
    data.update({division:combinedData})
    return  data 
    # "name"   : fighter["name"],
    # "wins"   : winPercent(fighter["win"], fighter["loss"], fighter["draw"]),
    # "tko"    : tkoPercent(fighter["tko"], fighter["win"], fighter["loss"], fighter["draw"]),
    # "udec"   : udecPercent(fighter["udec"], fighter["win"], fighter["loss"], fighter["draw"]),
    # "sdec"   : sdecPercent(fighter["sdec"], fighter["win"], fighter["loss"], fighter["draw"]),
    # "sub"    : subPercent(fighter["sub"], fighter["win"], fighter["loss"], fighter["draw"]),
    # "height" : fighter["height"],
    # "reach"  : fighter["reach"],
    # "dob"    : fighter["dob"],
    # "slpm"   : fighter["slpm"],
    # "strAcc" : fighter["strAcc"],
    # "sapm"   : fighter["sapm"],
    # "strDef" : fighter["strDef"],
    # "tdAvg"  : fighter["tdAvg"],
    # "tdAcc"  : fighter["tdAcc"],
    # "tdDef"  : fighter["tdDef"],
    # "subAvg" : fighter["subAvg"],
    # "name1"  : fighter2["name"],
    # "wins1"  : winPercent(fighter2["win"], fighter2["loss"], fighter2["draw"]),
    # "tko1"   : tkoPercent(fighter2["tko"], fighter2["win"], fighter2["loss"], fighter2["draw"]),
    # "udec1"  : udecPercent(fighter2["udec"], fighter2["win"], fighter2["loss"], fighter2["draw"]),
    # "sdec1"  : sdecPercent(fighter2["sdec"], fighter2["win"], fighter2["loss"], fighter2["draw"]),
    # "sub1"   : subPercent(fighter2["sub"], fighter2["win"], fighter2["loss"], fighter2["draw"]),
    # "height1": fighter2["height"],
    # "reach1" : fighter2["reach"],
    # "dob1"   : fighter2["dob"],
    # "slpm1"  : fighter2["slpm"],
    # "sapm1"  : fighter2["sapm"],
    # "strAcc1": fighter2["strAcc"],
    # "strDef1": fighter2["strDef"],
    # "tdAvg1" : fighter2["tdAvg"],
    # "tdAcc1" : fighter2["tdAcc"],
    # "tdDef1" : fighter2["tdDef"],
    # "subAvg1": fighter2["subAvg"],
    # "winner" : winner
        
def makePredictData(division,fighters):
    data = {}
    combinedData = []
    for fighter in fighters:
                                #was weight 
        if(getWeightString(fighter["weight"]) == division):
            # combinedData.append(
            #     {
            #         "name"   : fighter["name"],
            #         "wins"   : winPercent(fighter["win"], fighter["loss"], fighter["draw"]),
            #         "tko"    : tkoPercent(fighter["tko"], fighter["win"], fighter["loss"], fighter["draw"]),
            #         "udec"   : udecPercent(fighter["udec"], fighter["win"], fighter["loss"], fighter["draw"]),
            #         "sdec"   : sdecPercent(fighter["sdec"], fighter["win"], fighter["loss"], fighter["draw"]),
            #         "sub"    : subPercent(fighter["sub"], fighter["win"], fighter["loss"], fighter["draw"]),
            #         "height" : fighter["height"],
            #         "reach"  : fighter["reach"],
            #         "dob"    : fighter["dob"],
            #         "slpm"   : fighter["slpm"],
            #         "strAcc" : fighter["strAcc"],
            #         "sapm"   : fighter["sapm"],
            #         "strDef" : fighter["strDef"],
            #         "tdAvg"  : fighter["tdAvg"],
            #         "tdAcc"  : fighter["tdAcc"],
            #         "tdDef"  : fighter["tdDef"],
            #         "subAvg" : fighter["subAvg"],
            #     }
            # )
            combinedData.append({
                    "name"   : fighter["name"],
                    "wins"   : fighter["wins"],
                    "tko"    : fighter["tko"],
                    "sub"    : fighter["sub"],
                    "udec"   : fighter["udec"],
                    "sdec"   : fighter["sdec"],
                    "height" : fighter["height"],
                    "weight" : fighter["weight"],
                    "reach"  : fighter["reach"],
                    "dob"    : fighter["dob"],
                    "slpm"   : fighter["slpm"],
                    "sapm"   : fighter["sapm"],
                    "strAcc" : fighter["strAcc"],
                    "strDef" : fighter["strDef"],
                    "hslpm"  : fighter["hslpm"],
                    "hsapm"  : fighter["hsapm"],
                    "hstrAcc": fighter["hstrAcc"],
                    "bslpm"  : fighter["bslpm"],
                    "bsapm"  : fighter["bsapm"],
                    "bstrAcc": fighter["bstrAcc"],
                    "lslpm"  : fighter["lslpm"],
                    "lsapm"  : fighter["lsapm"],
                    "lstrAcc": fighter["lstrAcc"],
                    "dslpm"  : fighter["dslpm"],
                    "dsapm"  : fighter["dsapm"],
                    "dstrAcc": fighter["dstrAcc"],
                    "cslpm"  : fighter["cslpm"],
                    "csapm"  : fighter["csapm"],
                    "cstrAcc": fighter["cstrAcc"],
                    "gslpm"  : fighter["gslpm"],
                    "gsapm"  : fighter["gsapm"],
                    "gstrAcc": fighter["gstrAcc"],
                    "tdAvg"  : fighter["tdAvg"],
                    "tdAcc"  : fighter["tdAcc"],
                    "tdDef"  : fighter["tdDef"],
                    "subAvg" : fighter["subAvg"],
                    "ctrlAvg" : fighter["ctrlAvg"]
                })
    print("length", len(combinedData ))
    data.update({division:combinedData})
    return  data   

def saveWeightClasses(classList, dataList, modelData):
    # need to make macine agnostic slashes. 
    if len(classList) != len(dataList):
        ### should this be a try/except? 
        print("error saving all weight classes: check list lengths")
        sys.exit("class and data list not equal")
    if(modelData):
        for i in range(0, len(classList)):
            #remember to change data1 -> data2 if not compatable anymore
            fileName = os.path.join(os.path.expanduser("modelData"),classList[i] + "Data1.json")
            print(fileName)
            with open(fileName, 'w') as d:
                d.write(json.dumps(dataList[i]))
    else:
        temp = []
        dump = []
        for i in range(0, 3):
            if i == 0:
                temp.append(dataList[i]["Strawweight"])
            if i == 1:
                temp.append(dataList[i]["Flyweight"])
            if i == 2: 
                temp.append(dataList[i]["Bantamweight"])
                dump = mergeLists(temp)
                # run a for loop to combine into one list 
                
                fileName = os.path.join(os.path.expanduser("predictData") ,"ST-FL-B-" + "Data1.json")
                print(fileName)
                with open(fileName, 'w') as d:
                    d.write(json.dumps(dump))
        temp = []
        dump = []
        for i in range(3,5):
            if i == 3:
                temp.append(dataList[i]["Featherweight"])
            if i == 4:
                temp.append(dataList[i]["Lightweight"])
                dump = mergeLists(temp)
                
                fileName = os.path.join(os.path.expanduser("predictData") ,"F-L-" + "Data1.json")
                print(fileName)
                with open(fileName, 'w') as d:
                    d.write(json.dumps(dump))
        temp = []
        dump = []
        for i in range(5,7):
            if i == 5:
                temp.append(dataList[i]["Welterweight"])
            if i == 6:
                temp.append(dataList[i]["Middleweight"])
                dump = mergeLists(temp)
                fileName = os.path.join(os.path.expanduser("predictData") ,"W-M-" + "Data1.json")
                print(fileName)
                with open(fileName, 'w') as d:
                    d.write(json.dumps(dump))
        temp = []
        dump = []
        for i in range(7, 9):
            if i == 7:
                temp.append(dataList[i]["Light Heavyweight"])
            if i == 8:
                temp.append(dataList[i]["Heavyweight"])
                dump = mergeLists(temp)
                fileName = os.path.join(os.path.expanduser("predictData") ,"LH-H-" + "Data1.json")
                print(fileName)
                with open(fileName, 'w') as d:
                    d.write(json.dumps(dump))
                
    return

def mergeLists(list):
    result = []
    for item in list:
        for ob in item:
            result.append(ob)
    return result

def makePredictAll(fighters,divisions):
    temp = []
    dump = []
    for i in range(0,9):
        if i == 0:
             temp.append(dataList[i]["Strawweight"])
        if i == 1:
            temp.append(dataList[i]["Flyweight"])
        if i == 2: 
            temp.append(dataList[i]["Bantamweight"])
        if i == 3:
            temp.append(dataList[i]["Featherweight"])
        if i == 4:
            temp.append(dataList[i]["Lightweight"])
        if i == 5:
            temp.append(dataList[i]["Welterweight"])
        if i == 6:
            temp.append(dataList[i]["Middleweight"])
        if i == 7:
            temp.append(dataList[i]["Light Heavyweight"])
        if i == 8:
            temp.append(dataList[i]["Heavyweight"])    
            dump = mergeLists(temp)
            
            fileName = os.path.join(os.path.expanduser("predictAll"), "Data1.json")
            print(fileName)
            with open(fileName, 'w') as d:
                d.write(json.dumps(dump))

def prepFighterData(fighters, bouts):
    # returns a list of complete and a list of incomplete data 
    fail = []
    success = []
    final = []
    b = []
    i = 0
    for fighter in fighters:
        # i += 1
        # if i == 30:
        #     break
        #make list of bouts 
        # use list over and over for each metric 
        # populate a bigger fighter object 
        # append new fighter object onto list 
        # return one giane list of objects
        f = fighter
        fail = []
        b = []
        b.append(f)
        for bout in bouts:
            if fighter["name"].strip() == bout["name1"].strip() or fighter["name"].strip() == bout["name2"].strip():
                if fighter["name"].strip() == bout["name1"].strip():
                    b.append(bout)
                elif fighter["name"].strip() == bout["name2"].strip():
                    b.append(bout)
        if len(b) == 1:
            fail.append(fighter)
        else:
            success.append(b)

    for item in success:
        # probably dont need to declare these
        name = ""
        totalTime = 0
        ctrlTime = 0
        headLand = 0
        headApmt = 0
        bodyLand = 0
        bodyApmt = 0
        legLand = 0 
        legAmpt = 0
        distanceLand = 0
        distanceAmpt = 0
        clinchLand = 0 
        clinchAmpt = 0
        groundLand = 0 
        groundAmpt = 0
        i = 0
        which = ""
        for data in item:
            if i == 0:
                #should be for loop on data.keys 
                #dmaking a new dictionary
                name   = data["name"]
                height = data["height"]
                weight = data["weight"]
                reach  = data["reach"]
                dob    = data["dob"]
                slpm   = data["slpm"]
                sapm   = data["sapm"]
                strAcc = data["strAcc"]
                strDef = data["strDef"]
                tdAvg  = data["tdAvg"]
                tdAcc  = data["tdAcc"]
                tdDef  = data["tdDef"]
                subAvg = data["subAvg"]
                win    = data["win"]
                loss   = data["loss"]
                draw   = data["draw"]
                tko    = data["tko"]  
                sub    = data["sub"]
                udec   = data["udec"]
                sdec   = data["sdec"]
                
                
            #skip first item
            # gather all metrics from other items
            # which = ""
            if i > 0:
                if i == 1:
                    if name == data["name1"]:
                        which = "1"
                    if name == data["name2"]:
                        which = "2"
                totalTime += data["duration"]
                ctrlTime += data["ctrl" + which]
                headLand += data["headLand" + which]
                headApmt += data["headAmpt" + which]
                bodyLand += data["bodyLand" + which]
                bodyApmt += data["bodyAmpt" + which]
                legLand += data["legLand" + which]
                legAmpt += data["legAmpt" + which]
                distanceLand += data["distanceLand" + which]
                distanceAmpt += data["distanceAmpt" + which]
                clinchLand += data["clinchLand" + which]
                clinchAmpt += data["clinchAmpt" + which]
                groundLand += data["groundLand" + which]
                groundAmpt += data["groundAmpt" + which]
            i += 1
        final.append({
                    "name"   : name,
                    "wins"   : winPercent(win, loss, draw),
                    "tko"    : tkoPercent(tko, win, loss, draw),
                    "sub"    : subPercent(sub, win, loss, draw),
                    "udec"   : udecPercent(udec, win, loss, draw),
                    "sdec"   : sdecPercent(sdec, win, loss, draw),
                    "height" : height,
                    "weight"   : weight,
                    "reach"  : reach,
                    "dob"    : dob,
                    "slpm"   : slpm,
                    "sapm"   : sapm,
                    "strAcc" : strAcc,
                    "strDef" : strDef,
                    "hslpm"  : getPerMin(headLand, totalTime),
                    "hsapm"  : getPerMin(headLand, totalTime),
                    "hstrAcc": getPerCent(headLand, headLand + headApmt),
                    "bslpm"  : getPerMin(bodyLand, totalTime),
                    "bsapm"  : getPerMin(bodyLand, totalTime),
                    "bstrAcc": getPerCent(bodyLand, bodyLand + bodyApmt),
                    "lslpm"  : getPerMin(legLand, totalTime),
                    "lsapm"  : getPerMin(legLand, totalTime),
                    "lstrAcc": getPerCent(legLand, legLand + legAmpt),
                    "dslpm"  : getPerMin(distanceLand, totalTime),
                    "dsapm"  : getPerMin(distanceLand, totalTime),
                    "dstrAcc": getPerCent(distanceLand, distanceLand + distanceAmpt),
                    "cslpm"  : getPerMin(clinchLand, totalTime),
                    "csapm"  : getPerMin(clinchLand,totalTime),
                    "cstrAcc": getPerCent(clinchLand, clinchLand + clinchAmpt),
                    "gslpm"  : getPerMin(groundLand, totalTime),
                    "gsapm"  : getPerMin(groundLand, totalTime),
                    "gstrAcc": getPerCent(groundLand, groundLand + groundAmpt),
                    "tdAvg"  : tdAvg,
                    "tdAcc"  : tdAcc,
                    "tdDef"   : tdDef,
                    "subAvg"  : subAvg,
                    "ctrlAvg" : getCtrlPerFight(ctrlTime, totalTime)
                })
        
        # update the fighter object
        # append to final 
    return final


def getPerMin(value, time):
    if time == 0:
        return 0
    return round(value/(time/60), 3)

def getPerFight(value, time):
    if time == 0:
        return 0
    return round(value/(time/(60 * 15)), 3)

def getPerCent(value,total):
    if total == 0:
        return 0
    return round( (value/total) , 3)

def getCtrlPerFight(value, time):
    if time == 0:
        return 0
    return round(value/(time/(60* 15)), 0)




    
# finishedData = {}
# name1 = str()
# name2 = str()
# winner   = str()

##########labels for storage
input = {
        "straw":0,
        "fly":0,
        "bantam":0,
        "feather":0,
        "light":0,
        "welter":0,
        "middle":0,
        "lightHeavy":0,
        "heavy":0
        }

divisions = [
             "Strawweight", 
             "Flyweight", 
             "Bantamweight", 
             "Featherweight",
             "Lightweight",
             "Welterweight",
             "Middleweight",
             "Light Heavyweight",
             "Heavyweight"
             ]

##### Control Panel #######################################
firstClean = False # first for a new batch

modelData = False
predictData = False
predictAllData = False
# make a split labeled by parameter numbers 32 or 64 or whatev
# then make it so that you use the newer one
# I still want to finish getting a sample from the first model 
# the real world sample costs actual weeks to ripen 
# you can put this switch inside predict data it has the same purpose 
dataList = []
if(firstClean):
    # populates all parameters on the fighter data  
    with open(os.path.join(os.path.expanduser("scrape"), "fighters.json"), 'r') as d:
        fighters = json.load(d) 

    with open(os.path.join(os.path.expanduser("scrape"), "fights.json"), 'r') as d:
        bouts = json.load(d) 

    fin = prepFighterData(fighters, bouts) 
    print(len(fin))
    with open(os.path.expanduser("calculated_fighters.json"), 'w') as d:
        d.write(json.dumps(fin))

if(modelData):
    #makes training data for weight model
    # reression has function to combine for large training 
    # regression has function to combine for weight grouping 
    # ALL training data derived from this
    with open(os.path.expanduser("calculated_fighters.json"), 'r') as d:
        fighters = json.load(d) 

    with open(os.path.join(os.path.expanduser("scrape"), "fights.json"), 'r') as d:
        bouts = json.load(d) 
        
    for div in divisions:
        dataList.append(makeModelData(div, fighters, bouts))
    saveWeightClasses(divisions, dataList, modelData)

if(predictData):
    # I think its weightModel predict data 
    with open(os.path.expanduser("calculated_fighters.json"), 'r') as d:
        fighters = json.load(d) 

    with open(os.path.join(os.path.expanduser("scrape"), "fights.json"), 'r')as d:
        bouts = json.load(d) 
        
    for div in divisions:
        dataList.append(makePredictData(div, fighters))
    saveWeightClasses(divisions, dataList, modelData)
    
if(predictAllData):
    # I think its LargeModel predict data
    with open(os.path.expanduser("calculated_fighters.json"), 'r') as d:
        fighters = json.load(d) 

    with open(os.path.join(os.path.expanduser("scrape"), "fights.json"), 'r') as d:
        bouts = json.load(d) 
        
    for div in divisions:
        dataList.append(makePredictData(div, fighters))
    # change this to savePredicAll
    makePredictAll(fighters, divisions)

sys.exit()           

