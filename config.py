########globals :(((##################




abs_pos = [0,0]
relative_pos = [0,0]
relative_offset = [0,0]
abs_steps = [0,0]
#labjack_Voltage = [0,10]
Volt_to_gauss = 1
d = None
inst = None
conversion = 0.0015716 #conversion*steps = mm
xlim = 450 #limit in z direction is 440 mm
ylim = -210 #limit in y direction is 185 mm
DESIRED_SAMPLES = 10000#samples to average per axis per data point