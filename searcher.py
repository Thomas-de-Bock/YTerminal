
from youtubesearchpython import VideosSearch
import json
from Track import *
from tools import cutString

def getTracks(name, amount):
    results = str(VideosSearch(name, limit = amount).result())
    tracktitles = getTitleFromJSON(results, amount)
    tracklinks = getLinkFromJSON(results, amount)
    trackchannels = getKeyFromJSON(results, amount, "'name'")
    trackchannellinks = getChannelLinkFromJSON(results, amount)

    #In the case that results are less that desired
    trackamount = len(tracklinks)
    tracks = [None] * trackamount
    
    for i in range(0, trackamount):
        tracks[i] = Track(tracktitles[i], tracklinks[i], trackchannels[i], trackchannellinks[i])

    return tracks

def tracksToString(tracks, width):
    result = ""
    for i in range(0, len(tracks)):
        if len(tracks[i].title) > width:
            result += cutString(tracks[i].title, width)
        else:
            result += tracks[i].title
        if i < len(tracks)-1:
            result += "\n"
    return result

def getTitleFromJSON(data, amount, key = "'title'"):
    locs = [i for i in range(len(data)) if data.startswith(key, i)]
    
    #Because amount of results might be less that desired
    if amount > int(len(locs)/2):
        amount = int(len(locs)/2)
    result = [None] * amount
    
    for a in range(0, amount*2, 2):
        value = getValAtIndex(locs[a], key, data)
        result[int(a/2)] = value

    return result

def getKeyFromJSON(data, amount, key):
    locs = [i for i in range(len(data)) if data.startswith(key, i)]
    
    #Because amount of results might be less that desired
    if amount > int(len(locs)):
        amount = int(len(locs))
    result = [None] * amount
    
    for a in range(0, amount):
        value = getValAtIndex(locs[a], key, data)
        result[a] = value

    return result

def getLinkFromJSON(data, amount, key = "'link'"):
    locs = [i for i in range(len(data)) if data.startswith(key, i)]
    
    #Because amount of results might be less that desired
    if amount > int(len(locs)/2):
        amount = int(len(locs)/2)
    result = [None] * amount
    
    for a in range(1, amount*2, 2):
        value = getValAtIndex(locs[a], key, data)
        result[int((a-1)/2)] = value

    return result

def getChannelLinkFromJSON(data, amount, key = "'link'"):
    locs = [i for i in range(len(data)) if data.startswith(key, i)]
    
    #Because amount of results might be less that desired
    if amount > int(len(locs)/2):
        amount = int(len(locs)/2)
    result = [None] * amount
    
    for a in range(0, amount*2, 2):
        value = getValAtIndex(locs[a], key, data)
        result[int(a/2)] = value

    return result

def getValAtIndex(index, key, data):
    value = ""
    for i in range(index+len(key)+3, len(data)):
        if data[i] == "'" and data[i+1] == "," or data[i] == '"' and data[i+1] == "," :
            break
        value+=data[i]
    return value

