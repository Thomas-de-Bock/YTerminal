from player import *
import curses
import time
import math

#playFromLink("https://www.youtube.com/watch?v=nkJqVFmrAZ0")

stdscr = curses.initscr()
stdscr.clear()
curses.cbreak()
stdscr.keypad(True)


searchwin = curses.newwin(2, math.floor(curses.COLS/2), 0, int(curses.COLS/4))
searchwin.addstr(u'\u250C' + "hehe stinkyyyyyyyyy" + "          " + u'\u2510' +"\n")
searchwin.addstr(u'\u2514' + (u'\u2500' * 29) + u'\u2518')

searchwin.refresh()

time.sleep(3)

curses.endwin()

