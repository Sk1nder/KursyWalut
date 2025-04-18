import requests
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib
import datetime as dt

typeDict = {
    "mid": "a",
    "bid": "c",
    "ask": "c"
}

titleDict = {
    "mid": "Kurs Średni",
    "bid": "Kupno",
    "ask": "Sprzedaż"
}

URL = "https://api.nbp.pl/api/exchangerates/"

matplotlib.use('Agg')
sns.set_theme()

response = requests.get(URL + "tables/C")
data = response.json()[0]
rates = data["rates"]

currencysDict = {curr["code"]: curr["currency"] for curr in data["rates"]}
currCodesList = [f"{key} - {value}" for key, value in currencysDict.items()]

def currRateMid(index):
    response = requests.get(URL + f"rates/A/{index}")
    rate = response.json()["rates"][0]['mid']
    return rate

def currRate(index):
    response = requests.get(URL + f"tables/c/today/")
    data = response.json()[0]['rates']
    for item in data:
        if item['code'] == index:
            return item


def chartData(index, typ, startDate, endDate):
    plt.close('all')
    print(f"Debug funkcji chartData: {index}, {typ}, {startDate}, {endDate}")
    df = concatData(index, typ, startDate, endDate)
    print(df)
    fig = px.line(df, x='effectiveDate', y=typ, title=titleDict[typ], template='ggplot2',
                  labels={
                      "effectiveDate": 'Data',
                      typ: titleDict[typ]
                  })
    fig.update_layout(
        dragmode=False,  # Wyłączanie zooma
        width=1600,  # Stała szerokość wykresu
        height=600,  # Stała wysokość wykresu
        xaxis=dict(
            type='category',  # Osi X traktowana jako category a nie data
            showgrid=True,  # Włączenie siatki
            gridcolor='lightgrey',  # Kolor siatki
            gridwidth=1  # Szerokość linii siatki
        ),
        yaxis=dict(
            showgrid=True,  # Włączenie siatki
            gridcolor='lightgrey',  # Kolor siatki
            gridwidth=1  # Szerokość linii siatki
        )
    )
    fig.print_grid()
    return fig

def convertDayWeek(date):
    if type(date) == str:
        stringToDT(date)
    if date.weekday() == 5:
        date = date - dt.timedelta(days=1)
    elif date.weekday() == 6:
        date = date - dt.timedelta(days=2)
    return dtToString(date)

def stringToDT(date):
    if type(date) == str:
        return dt.datetime.strptime(date, "%Y-%m-%d")
    else:
        return date

def dtToString(date):
    if type(date) == str:
        return date
    else:
        return str(dt.datetime.strftime(date, "%Y-%m-%d"))

def concatData(index, typ, startDate, endDate):
    startDate = stringToDT(startDate)
    endDate = stringToDT(endDate)
    df = pd.DataFrame()
    while endDate > startDate:
        midDate = startDate + dt.timedelta(days=93)
        if midDate > endDate:
            midDate = endDate
        print(f"rates/{typeDict[typ]}/{index}/{dtToString(startDate)}/{dtToString(midDate)}")
        response = requests.get(URL + f"rates/{typeDict[typ]}/{index}/{dtToString(startDate)}/{dtToString(midDate)}")
        df = pd.concat([df, pd.DataFrame(response.json()["rates"])], ignore_index=True)
        startDate = midDate
    return df