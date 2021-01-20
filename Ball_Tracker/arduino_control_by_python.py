from pyfirmata import ArduinoMega
from pyfirmata import SERVO
from time import sleep
from tkinter import *

board = ArduinoMega('COM20')

board.digital[6].mode = SERVO

pin6 = board.get_pin('d:6:o')

def move_servo(a):
    board.digital[6].write(a)

root = Tk()

scale = Scale(root,
              command=move_servo,
              to=175,
              orient=HORIZONTAL,
              length=400,
              label='Angle')
scale.pack(anchor=CENTER)

root.mainloop()
