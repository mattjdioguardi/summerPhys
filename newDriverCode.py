import serial
import tkinter as tk
import time
import pyvisa
from datetime import datetime
from multiprocessing import Process, Lock
import u6
from functools import partial
import matplotlib.pyplot as plt
import math
import pandas as pd



###################NEW 2021##########################

##############################Keithley Set Up#####################################
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB0::16::INSTR')
print(inst.query("*IDN?"))
inst.write("SENS:FUNC 'VOLT:DC' ")
inst.write("SENS:VOLT:DC:RANG:AUTO ON ")
inst.write("SENS:VOLT:NPLC 5")		#integration time in PLCs, 1 PLC= 1power line cycle =1/60 sec
inst.write("SENS:VOLT:DC:AVER:COUN 6")

# #############################u6 setup##########################################
d = u6.U6()
d.getCalibrationData()
print("Configuring U6 stream")
d.streamConfig(NumChannels=3, ChannelNumbers=[0, 1, 2], ChannelOptions=[0, 0, 0],
                SettlingFactor=1, ResolutionIndex=1, ScanFrequency=1000)

################################serial setup###################################
ser = serial.Serial('/dev/cu.usbmodem0E22D9A1')  # open serial port

########globals :(((##################
abs_pos = [0,0]
relative_pos = [0,0]
relative_offset = [0,0]
abs_steps = [0,0]


#clean up all the single lines of assignment for the lists its messy
def set_absolute_zero(abs_pos, abs_steps):
    """resets the absolute zero position to the postion that the steppers are
    currently at"""
    relative_offset[0] -= abs_pos[0]
    relative_offset[1] -= abs_pos[1]
    abs_pos[0] = 0
    abs_pos[1] = 0
    abs_steps[0] = 0
    abs_steps[1] = 0
    abs_Label.config(text = "%s , %s" %(abs_pos[0],abs_pos[1]))

def set_relative_zero(relative_pos, relative_offset):
    """resets the relative zero poistion to the postion the steppers are currently
    at """
    relative_offset[0] = abs_pos[0]
    relative_offset[1] = abs_pos[1]
    relative_pos[0] = 0
    relative_pos[1] = 0
    relative_Label.config(text = "%s , %s" %(relative_pos[0],relative_pos[1]))

#later change to only manage absolute pos and calculte realtive pos based off offset when need be
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

def move(direc, step):
    """Takes direc char of u,d,f,b (up, down, forward, backward)
        and step in mm and moves that distance in that direction."""
    ser.write(str.encode('q'))

    machine_step = str(round(step/conversion))

    ser.write((str.encode(machine_step)))
    ser.write((str.encode(direc)))
    if ser.read() != b'*':
        print("error error error ERROR")
    global abs_steps
    global abs_pos
    global relative_pos
    global relative_offset

    update_position(direc, round(step/conversion), abs_steps,abs_pos, relative_pos, relative_offset)
    abs_Label.config(text = "%.3g , %.3g" %(abs_pos[0],abs_pos[1]))
    relative_Label.config(text = "%.3g , %.3g" %(relative_pos[0],relative_pos[1]))

def abs_home(abs_pos):
    """moves the steppers back to the Absolute zero position"""
    if(abs_pos[0]) > 0:
        move('b',abs_pos[0])
    else:
        move('f',-abs_pos[0])

    if(abs_pos[1]) > 0:
        move('d',abs_pos[1])
    else:
        move('u',-abs_pos[1])

def relative_home(relative_pos):
    """moves the steppers back to the relative home position"""
    if(relative_pos[0]) > 0:
        move('b',relative_pos[0])
    else:
        move('f',-relative_pos[0])

    if(relative_pos[0]) > 0:
        move('d',relative_pos[1])
    else:
        move('u',-relative_pos[1])

def goTo(x,y,pos):
    """given an x(z) and y position the stepers move to those coordinates in
    terms of the given position relative or absolute can be passed"""
    if(x<xlim and x >= 0):
        if(x<pos[0]):
            move('b',pos[0]-x)
        else:
            move('f',x-pos[0])
    if(y<ylim and y >= 0):
        if(y<pos[1]):
            move('d',pos[1]-y)
        else:
            move('u',y-pos[1])

#gross way to do this but tkninter is annoying
def goToClick(abs_pos):
    """takes the values in the goto bozes on the interface and sends those to
    goTo. This uses relative coordinates"""
    x = int(xmove.get())#make this more elegant for restriction to ints
    y = int(ymove.get())
    goTo(x,y,abs_pos)

# Yeah this is anoying and no need for a diagonal plot at least as of now
# leaving for later or never
#should probably add a get direction fucntion so goto and this are cleaner
#need to add bounds so arm doestn crash
def scan(relative_pos):
    """Pulls starting coordinates, ending coordinates, and a step size from the
    window and then moves in a very rough line between the two points. These
    coordinates are interms of the realative zero postion. Collects
    measurements as it goes and then saves this data to a timestamped
    spreadsheet"""
    step = int(step_size.get())
    xinitial = int(xstart.get())
    yinitial = int(ystart.get())
    xfinal = int(xend.get())
    yfinal = int(yend.get())
    m = None if (xfinal-xinitial) == 0 else(yfinal - yinitial)/(xfinal-xinitial)

    if(m != None):
        angle = abs(math.atan(m))
        xstep = round(math.cos(angle)*step)
        ystep = round(math.sin(angle)*step)
        xstep +=1 if xstep == 0 else xstep
        ystep +=1 if ystep == 0 else ystep
    else:
        xstep = 0
        ystep = step
    xdir = 'f' if xfinal > xinitial else 'b'
    ydir = 'u' if yfinal > yinitial else 'd'

    goTo(xinitial,yinitial,relative_pos)
    Scan_Data = [[],[],[],[],[]]

    while (round(relative_pos[0]) != xfinal or round(relative_pos[1]) != yfinal):
        collect(relative_pos, Scan_Data)
        if(abs(relative_pos[0] - xfinal) >= xstep):
            move(xdir,xstep)
        elif(relative_pos[0] != xfinal):
            move(xdir,abs(relative_pos[0] - xfinal))
        if(abs(relative_pos[1] - yfinal) >= ystep):
            move(ydir,ystep)
        elif(relative_pos[1] != yfinal):
            move(ydir,abs(relative_pos[1] - yfinal))
    collect(relative_pos, Scan_Data)
    saveData(Scan_Data)
    goTo(xfinal,yfinal,relative_pos)

def GPIB_Point(relative_pos):
    """records field at a single point from GPIB and returns it in the form
    [z coordonate, y coordonate, Bx, By, Bz]"""
    Bfield = [0,0,0]
    for i in range(5):
        Bfield[0] += float(inst.query("MEAS:VOLT:DC? (@204)")[:15])
        Bfield[1] += float(inst.query("MEAS:VOLT:DC? (@206)")[:15])
        Bfield[2] += float(inst.query("MEAS:VOLT:DC? (@203)")[:15])
    Bfield = [relative_pos[0], relative_pos[1]] + [x/5 for x in Bfield]
    return Bfield

def U6_point(relative_pos):
    d.streamStart()
    Bcur = next(d.streamData())
    d.streamStop()
    Bfield = [relative_pos[0], relative_pos[1],
    sum(Bcur["AIN0"])/len(Bcur["AIN0"]),
    sum(Bcur["AIN1"])/len(Bcur["AIN1"]),
    sum(Bcur["AIN2"])/len(Bcur["AIN2"])]
    return Bfield

def collect(relative_pos,data):
    """Records data from GPIB  and appends them to a passed list of form
    [[z coordonates], [y coordonates], [Bx], [By], [Bz]] where each entry of the
    same index is one data point"""

    if(mode.get() == "GPIB"):
        Bfield = GPIB_Point(relative_pos)
    elif(mode.get() == "labjack"):
        Bfield = U6_point(relative_pos)
    for x in range(len(Bfield)):
        data[x].append(Bfield[x])


def saveData(data):
    """saves passed data in the form
    [[z coordonates], [y coordonates], [Bx], [By], [Bz]] to a spreadsheet that
    is timestamped"""
    now = datetime.now()
    dateString = now.strftime("%d-%m-%Y %H:%M:%S")

    df = pd.DataFrame({'z':data[0], 'y': data[1], 'Bx':data[2],
                       'By':data[3],'Bz':data[4],})
    writer = pd.ExcelWriter("Bfield_at_"+dateString+ '.xlsx')
    df.to_excel(writer,index=False)
    writer.save()

def Field_Window(relative_pos):
    """opens a new window displaying the field at the current point"""
    Field = tk.Toplevel(win)
    Field.geometry("300x300")

    if(mode.get() == "GPIB"):
        Cur_Field = GPIB_Point(relative_pos)
    elif(mode.get() == "labjack"):
        Cur_Field = U6_point(relative_pos)

    tk.Label(Field, text = "Bx:%.7g" %(Cur_Field[2])).grid(column=1,row=1)
    tk.Label(Field, text = "Bx:%.7g" %(Cur_Field[3])).grid(column=1,row=2)
    tk.Label(Field, text = "Bx:%.7g" %(Cur_Field[4])).grid(column=1,row=3)


#########################tk nonsense ###############################################
"""some nasty stuff where parameters arent passed but works just some global
scoping is used. maybe fix later. not really best practice but its the easiest
way to setup tkinter and it works"""

win = tk.Tk()
win.title("3D Mapper")
win.geometry("2000x500")

tk.Label(win, text="absolute position").grid(row=1,column=1)
abs_Label = tk.Label(win, text = "%s , %s" %(abs_pos[0],abs_pos[1]))
abs_Label.grid(column=1, row=2)
tk.Button(win, text="home to absolute 0",command=partial(abs_home,abs_pos)).grid(column=1, row=4)

tk.Label(win, text="relative position").grid(row=1,column=2)
relative_Label = tk.Label(win, text = "%s , %s" %(relative_pos[0],relative_pos[1]))
relative_Label.grid(column=2, row=2)
tk.Button(win, text="set relative 0",command=partial(set_relative_zero,relative_pos, relative_offset)).grid(column=2, row=3)
tk.Button(win, text="home to relative 0",command=partial(relative_home,relative_pos)).grid(column=2, row=4)

tk.Button(win, text="up 1",command=partial(move,'u', 1)).grid(column=6, row=4)
tk.Button(win, text="up 10",command=partial(move,'u', 10)).grid(column=6, row=3)
tk.Button(win, text="up 100",command=partial(move,'u', 100)).grid(column=6, row=2)

tk.Button(win, text="down 1",command=partial(move,'d', 1)).grid(column=6, row=6)
tk.Button(win, text="down 10",command=partial(move,'d', 10)).grid(column=6, row=7)
tk.Button(win, text="down 100",command=partial(move,'d', 100)).grid(column=6, row=8)

tk.Button(win, text="back 1",command=partial(move,'b', 1)).grid(column=5, row=5)
tk.Button(win, text="back 10",command=partial(move,'b', 10)).grid(column=4, row=5)
tk.Button(win, text="back 100",command=partial(move,'b', 100)).grid(column=3, row=5)

tk.Button(win, text="forward 1",command=partial(move,'f', 1)).grid(column=7, row=5)
tk.Button(win, text="forward 10",command=partial(move,'f', 10)).grid(column=8, row=5)
tk.Button(win, text="forward 100",command=partial(move,'f', 100)).grid(column=9, row=5)

tk.Label(win, text="go to:").grid(column=10,row=1)
tk.Label(win, text="z:").grid(column=10,row=2)
xmove = tk.Entry(win,width=3)
xmove.grid(column=11,row=2)
tk.Label(win, text="y:").grid(column=12,row=2)
ymove = tk.Entry(win,width=3)
ymove.grid(column=13,row=2)
tk.Button(win, text="GO!",command=partial(goToClick,relative_pos)).grid(column=14, row=2)

tk.Label(win, text="scan from:").grid(column=10,row=4)
tk.Label(win, text="z:").grid(column=10,row=5)
xstart = tk.Entry(win,width=3)
xstart.grid(column=11,row=5)
tk.Label(win, text="y:").grid(column=12,row=5)
ystart = tk.Entry(win,width=3)
ystart.grid(column=13,row=5)

tk.Label(win, text="stepsize:").grid(column=14,row=5)
step_size = tk.Entry(win,width=3)
step_size.grid(column=15,row=5)

tk.Label(win, text="scan to:").grid(column=10,row=6)
tk.Label(win, text="z:").grid(column=10,row=7)
xend = tk.Entry(win,width=3)
xend.grid(column=11,row=7)
tk.Label(win, text="y:").grid(column=12,row=7)
yend = tk.Entry(win,width=3)
yend.grid(column=13,row=7)
tk.Button(win, text="GO!",command=partial(scan,relative_pos)).grid(column=14, row=7)

tk.Button(win, text="Get current field",command= partial(Field_Window,relative_pos)).grid(column=10,row=9)

def advancedNewWindow():
    """opens window with advanced settings"""
    advanced = tk.Toplevel(win)
    advanced.title("advanced settings")
    advanced.geometry("300x300")
    tk.Button(advanced, text="set absolute 0",command=partial(set_absolute_zero,abs_pos,abs_steps)).grid(column=1, row=3)
    step_Label = tk.Label(advanced, text = "%s , %s" %(abs_steps[0],abs_steps[1]))
    step_Label.grid(column=1,row=1)

tk.Button(win, text="Advanced Settings",command=advancedNewWindow).grid(column=1, row=20)

mode = tk.StringVar(win)
modes = {"labjack", "GPIB", "labjack + GBIB"}
mode.set("labjack")
mode_select = tk.OptionMenu(win,mode,*modes)
mode_select.grid(column=1,row=7)



# def matthew_collect_data(data):
#     missed = 0
#     dataCount = 0
#     packetCount = 0
#     while(True):
#         with mutex:
#             if(collected):
#                 print("missed: %s, dataount: %s, packet count: %s" %
#                       (missed, dataCount, packetCount))
#                 return
#                 #reaturn data
#         for r in d.streamData():
#             data.append(sum(r["AIN0"])/len(r["AIN0"]),
#                         sum(r["AIN1"])/len(r["AIN1"]),
#                         sum(r["AIN2"])/len(r["AIN2"]))

# def matthew_test():

#     #go_to_abs_zero()
#     mydata = []
#     p = Process(target = matthew_collect_data, args = (mydata,))
#     p.start()
#     time.sleep(4.0)
#     with mutex:
#         collected = True
#     #go_to_abs_zero()
#     #move_to_start('x', 50)
#     p.join()
#     print(mydata)

if __name__ == '__main__':

    conversion = 0.0015716 #conversion*steps = mm
    limit_b = 10000 #direction limits. not implemented will remove in final version
    limit_f = 10000
    limit_u = 10000
    limit_d = 10000
    xlim = 440 #limit in z direction is 440 mm
    ylim = 185 #limit in y direction is 185 mm

    win.mainloop()

