import u3
import numpy as np
import config

##################################U3 setup##########################
e = u3.U3()
e.getCalibrationData()


def auto_zero(coil,axis,U6_Point):
    """given a specific coil and axis will vary that current and find the optimal
    current for getting a 0 Field"""
    #this will not be able to stay as a list as multiple lab jacks will require
    #adressing different devices
    if(coil[1] < 2):
        jack = config.d
    else:
        jack = e
    low = 0
    high = 5
    Bfield = []
    for r in range(5):
        print(r)
        voltages = np.linspace(low,high,11)
        Bfield = np.zeros(len(voltages))
        offset = (high - low)/11
        for i, v in enumerate(voltages):
            jack.writeRegister(coil[0],v)
            Bfield[i] = abs(0 - U6_Point(config.relative_pos)[axis])
        low = voltages[list(Bfield).index(min(Bfield))] - offset
        high = voltages[list(Bfield).index(min(Bfield))] + offset
        print(min(Bfield))
    jack.writeRegister(coil[0],voltages[list(Bfield).index(min(Bfield))])

def setCurrent(coil,reg,val):
    """Takes a given coil number and pulls the voltage from a tk entry and sets
    that voltage on the labjacks to control the current of the power supplys
    P.S. This is kinda nasty leaving it in the tk nonsese section as it is very
    dependent on setup as we are currently using 2 U3s and a U6 so registers and
    different devices need to be used for differnt coils."""

    #should make the entry correspond to the current not just set the entry as V
    if(coil < 2):
        config.d.writeRegister(reg,float(val()))
    else:
        e.writeRegister(reg,float(val()))

