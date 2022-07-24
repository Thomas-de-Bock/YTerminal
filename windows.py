import curses
from curses.textpad import *
import time
import math
import keyboard
import pyautogui
from player import playFromLink
from searcher import *
from Track import *
from tools import *
from threading import Thread

#Character setup: Right-Down corner etc.
RDC = u'\u250C'
LDC = u'\u2510'
RUC = u'\u2514'
LUC = u'\u2518'
Line = u'\u2500'
LineUp = u'\u2502'

rows = -1
cols = -1

def outlineWindow(win, name, hasName = True):
    height, width = win.getmaxyx()
    for y in range(0, height):
        rowstr = ""
        for x in range(0, width-1):
            crntchar = " "
            if y == 0:
                crntchar = Line
                if x > 1 and x <= len(name)+1 and hasName:
                    crntchar = name[x-2]
                elif x == 1 and hasName or x == len(name)+2 and hasName:
                    crntchar = ' '
                elif x == 0:
                    crntchar = RDC
                elif x == width-2:
                    crntchar = LDC
            elif y == height-1:
                crntchar = Line
                if x == 0:
                    crntchar = RUC
                elif x == width-2:
                    crntchar = LUC
            elif x == 0 or x == width-2:
                    crntchar = LineUp
            rowstr += crntchar
        if y != height-1:
            rowstr += "\n"
        
        win.addstr(rowstr)
    win.refresh()

def setProgbar(perc):
    progamount = math.floor((perc/100)*cols)
    progwin.addstr("█" * (progamount-1) + Line*(cols-progamount-2))
    progwin.refresh()

def getTextWindow(win, isSearch=False):
    sizey, sizex = win.getmaxyx()
    posy, posx = win.getbegyx()
    newTextwin = None
    if isSearch:
        newTextwin = curses.newwin(1, sizex-5, posy, posx+2)
    else:
        newTextwin = curses.newwin(sizey-2, sizex-3, posy+1, posx+1)
    newTextwin.refresh()
    return newTextwin

def setupWindows():
    global currentTrack
    #Curses setup
    global stdscr
    stdscr = curses.initscr()
    stdscr.clear()
    curses.noecho()

    global rows, cols
    #Get screen sizes
    rows, cols = stdscr.getmaxyx()
    
    rows -=1
    cols -=1
    
    #Getting sizes
    searchwidth = math.floor(cols/2)
    playlistwidth = math.floor((cols-searchwidth)/2)
    playlistheight = -1

    if rows < 19:
        playlistheight = math.floor(rows/1.2)
    else:
        playlistheight = rows - 6

    mainheight = math.floor((6*playlistheight/8)-3)+1
    selectedheight = playlistheight - mainheight - 1

    #Outline windows---------
    #Searchbar setup
    searchwin = curses.newwin(2, searchwidth, 0, playlistwidth)
    outlineWindow(searchwin, "")
    #Main List setup
    global mainwin
    global mainTracks
    mainwin = curses.newwin(mainheight, searchwidth, 2, playlistwidth)
    outlineWindow(mainwin, "Main")

    #selectedTrack setup
    global selectedTrack #For track inside window

    global selectedwin
    selectedwin = curses.newwin(selectedheight, searchwidth, 1+mainheight, playlistwidth)
    outlineWindow(selectedwin, "Selected", False)

    #Playlist setup
    playlistwin = curses.newwin(playlistheight, playlistwidth, 0, 0)
    outlineWindow(playlistwin, "Playlist")

    #Queue setup
    queuewin = curses.newwin(playlistheight, cols-searchwidth-playlistwidth, 0, searchwidth+playlistwidth )
    outlineWindow(queuewin, "Queue")

    #ProgressBar setup
    global progwin
    progwin = curses.newwin(1, cols-2, rows-1, 1)
    
    #Text windows----------
    global mainTextwin, playlistTextwin, queueTextwin, selectedTextwin
    mainTextwin = getTextWindow(mainwin)
    playlistTextwin = getTextWindow(playlistwin)
    queueTextwin = getTextWindow(queuewin)
    selectedTextwin = getTextWindow(selectedwin)
    global searchTextwin
    searchTextwin = Textbox(getTextWindow(searchwin, True))
    
    #Enable cursor
    curses.curs_set(1)

    global isEditingSearch
    isEditingSearch = False

    return stdscr

def setMainText(text):
    mainTextwin.clear()
    mainTextwin.addstr(text)

def stopEditSearch():
    pyautogui.keyDown("ctrl")
    pyautogui.press("g")
    pyautogui.keyUp("ctrl")
    global isEditingSearch
    isEditingSearch = False

def setQueueText(text):
    queueTextwin.addstr(text)
    queueTextwin.refresh()

def setPlaylistText(text):
    playlistTextwin.addstr(text)
    playlistTextwin.refresh()

def getWindowElementCount(win):
    return ((Textbox)(win)).gather().count('\n')

def moveSelectionCursor(win, dir):
    posy, posx = win.getyx()
    sizey = getWindowElementCount(win)

    if dir == "up":
        posy -= 1
    elif dir == "down":
        posy += 1

    if posy < 0:
        posy = 0
    elif posy >= sizey-1:
        posy = sizey-1
    #Do twice to place cursor TEMP
    win.move(posy, 0)
    updateSelectedWin()
    win.move(posy, 0)
    win.refresh()


def updateSelectedWin():
    posy, posx = mainTextwin.getyx()
    global selectedTrack
    selectedTrack = mainTracks[posy]
    displaySelectedTrack()

def displaySelectedTrack():
    sizey, sizex = selectedTextwin.getmaxyx()

    selectedTextwin.clear()
    selectedTextwin.addstr(cutString(selectedTrack.title, sizex * 2) + "\n")
    selectedTextwin.addstr(sizey-1, 0,"By: " + cutString(selectedTrack.channel,sizex-5))
    selectedTextwin.refresh()

def editSearch():
    global isEditingSearch
    isEditingSearch = True
    searchThread = Thread(target = searchTextwin.edit)
    searchThread.start()

def doSearch(term):
    resultamount, width = mainTextwin.getmaxyx()
    global mainTracks
    mainTracks = getTracks(term, resultamount)

    setMainText(tracksToString(mainTracks, width-4))

    stopEditSearch()

    mainTextwin.move(0, 0)
    updateSelectedWin()

    #Move cursor to first result
    mainTextwin.move(0, 0)
    mainTextwin.refresh()

def playSelected():
    posy, posx = mainTextwin.getyx()
    global currentTrack
    currentTrack = mainTracks[posy]
    playFromLink(currentTrack.link)

def inputLoop():
    lastwasinput = False
    while True:
        if keyboard.is_pressed('esc'):
            if not lastwasinput:
                if isEditingSearch:
                    doSearch(searchTextwin.gather())
                else:
                    playSelected()
            lastwasinput = True
        elif keyboard.is_pressed('down arrow'):
            if not lastwasinput:
                moveSelectionCursor(mainTextwin, "down")
            lastwasinput = True
        elif keyboard.is_pressed('up arrow'):
            if not lastwasinput:
                moveSelectionCursor(mainTextwin, "up")
            lastwasinput = True
        elif keyboard.is_pressed('f1'):
            if not lastwasinput:
                editSearch()
            lastwasinput = True
        else:
            lastwasinput = False
