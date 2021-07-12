import serial
import tkinter as tk
import config


################################serial setup###################################
ser = serial.Serial('/dev/cu.usbmodem0E22D9A1',baudrate=115200)  # open serial port


#clean up all the single lines of assignment for the lists its messy
def set_absolute_zero(abs_pos, abs_steps, relative_offset,abs_Label):
    """resets the absolute zero position to the postion that the steppers are
    currently at"""
    relative_offset[0] -= abs_pos[0]
    relative_offset[1] -= abs_pos[1]
    abs_pos[0] = 0
    abs_pos[1] = 0
    abs_steps[0] = 0
    abs_steps[1] = 0
    #tkinter below not needed if not using tkinter
    abs_Label.config(text = "%s , %s" %(abs_pos[0],abs_pos[1]))

def set_relative_zero(relative_pos, relative_offset, abs_pos,relative_Label):
    """resets the relative zero poistion to the postion the steppers are currently
    at """
    relative_offset[0] = abs_pos[0]
    relative_offset[1] = abs_pos[1]
    relative_pos[0] = 0
    relative_pos[1] = 0
    #tkinter below not needed if not using tkinter
    relative_Label.config(text = "%s , %s" %(relative_pos[0],relative_pos[1]))

def update_position(direc, step, abs_steps,abs_pos, relative_pos,relative_offset):
    """updates all position variables to their new poistion given the number of
    steps that was moved and the direction it moved"""
    if direc == 'b':
        abs_steps[0]-= step
    if direc == 'f':
        abs_steps[0] += step
    if direc == 'd':
        abs_steps[1] -= step
    if direc == 'u':
        abs_steps[1] += step

    abs_pos[0] = abs_steps[0]*conversion
    abs_pos[1] = abs_steps[1]*conversion
    relative_pos[0] = abs_pos[0]-relative_offset[0]
    relative_pos[1] = abs_pos[1]-relative_offset[1]

def move(direc, step,abs_Label, relative_Label):
    """Takes direc char of u,d,f,b (up, down, forward, backward)
        and step in mm and moves that distance in that direction."""
    ser.write(str.encode('q'))

    machine_step = str(round(step/config.conversion))

    ser.write((str.encode(machine_step)))
    ser.write((str.encode(direc)))
    ch = ser.read()

    if ch == "!":
        print("hit limit. aborting.")
        return -1
    if ch != b'*':
        print(ch)
        print("error error error ERROR")

    update_position(direc, round(step/config.conversion),
                    config.abs_steps,config.abs_pos, config.relative_pos,
                    config.relative_offset)
    #Tkinter below not needed if not using
    abs_Label.config(text = "%.3g , %.3g" %(config.abs_pos[0],config.abs_pos[1]))
    relative_Label.config(text = "%.3g , %.3g" %(config.relative_pos[0],config.relative_pos[1]))

def goTo(x,y,relative_pos,abs_pos):
    """given an x(z) and y position the stepers move to those coordinates in
    terms of the given position relative or absolute can be passed"""

    if(x<relative_pos[0] and abs_pos[0] - abs(relative_pos[0]-x) >= 0):
        if move('b',abs(relative_pos[0]-x)): return -1
    elif(x>relative_pos[0] and abs_pos[0] + abs(relative_pos[0]-x) <= xlim):
        if move('f',abs(relative_pos[0]-x)): return -1
    if(y<relative_pos[1] and abs_pos[1] - abs(relative_pos[1]-y) >= ylim):
        if move('d',abs(relative_pos[1]-y)): return -1
    elif(y>relative_pos[1] and abs_pos[1] + abs(relative_pos[1]-y) <= 0):
        if move('u',abs(relative_pos[1]-y)): return -1

def abs_home(abs_pos):
    """moves the steppers back to the Absolute zero position"""
    if goTo(0,0,abs_pos,abs_pos): return -1

def relative_home(relative_pos,abs_pos):
    """moves the steppers back to the relative home position"""
    if goTo(0,0,relative_pos, abs_pos): return -1

def set_speed(yspeed,xspeed):
    """sets the speed of the stepper drivers(reference driver code)"""
    ser.write((str.encode(str(yspeed))))
    ser.write((str.encode('m')))
    ser.write((str.encode(str(xspeed))))
    ser.write((str.encode('M')))
