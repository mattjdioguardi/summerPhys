

import u6



d = u6.U6()
# For applying the proper calibration to readings.
d.getCalibrationData()
print("Configuring U6 stream")
d.streamConfig(NumChannels=3, ChannelNumbers=[0, 1, 2], ChannelOptions=[0, 0, 0],
SettlingFactor=1, ResolutionIndex=1, ScanFrequency=1000)

def U6_point():
    d.streamStart()
    Bcur = next(d.streamData())
    d.streamStop()
    Bfield = [1, 1,
              sum(Bcur["AIN0"])/len(Bcur["AIN0"]),
              sum(Bcur["AIN1"])/len(Bcur["AIN1"]),
              sum(Bcur["AIN2"])/len(Bcur["AIN2"])]
    return Bfield




if __name__ == '__main__':
    U6_point()

