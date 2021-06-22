

import u6
import time

DESIRED_SAMPLES = 10000

d = u6.U6()
# For applying the proper calibration to readings.
d.getCalibrationData()
print("Configuring U6 stream")
d.streamConfig(NumChannels=3, ChannelNumbers=[0, 1, 2], ChannelOptions=[0, 0, 0],
SettlingFactor=1, ResolutionIndex=1, ScanFrequency=DESIRED_SAMPLES)

def U6_point():
    samples_collected = 0
    Bfield = [1, 1, 0, 0, 0]
    d.streamStart()
    while(samples_collected < DESIRED_SAMPLES):
        print("hello")
        Bcur = next(d.streamData())
        Bfield[2] += sum(Bcur["AIN0"])/len(Bcur["AIN0"])
        Bfield[3] += sum(Bcur["AIN1"])/len(Bcur["AIN1"])
        Bfield[4] += sum(Bcur["AIN2"])/len(Bcur["AIN2"])
        samples_collected += len(Bcur["AIN0"]) + len(Bcur["AIN1"])+ len(Bcur["AIN2"])
    d.streamStop()
    return Bfield




if __name__ == '__main__':
    print(U6_point())

