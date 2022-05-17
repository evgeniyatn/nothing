import pandas as pd
from bs4 import BeautifulSoup
import urllib3
import os
import io
from spyre import server
# Task 4
RegionDict = [
    {"label": "Vinnuts'ka", "value": 1},
    {"label": "Volyns'ka", "value": 2},
    {"label": "Dnipropetrovs'ka", "value": 3},
    {"label": "Donets'ka", "value": 4},
    {"label": "Jytomyrs'ka", "value": 5},
    {"label": "Zakarpats'ka", "value": 6},
    {"label": "Zaporiz'ka", "value": 7},
    {"label": "Ivano-Frankivs'ka", "value": 8},
    {"label": "Kyivs'ka", "value": 9},
    {"label": "Kirovograds'ka", "value": 10},
    {"label": "Lugans'ka", "value": 11},
    {"label": "Lvivs'ka", "value": 12},
    {"label": "Mykolaivs'ka", "value": 13},
    {"label": "Odes'ka", "value": 14},
    {"label": "Poltavs'ka", "value": 15},
    {"label": "Rivnens'ka", "value": 16},
    {"label": "Sums'ka", "value": 17},
    {"label": "Ternopils'ka", "value": 18},
    {"label": "Harkivs'ka", "value": 19},
    {"label": "Hersons'ka", "value": 20},
    {"label": "Hmelnyts'ka", "value": 21},
    {"label": "Cherkas'ka", "value": 22},
    {"label": "Chernivets'ka", "value": 23},
    {"label": "Chernihyvs'ka", "value": 24},
    {"label": "Krym", "value": 25}
]

def convertId(id):
    idConvertDict = {
        '22': 1, '24': 2, '23': 3, '25': 4, '3': 5, '4': 6, '3': 7, '19': 8, '20': 9, '21': 10,
        '9': 11, '9': 12, '10': 13, '11': 14, '12': 15, '13': 16, '14': 17, '15': 18, '16': 19,
        '25': 20, '17': 21, '18': 22, '1': 24, '2': 25, '5':14}
    return idConvertDict[str(id)]



class SimpleApp(server.App):
    title = "Simple App"
    inputs = [
        {
            "type": 'dropdown',
            "label": 'Data',
            "options": [{"label": "VCI", "value": "VCI"},
                        {"label": "TCI", "value": "TCI"},
                        {"label": "VHI", "value": "VHI"}],
            "key": 'ticker1',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Region',
            "options": RegionDict,
            "key": 'ticker2',
            "action_id": "update_data"
        },
        {
            "type":'text', 
            "key":"range", 
            "label":"date range",
            "value":"9-10", 
            "action_id":"simple_html_output"
        }]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Go"
    }]

    tabs = ["Plot", "Table"]
    outputs = [{"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"},
               {"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True}]
    
    def getHTML(self, params):
        range = params['range']
        return range
    def getData(self, params):
        ticker1 = params['ticker1']
        ticker2 = params['ticker2']
        range = params['range'].split("-")

        req = urllib3.PoolManager()
        vhi_url = (
            f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID="+str(convertId(ticker2))+"&year1=1981&year2=2022&type=Mean")

        res = req.request('GET', vhi_url)
        soup = BeautifulSoup(res.data, 'html.parser')
        print("Downloaded: " + soup.getText()[0:70])
        soup = soup.getText().split("\n", 1)[1].replace(
            ", ", ",").replace(",\n", "\n")
        buffer = io.StringIO(soup)
        df = pd.read_csv(filepath_or_buffer=buffer,
                         index_col="year", parse_dates=True)
        df = df.query(f"{ticker1} > 0 and week <= {range[1]} and week >= {range[0]}")
        print(df)

        return df[[ticker1]
        ]

    def getPlot(self, params):
        ticker1 = params['ticker1']
        ticker2 = params['ticker2']
        df = self.getData(params)
        print(df)

        plt_obj = df.plot()
        plt_obj.set_ylabel(ticker1)
        plt_obj.set_title("Data")
        fig = plt_obj.get_figure()

        return fig
    
app = SimpleApp()
app.launch()
