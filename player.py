from pytube import YouTube
import os
from playsound import playsound
from threading import Thread

def getItag(vid):
    audiostreamstr = str(vid.streams.filter(only_audio=True))
    itagindex = audiostreamstr.find("itag")
    itagstr = ""
    for i in range(itagindex+6, len(audiostreamstr)):
        if audiostreamstr[i] == '"':
            break
        else:
            itagstr += audiostreamstr[i]
    return itagstr

def getVid(link):
    return YouTube(link)

def getAudioPath(vid):
    vid.streams.get_by_itag(int(getItag(vid))).download(trackpath, vid.title)
    return trackpath+"/"+vid.title

def playFromLink(link):
    mainpath = os.path.dirname(os.path.realpath(__file__))
    global trackpath
    trackpath = mainpath+"/Temp"
    try:
        os.mkdir(trackpath) 
    except:
        pass

    track = getVid(link)
    currenttrack = getAudioPath(track)

    musicThread = Thread(target = playsound, args=(currenttrack, ))
    musicThread.start()

    #playsound(currenttrack)
