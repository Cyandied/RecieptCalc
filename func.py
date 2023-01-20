
import json
import requests

relavantFile = 'PullStuff.JSON'

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


def PullAll():
    with open(relavantFile, 'r') as f:
        receipts = json.loads(f.read())
    return receipts

def WriteTo(reciept):
    with open(relavantFile, 'r+') as f:
        file_data = json.load(f)

        file_data.append(reciept)

        f.seek(0)

        json.dump(file_data, f, indent=4)

def LoadAll():
    receipts = PullAll()
    listForListbox = []
    runNr = 0
    for entry in receipts:
        runNr +=1
        listItem = f'{runNr}.{entry["date"]}_{entry["store"]}_{entry["subtotal"]}'
        listForListbox.append(listItem)
    return listForListbox

def FilterYMS(M,S):
    receipts = PullAll()
    listForListbox = []
    runNr = 0
    for entry in receipts:
        runNr +=1
        listItem = f'{runNr}.{entry["date"]}_{entry["store"]}_{entry["subtotal"]}'
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

def ReturnItem(id):
    receipts = PullAll()
    contribToPay_string = ""
    for key, value in receipts[id]["contributorToPay"].items():
        contribToPay_string = f'{contribToPay_string}\n\t{key} is to pay {value} kr'

    item_string = ""
    for item in receipts[id]["items"]:
        item_string =  f'{item_string}\n\tName: {item["name"]} \n\tPrice: {item["price"]} \n\tDiscount: {item["discount"]} \n\tContributors: {item["contributors"]} \n'

    receiptToShow = f'Date: {receipts[id]["date"]} \nStore: {receipts[id]["store"]} \nPaid by: {receipts[id]["paidBy"]} \nSubtotal: {receipts[id]["subtotal"]} kr \nContributors to pay: {contribToPay_string} \nItems: {item_string}'
    return receiptToShow
