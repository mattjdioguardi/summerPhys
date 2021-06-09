import pandas as pd
from datetime import datetime


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





test = [[1,0,34],[0,0,0],[.1,.1,.1],[0,1,0],[5,10,15]]
saveData(test)