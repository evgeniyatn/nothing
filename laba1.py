from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
import datetime
import os
import shutil


#Task 4
def convertId(id):
    idConvertDict = {
    '22': 1, '24': 2, '23': 3, '25': 4, '3': 5, '4': 6, '3': 7, '19': 8, '20': 9, '21': 10, 
    '9': 11, '9': 12, '10': 13, '11': 14, '12': 15, '13': 16, '14': 17, '15': 18, '16': 19, 
    '25': 20, '17': 21, '18': 22, '1': 24, '2': 25 }
    return idConvertDict[str(id)]

def clearData():
    for root, dirs, files in os.walk('csv'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def saveData(id):
    req = urllib3.PoolManager()
    now = datetime.datetime.now().strftime("%H.%M.%S")
    clearData()
    
    #os.mkdir('csv')

    vhi_url = (f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={id}&year1=1981&year2=2022&type=Mean")
    res = req.request('GET', vhi_url)
    soup = BeautifulSoup(res.data, 'html.parser')
    print("Downloaded: " + soup.getText()[0:70])
    soup = soup.getText().split("\n", 1)[1].replace(", ",",")
    
    file = open(f'csv/id_{id}_{now}.csv', 'w+')
    file.write(soup.replace(",\n", "\n"))
    file.close()

def readData(path):
    return pd.read_csv(path, index_col="year", parse_dates=True)

#task 5.1
def printVHI_extremumes(df, year):
    dfByYear = df["VHI"].filter(like=str(year),axis=0)
    print(dfByYear)
    print(f"> Max: {dfByYear.max()}")
    print(f"> Min: {dfByYear.min()}")

#task 5.2
def printVHI_extremeVal(df):
    print(df.query('VHI < 15 and VHI > 0').iloc[:, 5])

#task 5.3
def printVHI_moderateVal(df):
    print(df.query('VHI < 35 and VHI > 15').iloc[:, 5])






#Saves data to csv and convert id due to ukr alphabet
saveData(convertId(1))
pd.plotting.register_matplotlib_converters()


df = readData(f'csv/{os.listdir("csv")[0]}')


#printVHI_extremumes(df, 1982)
#printVHI_extremeVal(df)
printVHI_moderateVal(df)
