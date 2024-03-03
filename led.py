import time
import board
import digitalio

use = True

board = digitalio.DigitalInOut(board.LED)
board.direction = digitalio.Direction.OUTPUT
      
def blink(n, s):
    if use:
        for i in range(n):
            board.value = True
            time.sleep(s)
            board.value = False
            time.sleep(s)