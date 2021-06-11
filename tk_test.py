import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def saveData(data):
    """saves passed data in the form
    [[z coordonates], [y coordonates], [Bx], [By], [Bz]] to a spreadsheet that
    is timestamped"""
    now = datetime.now()
    dateString = now.strftime("%d-%m-%Y %H:%M:%S")

    df = pd.DataFrame({'z':data[0], 'y': data[1], 'Bx':data[2],
                       'By':data[3],'Bz':data[4],})
    writer = pd.ExcelWriter("Bfield_at_"+dateString+ '.xlsx')
    df.to_excel(writer)
    writer.save()

def plot_Bfield(data):
    """[[z coordonates], [y coordonates], [Bx], [By], [Bz]]"""

    # fig, (xBxBy,xBz) = plt.subplots(nrows=1, ncols=2, sharex=True,figsize=(12, 6))
    #
    # xBxBy.plot(data[0],data[2], color='tab:blue')
    # xBxBy.plot(data[0],data[3],  color='tab:orange')
    # xBz.plot(data[0],data[4],  color='tab:red')
    #
    # #add features
    # xBxBy.set_xlabel('mm displacement')
    # xBxBy.set_ylabel('B field (Gauss)')
    # xBxBy.legend(('x direction','y direction'))
    #
    # xBz.set_xlabel('mm displacement')
    # xBz.set_ylabel('B field (Gauss)')
    # xBz.legend(('z direction'))
    #
    # fig.tight_layout(pad=3.0)
    #
    # #save figure
    # plt.savefig('Bfield.png')
    #
    # #display the plot
    # plt.show()


    #print(np.meshgrid(data[0],data[1]))


    # Creating 2-D grid of features
    [X, Y] = np.meshgrid(data[0], data[1])
    print(X)
    print(Y)

    fig, ax = plt.subplots(1, 1)

    Z = X+Y
    print(Z)


    plt.contourf(X,Y,Z,levels=100)
    plt.show()




test = [[0,5,10,15,20,25,30,35,40],[0,1,2,3,4,5,5,5,5],[.1,.1,.1],[0,1,0],[5,10,15]]
plot_Bfield(test)