import serial
import tkinter as tk
import time
import pyvisa
from datetime import datetime
import u6
import u3
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.cbook as cbook
import matplotlib.colors as colors
import math
import pandas as pd
import numpy as np

import mapper_gui
import config

########################################################################
#  Written by Matthew Dioguardi during Hamilton summer reasearch 2021. #
#  working with research advisers Gorden Jones and Brian Collett.      #
#                                                                      #
#  Email: mattjdioguardi@gmail.com                                     #
#  github: github.com/mattjdioguardi                                   #
########################################################################



########globals :(((##################
# abs_pos = [0,0]
# relative_pos = [0,0]
# relative_offset = [0,0]
# abs_steps = [0,0]
# labjack_Voltage = [0,10]
# Volt_to_gauss = 1
# d = None
# inst = None
#


if __name__ == '__main__':
    mapper_gui.start_gui()

