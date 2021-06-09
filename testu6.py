import time
from threading import Thread, Lock

import u6








mutex = Lock()
collected = 0

def matthew_collect_data(data):
    global collected

    missed = 0
    dataCount = 0
    packetCount = 0
    d.streamStart()

                #reaturn data
    for r in d.streamData():
        mutex.acquire()
        if(collected):
            print("missed: %s, dataount: %s, packet count: %s" %
                  (missed, dataCount, packetCount))
            return
        mutex.release()
        data.append((sum(r["AIN0"])/len(r["AIN0"]),
                    sum(r["AIN1"])/len(r["AIN1"]),
                    sum(r["AIN2"])/len(r["AIN2"])))


def matthew_test():
    global collected
    #go_to_abs_zero()
    mydata = []
    t = Thread(target = matthew_collect_data, args = (mydata,))
    t.start()
    time.sleep(4.0)
    mutex.acquire()
    collected = 1
    mutex.release()
    print (collected)
    #go_to_abs_zero()
    #move_to_start('x', 50)
    t.join()
    print(mydata)

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
    Bfield = [relative_pos[0], relative_pos][1],
              sum(Bcur["AIN0"])/len(Bcur["AIN0"]),
              sum(Bcur["AIN1"])/len(Bcur["AIN1"]),
              sum(Bcur["AIN2"])/len(Bcur["AIN2"])]]
    return Bfield




if __name__ == '__main__':
    U6_collect()

