from collection import *
from movement import *
from data import *
import math
import numpy as np

import matplotlib.pyplot as plt


def scan(step,xinitial,yinitial,xfinal,yfinal,relative_pos,abs_pos,mode,save,abs_Label,relative_Label):
    """Pulls starting coordinates, ending coordinates, and a step size from the
    window and then moves in a very rough line between the two points. These
    coordinates are interms of the realative zero postion. Collects
    measurements as it goes and then saves this data to a timestamped
    spreadsheet"""

    m = None if (xfinal-xinitial) == 0 else(yfinal - yinitial)/(xfinal-xinitial)

    if(m != None):
        angle = abs(math.atan(m))
        xstep = round(math.cos(angle)*step)
        ystep = round(math.sin(angle)*step)
        xstep =1 if xstep == 0 else xstep
        ystep =1 if ystep == 0 else ystep
    else:
        xstep = 0
        ystep = step
    xdir = 'f' if xfinal > xinitial else 'b'
    ydir = 'u' if yfinal > yinitial else 'd'

    if goTo(xinitial,yinitial,relative_pos,abs_pos,abs_Label,relative_Label): return -1
    set_speed(2500,2500)
    Scan_Data = [[],[],[],[],[]]

    while (round(relative_pos[0]) != xfinal or round(relative_pos[1]) != yfinal):
        collect(relative_pos, Scan_Data,mode)
        if(abs(relative_pos[0] - xfinal) >= xstep):
            if move(xdir,xstep,abs_Label,relative_Label): return -1
        elif(relative_pos[0] != xfinal):
            if move(xdir,abs(relative_pos[0] - xfinal),abs_Label,relative_Label): return -1
        if(abs(relative_pos[1] - yfinal) >= ystep):
            if move(ydir,ystep,abs_Label,relative_Label): return -1
        elif(relative_pos[1] != yfinal):
            if move(ydir,abs(relative_pos[1] - yfinal),abs_Label,relative_Label): return -1
    collect(relative_pos, Scan_Data,mode)
    plot_Bfield(Scan_Data)

    if(save):
        saveData(Scan_Data)

    set_speed(40000,30000)
    if goTo(xinitial,yinitial,relative_pos,abs_pos,abs_Label,relative_Label): return -1

def Two_D_map(step, xinitial, yinitial, xfinal, yfinal,relative_pos,abs_pos,mode,save,dominant,abs_Label,relative_Label):
        """given a step size, starting and ending coordinates, the relative
        position of the arm the absolute position of the arm, the data collection
        mode(which device is being used), a bool to save the data or not, and
        the dominant scan direction(z for scan all z before moving in y and y
        for the opposite) maps across that area and displays plots of the field
        intensity in all 3 axises"""

        xfinal += 1 if xfinal > xinitial else -1
        yfinal += 1 if yfinal > yinitial else -1

        xdir = 'f' if xfinal > xinitial else 'b'
        ydir = 'u' if yfinal > yinitial else 'd'

        if goTo(xinitial,yinitial,relative_pos,abs_pos,abs_Label,relative_Label): return -1

        Scan_Data = [[],[],[],[],[]]
        #this is vile should just make a funtion that swaps the directions
        #to deceased to do that rn this will work
        if dominant == "y":
            while(round(relative_pos[0]) != xfinal):
                set_speed(40000,30000)
                if goTo(relative_pos[0],yinitial, relative_pos,abs_pos,abs_Label,relative_Label): return -1
                set_speed(2500,2500)
                time.sleep(1)

                while (round(relative_pos[1]) != yfinal):
                    collect(relative_pos, Scan_Data,mode)
                    if(abs(relative_pos[1] - yfinal) >= step):
                        if move(ydir,step,abs_Label,relative_Label): return -1
                    elif(relative_pos[1] != yfinal):
                        if move(ydir,abs(relative_pos[1] - yfinal),abs_Label,relative_Label): return -1
                if(abs(relative_pos[0] - xfinal) >= step):
                    if move(xdir,step,abs_Label,relative_Label): return -1
                elif(relative_pos[0] != xfinal):
                    if move(xdir,abs(relative_pos[0] - xfinal),abs_Label,relative_Label): return -1

            zlen = (len(pd.unique(Scan_Data[0])))
            ylen = (len(pd.unique(Scan_Data[1])))

            zmatrix, ymatrix = np.meshgrid(pd.unique(Scan_Data[0]),
                                           pd.unique(Scan_Data[1]))
            xfield = np.rot90(np.fliplr(np.array(Scan_Data[2]).reshape(zlen, ylen)))
            yfield = np.rot90(np.fliplr(np.array(Scan_Data[3]).reshape(zlen, ylen)))
            zfield = np.rot90(np.fliplr(np.array(Scan_Data[4]).reshape(zlen, ylen)))
        else:
            while(round(relative_pos[1]) != yfinal):
                set_speed(40000,30000)
                if goTo(xinitial,relative_pos[1], relative_pos,abs_pos,abs_Label,relative_Label): return -1
                set_speed(2500,2500)
                time.sleep(1)

                while (round(relative_pos[0]) != xfinal):
                    collect(relative_pos, Scan_Data,mode)
                    if(abs(relative_pos[0] - xfinal) >= step):
                        if move(xdir,step,abs_Label,relative_Label): return -1
                    elif(relative_pos[0] != xfinal):
                        if move(xdir,abs(relative_pos[0] - xfinal),abs_Label,relative_Label):return -1
                if(abs(relative_pos[1] - yfinal) >= step):
                    if move(ydir,step,abs_Label,relative_Label): return -1
                elif(relative_pos[1] != yfinal):
                    if move(ydir,abs(relative_pos[1] - yfinal),abs_Label,relative_Label): return -1

            zlen = (len(pd.unique(Scan_Data[0])))
            ylen = (len(pd.unique(Scan_Data[1])))

            zmatrix, ymatrix = np.meshgrid(pd.unique(Scan_Data[0]),
                                           pd.unique(Scan_Data[1]))
            xfield = np.array(Scan_Data[2]).reshape(ylen, zlen)
            yfield = np.array(Scan_Data[3]).reshape(ylen, zlen)
            zfield = np.array(Scan_Data[4]).reshape(ylen, zlen)

        xlevels, xcenter = TD_plot(zmatrix,ymatrix,xfield,"X")
        ylevels, ycenter = TD_plot(zmatrix,ymatrix,yfield,"Y")
        zlevels, zcenter = TD_plot(zmatrix,ymatrix,zfield,"Z")

        fig4, ZY = plt.subplots(1,1)
        plt.streamplot(zmatrix,ymatrix,zfield,yfield)

        plt.show()

        if (save):
            saveData(Scan_Data)

        set_speed(40000,30000)
        if goTo(xinitial,yinitial,relative_pos,abs_pos,abs_Label,relative_Label): return -1

        plt.show(block=True)
