from windows import *
import windows
import time
import curses
from curses.textpad import *
import keyboard
from threading import Thread

            
global stdscr
stdscr = setupWindows()

inputThread = Thread(target = inputLoop)
editSearch()

inputThread.start()

while True:
    time.sleep(1)

curses.endwin()


