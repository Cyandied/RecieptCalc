
import json
import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.lines as lines
from random import uniform

relavantFile = 'PullStuff.JSON'
URL = "NoThx"
# URL = "http://192.168.1.126/api/"

storeColors = {
    "netto": "gold",
    "7-eleven":"forestgreen",
    "super brugsen":"firebrick",
    "coop 365":"limegreen",
    "føtex":"navy",
    "bilka":"dodgerblue",
    "lidl":"cornflowerblue",
    "aldi":"paleturquoise",
    "mcd":"tab:olive",
    "fakta":"limegreen",
    "ikea bistro":"royalblue",
    "circle k":"maroon"
}

class fonts:
    header = ("","20", "bold")
    body = ("","10","")
    button = ("","10", "bold")
    input = ("","10","italic")

class Basics:
    def __init__(self, date, store, paidBy, contributors):
        self.date = date
        self.store = store
        self.paidBy = paidBy
        self.subtotal = 0
        tempContri = {}
        for contributor in contributors:
            tempContri[contributor] = 0
        self.contributorToPay = tempContri
        self.items = []

class Item:
    def __init__(self, name, price, discount, contributors):
        self.name = name
        self.price = price
        self.discount = discount
        self.contributors = contributors


def IsFloat(value):
    try:
        float(value)
        return True
    except Exception:
        return False


def PullAll(id = None):
    try:
        if id == None:
            response_API = requests.get(URL,timeout=0.5)
        else:
            response_API = requests.get(URL+id,timeout=0.5)
        data = response_API.text
        receipts = json.loads(data)
    except Exception:
        with open(relavantFile, 'r') as f:
            receipts = json.loads(f.read())
            if id != None:
                receipts = [receipt for receipt in receipts if receipt["id"] == int(id)][0]

    return receipts

def WriteTo(reciept):
    try:
        requests.post(URL, json = reciept,timeout=0.5)
    except Exception:
        with open(relavantFile, 'r+') as f:
            file_data = json.load(f)

            newId = file_data[-1]["id"] + 1
            reciept["id"] = newId

            file_data.append(reciept)

            f.seek(0)

            json.dump(file_data, f, indent=4)

def TryDelete(id):
    try:
        Try = json.loads(requests.delete(URL+id).text, timeout = 0.5)
        if "error" in Try:
            return False
        else: return True
    except Exception:
        with open(relavantFile) as f:
            data = json.load(f)
        del (data[FindIndexFromId(id,data)])
        with open(relavantFile, "w") as f:
            json.dump(data, f)
        return True

def FindIndexFromId(id,data):
    for i in np.arange(0,len(data)):
        if data[i]["id"] == int(id):
            return i

def LoadAll():
    receipts = PullAll()
    listForListbox = []
    for entry in receipts:
        listItem = f'{entry["id"]}.{entry["date"]}_{entry["store"]}_{entry["subtotal"]}'
        listForListbox.append(listItem)
    return listForListbox

def FilterYMS(M,S):
    receipts = PullAll()
    listForListbox = []
    for entry in receipts:
        listItem = f'{entry["id"]}.{entry["date"]}_{entry["store"]}_{entry["subtotal"]}'
        ymd = entry["date"].split("-")
        byMonth = int(M) != 0 and int(M) == int(ymd[1])
        byStore = S != "" and S.lower() == entry["store"].lower()
        byBoth = S != "" and int(M) != 0
        if byBoth:
            if byMonth and byStore:
                listForListbox.append(listItem)
        elif byMonth:
            listForListbox.append(listItem)
        elif byStore:
            listForListbox.append(listItem)
    return listForListbox

def FilterByMonthReturnDict(M):
    receipts = PullAll()

    recieptsForMonth = []
    for entry in receipts:
        ymd = entry["date"].split("-")
        byMonth = int(M) != 0 and int(M) == int(ymd[1])
        if byMonth:
            recieptsForMonth.append(entry)
    return recieptsForMonth

def ReturnItem(id):
    receipts = PullAll(id)
    contribToPay_string = ""
    for key, value in receipts["contributorToPay"].items():
        contribToPay_string = f'{contribToPay_string}\n\t{key} is to pay {value} kr'

    item_string = ""
    for item in receipts["items"]:
        item_string =  f'{item_string}\n\tName: {item["name"]} \n\tPrice: {item["price"]} \n\tDiscount: {item["discount"]} \n\tContributors: {item["contributors"]} \n'

    receiptToShow = f'Date: {receipts["date"]} \nStore: {receipts["store"]} \nPaid by: {receipts["paidBy"]} \nSubtotal: {receipts["subtotal"]} kr \nContributors to pay: {contribToPay_string} \nItems: {item_string}'
    return receiptToShow


MonthDates = {
    "1" : 31,
    "2" : 29,
    "3" : 31,
    "4" : 30,
    "5" : 31,
    "6" : 30,
    "7" : 31,
    "8" : 31,
    "9" : 30,
    "10" : 31,
    "11" : 30,
    "12" : 31,
}

def GenByMonth(month):
    days = MonthDates[str(month)]
    monthReceipts = FilterByMonthReturnDict(month)

    if len(monthReceipts) != 0:
        stores = []
        for receipt in monthReceipts:
            store = receipt['store']
            if store.lower() not in stores:
                stores.append(store.lower())

        subtotals = {store: [0 for _ in range(days)] for store in stores}

        for receipt in monthReceipts:
            store = receipt['store']
            y, m, d = receipt['date'].split('-')
            index = int(d) - 1
            subtotal = receipt['subtotal']
            subtotals[store.lower()][index] += subtotal
        return subtotals
    else: return False

def GenerateAll():
    monthlyData ={}
    for i in range(1,13):
        monthlyData[str(i)] = GenByMonth(i)
    return monthlyData

size = (10,6)

def PlotForYear(year):
    with open(f'ReceiptsFor{year}.JSON', 'r') as f:
        dataForYear = json.loads(f.read())
    fig, ax = plt.subplots(figsize = size)
    subtotalYear = 0
    colors = []
    months = np.arange(1,13)
    viableMonths = []
    dataForMonthByStore = {}
    for month in months:
        monthData = dataForYear[str(month)]
        if monthData != False:
            viableMonths.append(month)
            allStores = monthData.keys()
            for store in allStores:
                if store not in dataForMonthByStore.keys():
                    dataForMonthByStore[store] = [0,0,0,0,0,0,0,0,0,0,0,0]
                    if store.lower() not in storeColors.keys():
                        storeColors[store.lower()] = [uniform(0,1),uniform(0,1),uniform(0,1)]
                        
                    colors.append(storeColors[store.lower()])
                monthTotal = np.sum(monthData[store])
                dataForMonthByStore[store][month-1] = monthTotal
                subtotalYear += monthTotal

    yearDataVals = []

    for storeBreakdown in dataForMonthByStore.values():
        entryVals = []
        currentBase = 0
        for monthTotal in storeBreakdown:
            currentBase += monthTotal
            entryVals.append(currentBase)
        yearDataVals.append(entryVals)

    ax.stackplot(months, yearDataVals, labels = dataForMonthByStore.keys(), colors=colors)




    ax.set_xlabel("Month")
    ax.set_ylabel("Money spent [kr.]")
    ax.set_xticks(months)
    ax.legend(loc="upper left")
    return fig, viableMonths, subtotalYear/12

def PlotForMonth(month,year,budget):
    with open(f'ReceiptsFor{year}.JSON', 'r') as f:
        dataForYear = json.loads(f.read())
    subtotalMonth = 0
    colors = []
    fig,ax = plt.subplots(figsize = size)
    monthData = dataForYear[month]
    days = np.arange(1,MonthDates[month]+1)
    for store in monthData.keys():
        colors.append(storeColors[store.lower()])
    monthDataVals = []

    for storeBreakdown in monthData.values():
        entryVals = []
        currentBase = 0
        for dayTotal in storeBreakdown:
            currentBase += dayTotal
            entryVals.append(currentBase)
        monthDataVals.append(entryVals)

    ax.add_artist(lines.Line2D([1, days[-1]], [float(budget), float(budget)], ls = "--", c="k", alpha = 0.5, label = "Budget limit"))
    ax.stackplot(days, monthDataVals, labels = monthData.keys(), colors = colors, baseline = "zero")


    for entry in monthData.values():
        subtotalMonth += np.sum(entry)

    ax.set_xlabel("Day")
    ax.set_ylabel("Money spent [kr.]")
    if subtotalMonth < float(budget):
        ax.set_ylim(0,float(budget)+500)
    ax.set_xticks(days)
    ax.legend(loc="upper left")
    return fig, subtotalMonth

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=0)
    return figure_canvas_agg

def delete_figure(figure_canvas_agg):
    figure_canvas_agg.get_tk_widget().destroy()

def EnableUpdate(viableMonths,win):
    for month in viableMonths:
        win[str(month)].update(disabled = False)