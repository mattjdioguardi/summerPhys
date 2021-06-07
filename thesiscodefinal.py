
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 09:28:38 2020

@author: Lily Brackett
"""

import pyvisa
import serial
import tkinter as tk
from tkinter import ttk
import xlsxwriter
import matplotlib.pyplot as plt
import time
from multiprocessing import Process, Lock

import u6



##############################u6 setup##########################################
d = u6.U6()
# For applying the proper calibration to readings.
d.getCalibrationData()
print("Configuring U6 stream")
d.streamConfig(NumChannels=3, ChannelNumbers=[0, 1, 2], ChannelOptions=[0, 0, 0],
               SettlingFactor=1, ResolutionIndex=1, ScanFrequency=5)


###############################Keithley Set Up#####################################
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB0::16::INSTR')
print(inst.query("*IDN?"))
inst.write("SENS:FUNC 'VOLT:DC' ")
inst.write("SENS:VOLT:DC:RANG:AUTO ON ")
inst.write("SENS:VOLT:NPLC 5")		#integration time in PLCs, 1 PLC= 1power line cycle =1/60 sec
inst.write("SENS:VOLT:DC:AVER:COUN 6")


###########################Global Values################################

#universal information
limit_b = 10000
limit_f = 10000
limit_u = 10000
limit_d = 10000

num_run = 1

#absolute position program will initially generate (in mm)
abs_posx = 0
abs_posy = 0

#
stepy = 2

#
run_data = []

#
user_posx = 0
user_posy = 0

#where initial user zero is located in relation to absolute zero (in mm)
user_offx = 0 #modified based on the results of the horizontal data
user_offy = 0

##############################GUI Calibration Functions##################################

#establish the GUI window
win = tk.Tk()

win.title("3D Mapper")

#limits coded in mm
def set_limits():


    global abs_posx
    global abs_posy
    abs_posx = 0
    abs_posy = 0

    global user_posx
    global user_posy
    user_posx = 0
    user_posy = 0

    print("The current position is", user_posx, ',', user_posy)
    global limit_b
    global limit_f
    global limit_u
    global limit_d

    limit_b = 0
    limit_f = 400
    limit_u = 240
    limit_d = 0


def set_abs_zero():
    set_limits()


def go_to_abs_zero():
    if (move_to_start('x', 0)== True) and (move_to_start('y', 0)==True):
        print_position()

def set_user_zero():
    global user_posx
    global user_posy
    user_posx = 0
    user_posy = 0

    print("The current position is", user_posx, ',', user_posy)
    print('\n')

def go_to_user_zero():
    if(move_to_start('y', user_offy)==True) and (move_to_start('x', user_offx) == True):
        set_user_zero()


def adjust_user_zero_x():
    global user_offx
    adjustx = int(entry10.get())
    user_offx += adjustx

    if (move_to_start('x', user_offx)== True):

        print('User start in the x direction has been updated by', adjustx)
        print('\n')
        set_user_zero()
        print_abs_position()
    else:
        user_offx -= adjustx


def adjust_user_zero_y():
    global user_offy
    adjusty = int(entry11.get())
    user_offy += adjusty

    if (move_to_start('y', user_offy)== True):

            print('User start in the y direction has been updated by', adjusty)
            print('\n')
            set_user_zero()
            print_abs_position()
    else:
        user_offy -= adjusty


def print_position():

    print("The current position is", user_posx, ',', user_posy)
    print('\n')

def print_abs_position():

    print("The current absolute position is", abs_posx, ',', abs_posy)
    print('\n')

def print_user_position():

    print("The current user offset is", user_offx, ',', user_offy)
    print('\n')

def get_jump():

    movex = int(jumpx.get())
    movey = int(jumpy.get())
    move_to_start('x', movex)
    move_to_start('y', movey)
    print_position()

def point_click():
        Bdata = [[], [], []]
        Btext = make_Bdata(Bdata)
        Bx = split_Bdata(Btext,0)
        By = split_Bdata(Btext, 1)
        Bz = split_Bdata(Btext,2)

        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Current Bfield")

        ttk.Label(popupBonusWindow, text='Bx = ').grid(row=0, column= 0)
        ttk.Label(popupBonusWindow, text=(Bx, "Gauss")).grid(row=0, column= 6)

        ttk.Label(popupBonusWindow, text='By = ').grid(row=4, column= 0)
        ttk.Label(popupBonusWindow, text=(By, "Gauss")).grid(row=4, column= 6)

        ttk.Label(popupBonusWindow, text='Bz = ').grid(row=8, column= 0)
        ttk.Label(popupBonusWindow, text=(Bz, "Gauss")).grid(row=8, column= 6)

def get_abs_location():

        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Absolute Location")
        ttk.Label(popupBonusWindow, text='The absolute location is currently').grid(row=0, column= 0)
        ttk.Label(popupBonusWindow, text=('(', abs_posx,',', abs_posy,')')).grid(row=0, column= 4)

##############################GUI Calibration Display ##########################

#Absolute Calibration
ttk.Label(win, text="Absolute Zero").grid(column=0,row=4)
ttk.Button(win, text="Set Absolute Zero", command=set_abs_zero).grid(column=0, row=8)

ttk.Label(win, text="Go to Absolute Zero").grid(column=0,row=12)
ttk.Button(win, text="Go", command=go_to_abs_zero).grid(column=0, row=16)

ttk.Label(win, text="Get Absolute Location").grid(column=0,row=20)
ttk.Button(win, text="Return Location", command=get_abs_location).grid(column=0, row = 24)

ttk.Label(win, text="Jump to absolute location").grid(column=0,row=28)

ttk.Label(win, text="x position (mm):").grid(column=0,row=32)
jumpx = tk.Entry (win)
jumpx.grid(column=0,row=36, sticky=tk.W)

ttk.Label(win, text="y position (mm):").grid(column=0,row=40)
jumpy = tk.Entry (win)
jumpy.grid(column=0,row=44, sticky=tk.W)

ttk.Button(win, text="Jump", command=get_jump).grid(column=0, row=48)



#User Calibration
ttk.Label(win, text="Go to User Zero").grid(column=4,row=4)
ttk.Button(win, text="Go", command=go_to_user_zero).grid(column=4, row=8)

ttk.Label(win, text="x adjust user zero").grid(column=4,row=12)
entry10 = tk.Entry (win)
entry10.grid(column=4,row=16, sticky=tk.W)
ttk.Button(win, text="Go", command=adjust_user_zero_x).grid(column=4, row=20)

ttk.Label(win, text="y adjust user zero:").grid(column=4,row=24)
entry11 = tk.Entry (win)
entry11.grid(column=4,row=28, sticky=tk.W)
ttk.Button(win, text="Go", command=adjust_user_zero_y).grid(column=4, row=32)




#Get Field at Point
ttk.Label(win, text="Field at Current Location").grid(column=4,row=36)
ttk.Button(win, text="Get B Field", command=point_click).grid(column=4, row=40)



#########################GUI Mapping Functions#############################


def horizontal_click():

    orientation = 'x'
    xstart= int(entry4.get())
    xstop = int(entry5.get())
    step= int(entry6.get())
    xstart += user_offx
    xstop += user_offx

    dirx_i = set_dir(xstart, orientation)
    dirx_f = set_dir(xstop, orientation)

    initial = set_move(xstart, orientation)
    final = set_move(xstop, orientation)

    delta = final - initial
    if (step == 0) or (step < 0):
        print('Enter positive, nonzero step')

    elif multiple(delta, step) == False:
        print("that's not divisible")

    elif limits_fit(initial, dirx_i) == True and limits_fit(final, dirx_f) == True:


        initialx = abs_posx


        move_to_start(orientation, xstart)

        delta_direc = find_delta_direc(xstart, xstop, dirx_i, orientation)
        initialize_line(xstart, xstop, delta_direc, step)
        move_to_initial(orientation, xstop, initialx)
        print_position()
    else:
        print('out of bounds')



def vertical_click():

    orientation = 'y'
    ystart= int(entry7.get())
    ystop = int(entry8.get())
    step= int(entry9.get())
    ystart += user_offy
    ystop += user_offy

    diry_i = set_dir(ystart, orientation)
    diry_f = set_dir(ystop, orientation)

    initial = set_move(ystart, orientation)
    final = set_move(ystop, orientation)
    delta = final - initial

    if (step == 0) or (step < 0):
        print('Enter positive, nonzero step')

    elif multiple(delta, step) == False:
        print("that's not divisible")

    elif limits_fit(initial, diry_i) == True and limits_fit(final, diry_f) == True:

        initialy = abs_posy
        move_to_start(orientation, ystart)

        delta_direc = find_delta_direc(ystart, ystop, diry_i, orientation)
        initialize_line(ystart, ystop, delta_direc, step)
        move_to_initial(orientation, ystop, initialy)
        print_position()


    else:
        print('out of bounds')


#########################GUI Mapping Display#############################

#make lables
ttk.Label(win, text="Horizontal map").grid(column=12,row=4)
ttk.Label(win, text="Vertical map").grid(column=16,row=4)

#make entry windows
ttk.Label(win, text="x start position (mm):").grid(column=12,row=8)
entry4 = tk.Entry (win)
entry4.grid(column=12,row=12, sticky=tk.W)

ttk.Label(win, text="x final position (mm):").grid(column=12,row=16)
entry5 = tk.Entry (win)
entry5.grid(column=12,row=20, sticky=tk.W)

ttk.Label(win, text="step distance (mm) :").grid(column=12,row=24)
entry6 = tk.Entry (win)
entry6.grid(column=12,row=28, sticky=tk.W)

ttk.Label(win, text="y start position (mm):").grid(column=16,row=8)
entry7 = tk.Entry (win)
entry7.grid(column=16,row=12, sticky=tk.W)

ttk.Label(win, text="y final position (mm):").grid(column=16,row=16)
entry8 = tk.Entry (win)
entry8.grid(column=16,row=20, sticky=tk.W)


ttk.Label(win, text="step distance (mm) :").grid(column=16,row=24)
entry9 = tk.Entry (win)
entry9.grid(column=16,row=28, sticky=tk.W)



ttk.Button(win, text="Get B Field", command=horizontal_click).grid(column=12, row=32)
ttk.Button(win, text="Get B Field", command=vertical_click).grid(column=16, row=32)


############################################################################
################################Mapper Functions###############################

def set_dir(move, direc):
    if direc == 'x':
        if float(move) < 1:
            direc = 'b'
            return direc
        elif float(move) >= 1:
            direc = 'f'
            return direc
    elif direc == 'y':
        if float(move) < 1:
            direc = 'd'
            return direc
        elif float(move) >= 1:
            direc = 'u'
            return direc


def set_move(move, orientation):

    if orientation == 'x':
        move  = move - abs_posx

    if move < 0:
        move = move * -1

    if orientation == 'y':
        move  = move - abs_posy

        if move < 0:
            move = move * -1
    return move


def limits_fit(move, direc):

   if direc == 'b':
       if move <= limit_b:

            return True
   if direc == 'd':
        if move <= limit_d:

            return True
   if direc =='f':

        if move <= limit_f:

            return True
   if direc == 'u':

        if move <= limit_u:

            return True
   return False


def update_limits(direc, move):
    global limit_b
    global limit_f
    global limit_u
    global limit_d

    if direc == 'b':
        limit_b -= move
        limit_f += move

    if direc == 'f':
        limit_b += move
        limit_f -= move

    if direc == 'd':
        limit_d -= move
        limit_u += move

    if direc == 'u':
        limit_d = limit_d + move
        limit_u -= move


def update_position(direc, move):
    global abs_posx
    global abs_posy

    global user_posx
    global user_posy

    if direc == 'b':
        abs_posx -= move
        user_posx -= move
    if direc == 'f':
        abs_posx += move
        user_posx += move
    if direc == 'd':
        abs_posy -= move
        user_posy -= move
    if direc == 'u':
        abs_posy += move
        user_posy += move

def find_delta_direc(xstart, xstop, direc, orientation):
    delta = xstop - xstart
    if orientation == 'x':
        if delta < 0:
            delta_direc = 'b'
        else:
            delta_direc = 'f'
        return delta_direc
    if orientation == 'y':
        if delta < 0:
            delta_direc = 'd'
        else:
            delta_direc = 'u'
        return delta_direc

def move_to_start(orientation, start):


    if orientation == 'x':

        move  = start - abs_posx

        if move < 0:
            delta_direc = 'b'
            move = move * -1
        else:
            delta_direc = 'f'

    if orientation == 'y':
        move  = start - abs_posy

        if move < 0:
            delta_direc = 'd'
            move = move * -1
        else:
            delta_direc = 'u'
    zeromove_m(delta_direc, str(move), 'f')
    return True

    #below will never get called
    if limits_fit(move, delta_direc) == True:
        zeromove_m(delta_direc, str(move), 'f')
        return True


    else:
        print('The move in the', orientation, ' direction is out of bounds')


def move_to_initial(orientation, finish, initial):
    move = initial - finish
    if orientation == 'x':
        if move < 0:
            delta_direc = 'b'
            move = move * -1
        else:
            delta_direc = 'f'
        zeromove_m(delta_direc, str(move), 'f')
    if orientation == 'y':
        move = initial - finish
        if move < 0:
            delta_direc = 'd'
            move = move * -1
        else:
            delta_direc = 'u'
        zeromove_m(delta_direc, str(move), 'f')


#################################Data Functions###################################
ser = serial.Serial('/dev/cu.usbmodem0E22D9A1')  # open serial port
conversion = 0.0015716


def create_points(List, initial, final, step):
    if (final - initial) > 0:
        while not initial > final:
            List.append(initial)
            initial += step
        return List
    elif (final - initial) < 0:
        while not initial < final:
            List.append(initial)
            initial -=step
        return List
    else:
        "initial position and final position are the same "



def initialize_line(initial, final, delta_direc, step):

    List_points = []
    List_points = create_points(List_points, initial, final, step)
    map_line(initial, final, delta_direc, step, List_points)



def change_data(string):
    data = float(string[0:15])
    return data


def make_Bdata_1(data):

    x = inst.query("MEAS:VOLT:DC? (@204)")
    y = inst.query("MEAS:VOLT:DC? (@206)")
    z = inst.query("MEAS:VOLT:DC? (@203)")

    data[0].append(change_data(x))
    data[1].append(change_data(y))
    data[2].append(change_data(z))

    return data


def make_Bdata(data):
    x_average = 0
    y_average = 0
    z_average = 0
    for i in range(5):
        x = inst.query("MEAS:VOLT:DC? (@204)")
        x_average += change_data(x)
        y = inst.query("MEAS:VOLT:DC? (@206)")
        y_average += change_data(y)
        z = inst.query("MEAS:VOLT:DC? (@203)")
        z_average += change_data(z)
    x_data = x_average/5
    y_data = y_average/5
    z_data = z_average/5

    data[0].append(x_data)
    data[1].append(y_data)
    data[2].append(z_data)

    return data

#def make_Bdata_U6(data):



def multiple(m,n):
    if (m%n) == 0:
        return True
    else:
        return False


def zeromove_m(direc, move, Bdata):
    ser.write(str.encode('q'))

    machine_step = str(round(int(move)/conversion))
    b_step = str.encode(machine_step)
    b_dir = str.encode(direc)

    ser.write((b_step))
    ser.write((b_dir))


    char = ser.read()
    if char != b'*':
        print(char)
        print("error error error ERROR")

    time.sleep(.2)
    if Bdata != 'f':
        Bdata = make_Bdata(Bdata)


    update_position(direc, int(move))
    update_limits(direc, int(move))

    return Bdata


def map_line(initial, final, delta_direc, step, List_points):
    Bdata = make_Bdata([[], [], []])
    delta = final - initial
    numsteps = abs(int(delta/step))

    for x in range(numsteps):
        zeromove_m(delta_direc, str(step), Bdata)
    plot_the_data(List_points, Bdata)


def split_Bdata(Bdata,i):
     return Bdata[i]


def plot_the_data(List, Bdata):

    Bdata1 = split_Bdata(Bdata, 0)
    Bdata2 = split_Bdata(Bdata, 1)
    Bdata3 = split_Bdata(Bdata, 2)
    run_data.append([Bdata1, Bdata2, Bdata3])


    fig, (xBxBy,xBz) = plt.subplots(nrows=1, ncols=2, sharex=True,figsize=(12, 6))

    xBxBy.plot(List,Bdata1, color='tab:blue')
    xBxBy.plot(List,Bdata2,  color='tab:orange')
    xBz.plot(List,Bdata3,  color='tab:red')

    #add features
    xBxBy.set_xlabel('mm displacement')
    xBxBy.set_ylabel('B field (Gauss)')
    xBxBy.legend(('x direction','y direction'))

    xBz.set_xlabel('mm displacement')
    xBz.set_ylabel('B field (Gauss)')
    xBz.legend(('z direction'))

    fig.tight_layout(pad=3.0)

    #save figure
    plt.savefig('Bfield.png')

    #display the plot
    plt.show()

    workbook = xlsxwriter.Workbook('Data_plot.xlsx')
    bx = workbook.add_worksheet("Bx")
    by = workbook.add_worksheet("By")
    bz = workbook.add_worksheet("Bz")

    Lables = ['Distance from 0', 'Bx', 'By', 'Bz']

    row = 1
    col = 0

    for index in range(len(run_data)):
        bx.write(0, num_run - index, abs_posy - stepy * index)
        by.write(0, num_run - index, abs_posy - stepy * index)
        bz.write(0, num_run - index, abs_posy - stepy * index)

    for item in (List):
        bx.write(row, 0, item)
        bz.write(row, 0, item)
        by.write(row, 0, item)
        row += 1

    # Iterate over the data and write it out row by row.

    for data_index in range(len(run_data)):

        for index in (range(len(run_data[data_index][0]))):
            bx.write(index + 1, data_index + 1, run_data[data_index][0][index])
            by.write(index + 1, data_index + 1, run_data[data_index][1][index])
            bz.write(index + 1, data_index + 1, run_data[data_index][2][index])

    workbook.close()



#############################################################################


#Calling Main()
def tomRun():
    global num_run
    go_to_user_zero()
    xstart = 155
    ystart = 95
    ystop = 135
    xstop = 355
    stepx = 5
    stepy = 2
    orientation = 'x'
    delt = ystop - ystart
    runs = (ystop - ystart) / stepy + 1
    if delt < 0:
        print("Y sweep must go upwards ")
    elif  multiple(delt, stepy) == False:
        print("Y delta is not divisible by the step")
    for run in range(int(runs)):
        move_to_start('y', ystart)
        ystart += stepy
        dirx_i = set_dir(xstart, orientation)
        dirx_f = set_dir(xstop, orientation)

        initial = set_move(xstart, orientation)
        final = (xstop, orientation)

        delta = final - initial
        print(delta)
        if (stepx == 0) or (stepx < 0):
            print('Enter positive, nonzero step')

        elif multiple(delta, stepx) == False:
            print("that's not divisible")
            go_to_abs_zero()
            break

        elif limits_fit(initial, dirx_i) == True and limits_fit(final, dirx_f) == True:


            initialx = abs_posx


            move_to_start(orientation, xstart)
            delta_direc = find_delta_direc(xstart, xstop, dirx_i, orientation)
            initialize_line(xstart, xstop, delta_direc, stepx)
            print_position()
        else:
            print('out of bounds')
        num_run += 1
    go_to_abs_zero()


mutex = Lock()
collected = False

def matthew_collect_data(data):
    missed = 0
    dataCount = 0
    packetCount = 0
    while(True):
        with mutex:
            if(collected):
                print("missed: %s, dataount: %s, packet count: %s" %
                      (missed, dataCount, packetCount))
                return
                #reaturn data
        for r in d.streamData():
            data.append(sum(r["AIN0"])/len(r["AIN0"]),
                        sum(r["AIN1"])/len(r["AIN1"]),
                        sum(r["AIN2"])/len(r["AIN2"]))


def matthew_test():

    #go_to_abs_zero()
    mydata = []
    p = Process(target = matthew_collect_data, args = (mydata,))
    p.start()
    time.sleep(4.0)
    with mutex:
        collected = True
    #go_to_abs_zero()
    #move_to_start('x', 50)
    p.join()
    print(mydata)

if __name__ == '__main__':
    matthew_test()





#win.mainloop()
