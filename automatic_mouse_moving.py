import pyautogui as pg
import random
import time

while True:
    x = random.randint(600, 700)
    y = random.randint(200, 600)
    pg.moveTo(x, y, 0.5)
    time.sleep(2)
