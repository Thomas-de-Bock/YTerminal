from player import *
import curses
import time
import math

#Character setup: Right-Down corner etc.
RDC = u'\u250C'
LDC = u'\u2510'
RUC = u'\u2514'
LUC = u'\u2518'
Line = u'\u2500'
LineUp = u'\u2502'

rows = -1
cols = -1

def outlineWindow(win, name):
    height, width = win.getmaxyx()
    for y in range(0, height):
        rowstr = ""
        for x in range(0, width-1):
            crntchar = " "
            if y == 0:
                crntchar = Line
                if x > 1 and x <= len(name)+1:
                    crntchar = name[x-2]
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
    progwin.addstr("█" * (progamount-1) + "-"*(cols-progamount-2))
    progwin.refresh()

def getTextWindow(win, isSearch=False):
    sizey, sizex = win.getmaxyx()
    posy, posx = win.getbegyx()
    newTextwin = None
    if isSearch:
        newTextwin = curses.newwin(1, sizex-3, posy, posx+1)
    else:
        newTextwin = curses.newwin(sizey-2, sizex-3, posy+1, posx+1)
    newTextwin.refresh()
    return newTextwin

def setupWindows():
    #Curses setup
    stdscr = curses.initscr()
    stdscr.clear()
    curses.cbreak()
    stdscr.keypad(True)
    global rows, cols
    #Get screen sizes
    rows, cols = stdscr.getmaxyx()

    #Outline windows---------
    #Searchbar setup
    searchwidth = math.floor(cols/2)
    searchwin = curses.newwin(2, searchwidth, 0, int(cols/4))
    outlineWindow(searchwin, "")
    #Main List setup
    if rows < 19:
        mainheight = math.floor(rows/1.3)-2
    else:
        mainheight = rows - 6
    mainwin = curses.newwin(mainheight, searchwidth, 2, math.floor(int(cols/4)))
    outlineWindow(mainwin, "Main")

    #Playlist setup
    playlistwidth = math.floor((cols-searchwidth)/2)
    playlistwin = curses.newwin(mainheight+2, playlistwidth, 0, 0)
    outlineWindow(playlistwin, "Playlist")

    #Queue setup
    queuewin = curses.newwin(math.floor((mainheight+2)/2), cols-searchwidth-playlistwidth+1, 0, int(cols/4) + searchwidth)
    outlineWindow(queuewin, "Queue")

    #ProgressBar setup
    global progwin
    progwin = curses.newwin(1, cols-2, rows-1, 1)
    
    #Text windows----------
    global mainTextwin, playlistTextwin, queueTextwin
    mainTextwin = getTextWindow(mainwin)
    playlistTextwin = getTextWindow(playlistwin)
    queueTextwin = getTextWindow(queuewin)
    global searchTextwin
    searchTextwin = getTextWindow(searchwin, True)

def setMainText(text):
    mainTextwin.addstr(text)
    mainTextwin.refresh()
def setQueueText(text):
    queueTextwin.addstr(text)
    queueTextwin.refresh()
def setPlaylistText(text):
    playlistTextwin.addstr(text)
    playlistTextwin.refresh()
def addSearchChar(char):
    searchTextwin.addstr(char)
    searchTextwin.refresh()
