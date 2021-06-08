import serial
import tkinter as tk
import time
from multiprocessing import Process, Lock
import u6
from functools import partial



###################NEW 2021##########################


##############################u6 setup##########################################
# d = u6.U6()
# # For applying the proper calibration to readings.
# d.getCalibrationData()
# print("Configuring U6 stream")
# d.streamConfig(NumChannels=3, ChannelNumbers=[0, 1, 2], ChannelOptions=[0, 0, 0],
#                SettlingFactor=1, ResolutionIndex=1, ScanFrequency=5)
#

#################################serial setup###################################
# ser = serial.Serial('/dev/cu.usbmodem0E22D9A1')  # open serial port
# conversion = 0.0015716


#######################tk setup#########################################
win = tk.Tk()
win.title("3D Mapper")
win.geometry("1000x1000")


def set_absolute_zero(abs_pos):
    abs_pos[0] = 0
    abs_pos[1] = 0

def set_relative_zero(abs_pos):
    relative_pos[0] = 0
    relative_pos[1] = 0

def abs_home(abs_pos):
    if(abs_pos[0]) > 0:
        move('b',abs_pos[0])
    else:
        move('f',-abs_pos[0])

    if(abs_pos[1]) > 0:
        move('d',abs_pos[1])
    else:
        move('u',-abs_pos[1])

def relative_home(relative_pos):
    if(relative_pos[0]) > 0:
        move('b',relative_pos[0])
    else:
        move('f',-relative_pos[0])

    if(relative_pos[1]) > 0:
        move('d',relative_pos[1])
    else:
        move('u',-relative_pos[1])




def move(direc, step):
    """Takes direc char of u,d,f,b (up, down, forward, backward)
        and step in mm. move that distance.
    """
    ser.write(str.encode('q'))

    machine_step = str(round(step/conversion))

    ser.write((str.encode(machine_step)))
    ser.write((str.encode(direc)))

    if ser.read() != b'*':
        print(char)
        print("error error error ERROR")

    global abs_pos
    global relative_pos
    update_position(direc, step, abs_pos, relative_pos)
    a.config(text = "%s , %s" %(abs_pos[0],abs_pos[1]))




    #later change to only manage absolute pos and calculte realtive pos based off offset when need be
def update_position(direc, move, abs_pos, relative_pos):
    if direc == 'b':
        abs_pos[0] -= move
        relative_pos[0] -= move
    if direc == 'f':
        abs_pos[0] += move
        relative_pos[0] += move
    if direc == 'd':
        abs_pos[1] -= move
        relative_pos[1] -= move
    if direc == 'u':
        abs_pos[1] += move
        relative_pos[1] += move


a = tk.Label(win, text = "%s , %s" %(abs_pos[0],abs_pos[1]))
a.grid(column=4, row=4)


tk.Button(win, text="up 1",command=partial(move,'u', 1)).grid(column=4, row=3)
tk.Button(win, text="up 10",command=partial(move,'u', 10)).grid(column=4, row=2)
tk.Button(win, text="up 100",command=partial(move,'u', 100)).grid(column=4, row=1)

tk.Button(win, text="down 1",command=partial(move,'d', 1)).grid(column=4, row=5)
tk.Button(win, text="down 10",command=partial(move,'d', 10)).grid(column=4, row=6)
tk.Button(win, text="down 100",command=partial(move,'d', 100)).grid(column=4, row=7)

tk.Button(win, text="back 1",command=partial(move,'b', 1)).grid(column=3, row=4)
tk.Button(win, text="back 10",command=partial(move,'b', 10)).grid(column=2, row=4)
tk.Button(win, text="back 100",command=partial(move,'b', 100)).grid(column=1, row=4)

tk.Button(win, text="forward 1",command=partial(move,'f', 1)).grid(column=5, row=4)
tk.Button(win, text="forward 10",command=partial(move,'f', 10)).grid(column=6, row=4)
tk.Button(win, text="forward 100",command=partial(move,'f', 100)).grid(column=7, row=4)


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

    #initialize at some place else
    abs_pos = [0,0]
    relative_pos = [0,0]

    #ser = serial.Serial('/dev/cu.usbmodem0E22D9A1')  # open serial port
    conversion = 0.0015716
    limit_b = 10000
    limit_f = 10000
    limit_u = 10000
    limit_d = 10000







    win.mainloop()

