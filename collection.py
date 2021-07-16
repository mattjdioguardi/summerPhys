import u6
import pyvisa
import time
import config

def initialize_sensors(mode):
    """Initiliazes the selected sensor"""

    global inst
    global d
    if(mode == "Keithley"):
        ##############################Keithley Set Up#####################################
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        config.inst = rm.open_resource('GPIB0::16::INSTR')
        print(inst.query("*IDN?"))
        config.inst.write("SENS:FUNC 'VOLT:DC' ")
        config.inst.write("SENS:VOLT:DC:RANG:AUTO ON ")
        config.inst.write("SENS:VOLT:NPLC 5")		#integration time in PLCs, 1 PLC= 1power line cycle =1/60 sec
        config.inst.write("SENS:VOLT:DC:AVER:COUN 6")

    elif(mode == "labjack"):
        # #############################u6 setup##########################################
        config.d = u6.U6()
        config.d.getCalibrationData()
        print("Configuring U6 stream")
        config.d.streamConfig(NumChannels=3, ChannelNumbers=[0, 1, 2], ChannelOptions=[0, 0, 0],
        SettlingFactor=1, ResolutionIndex=1, ScanFrequency=10000)

    elif(mode == "Sypris"):
        ###################sypris setup#####################
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        config.inst = rm.open_resource('GPIB0::01::INSTR')
        print(inst.query("*IDN?"))
        config.inst.write("SENS#:FLUX:DC")
        config.inst.write("SENS#:FLUX:RANG:AUT ON")
        config.inst.write("CALC#:AVER:COUN 6")

def Keithly_Point(relative_pos):
    """records field at a single point from GPIB and returns it in the form
    [z coordonate, y coordonate, Bx, By, Bz]"""
    Bfield = [relative_pos[0], relative_pos[1], 0, 0, 0, 0, 0, 0]
    for i in range(5):
        Bx = float(config.inst.query("MEAS:VOLT:DC? (@204)")[:15])
        By = float(config.inst.query("MEAS:VOLT:DC? (@206)")[:15])
        Bz = float(config.inst.query("MEAS:VOLT:DC? (@203)")[:15])

        Bfield[2] += Bx
        Bfield[4] += By
        Bfield[6] += Bz

        std[0].append(Bx)
        std[1].append(By)
        std[2].append(Bz)


    for i in range(2,7):
        if i % 2 ==0:
            Bfield[i] /= packets_collected
    Bfield[3] = np.std(std[0])
    Bfield[5] = np.std(std[1])
    Bfield[7] = np.std(std[2])
    return Bfield

def Sypris_Point(relative_pos):
    """records field at a single point from GPIB and returns it in the form
    [z coordonate, y coordonate, Bx, By, Bz]"""
    Bfield = [relative_pos[0], relative_pos[1], 0, 0, 0, 0, 0, 0]
    std = [[],[],[]]
    for i in range(5):
        Bx = float(config.cinst.query("MEAS1:FLUX?")[:-2])
        By = float(config.inst.query("MEAS1:FLUX?")[:-2])
        Bz = float(config.inst.query("MEAS1:FLUX?")[:-2])

        Bfield[2] += Bx
        Bfield[4] += By
        Bfield[6] += Bz

        std[0].append(Bx)
        std[1].append(By)
        std[2].append(Bz)

    for i in range(2,7):
        if i % 2 ==0:
            Bfield[i] /= packets_collected
    Bfield[3] = np.std(std[0])
    Bfield[5] = np.std(std[1])
    Bfield[7] = np.std(std[2])
    return Bfield

def U6_Point(relative_pos):
    """records field at a single point from U6 and returns it in the form
    [z coordonate, y coordonate, Bx, By, Bz]"""
    samples_collected = 0
    packets_collected = 0
    Bfield = [relative_pos[0], relative_pos[1], 0, 0, 0, 0, 0, 0]
    std = [[],[],[]]
    config.d.streamStart()
    while(samples_collected < 3*config.DESIRED_SAMPLES):
        Bcur = next(config.d.streamData())
        Bfield[2] += sum(Bcur["AIN0"])/len(Bcur["AIN0"])
        Bfield[4] += sum(Bcur["AIN1"])/len(Bcur["AIN1"])
        Bfield[6] += sum(Bcur["AIN2"])/len(Bcur["AIN2"])

        std[0] += Bcur["AIN0"]
        std[1] += Bcur["AIN1"]
        std[2] += Bcur["AIN2"]

        samples_collected += len(Bcur["AIN0"]) + len(Bcur["AIN1"])+ len(Bcur["AIN2"])
        packets_collected += 1
    config.d.streamStop()
    for i in range(2,7):
        if i % 2 ==0:
            Bfield[i] /= packets_collected
    Bfield[3] = np.std(std[0])
    Bfield[5] = np.std(std[1])
    Bfield[7] = np.std(std[2])

    return Bfield

def collect(relative_pos,data, mode):
    """Records data from GPIB  and appends them to a passed list of form
    [[z coordonates], [y coordonates], [Bx], [By], [Bz]] where each entry of the
    same index is one data point"""

    if(mode == "Keithley"):
        Bfield = Keithly_Point(relative_pos)
    elif(mode == "labjack"):
        Bfield = U6_Point(relative_pos)
    elif(mode == "Sypris"):
        Bfield = Sypris_Point(relative_pos)
    for x in range(len(Bfield)):
        data[x].append(Bfield[x])


def get_noise(mode):
    """takes many samples of the field at one point and returns these lists(field
    over time) in the form of [[Bx],[By],[Bz]] such that noise in the system
    can be seen """
    if(mode == "Keithley"):
        Bfield = [[],[],[]]
        for i in range(100):
            Bfield[0].append(float(config.inst.query("MEAS:VOLT:DC? (@204)")[:15]))
            Bfield[1].append(float(config.inst.query("MEAS:VOLT:DC? (@206)")[:15]))
            Bfield[2].append(float(config.inst.query("MEAS:VOLT:DC? (@203)")[:15]))
        return Bfield

    elif(mode == "labjack"):
        samples_collected = 0
        packets_collected = 0
        Bfield = [[], [], []]
        config.d.streamStart()
        while(samples_collected < 3*config.DESIRED_SAMPLES):
            Bcur = next(config.d.streamData())
            Bfield[2] += Bcur["AIN0"]
            Bfield[3] += Bcur["AIN1"]
            Bfield[4] += Bcur["AIN2"]

            samples_collected += len(Bcur["AIN0"]) + len(Bcur["AIN1"])+ len(Bcur["AIN2"])
            packets_collected += 1
        config.d.streamStop()
        return Bfield
    elif(mode == "Sypris"):
        Bfield = [[],[],[]]
        for i in range(100):
            Bfield[0].append(float(config.cinst.query("MEAS1:FLUX?")[:-2]))
            Bfield[1].append(float(config.inst.query("MEAS1:FLUX?")[:-2]))
            Bfield[2].append(float(config.inst.query("MEAS1:FLUX?")[:-2]))
        return Bfield






