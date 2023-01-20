
import json
import requests

class fonts:
    header = ("","20", "bold")
    body = ("","10","")
    button = ("","10", "bold")
    input = ("","10","italic")

class Basics:
    def __init__(self, date, store, paidBy, contributers):
        self.date = date
        self.store = store
        self.paidBy = paidBy
        self.subtotal = 0
        self.contributersToPay = []
        tempContri = {}
        for contributer in contributers:
            tempContri[contributer] = 0
        self.contributersToPay.append(tempContri)
        self.items = []

class Item:
    def __init__(self, name, price, discount, contributers):
        self.name = name
        self.price = price
        self.discount = discount
        self.contributers = contributers


def IsFloat(value):
    try:
        float(value)
        return True
    except Exception:
        return False


def PullAll():
    with open('PullStuff.txt', 'r') as f:
        receipts = json.loads(f.read())
    return receipts

# def CreateFile(date, store, payer):
#     f = open(f"Receipt\{str(date)}_{store}.json", "x")
#     basics = Basics(date, store, payer).__dict__
#     f.write(json.dumps(basics))
#     f.close()
#     return f"Receipt\{str(date)}_{store}.json"

# def AppendItem(name, price, discount, contributers, relavantFile):
#     def write_json(new_data, filename= relavantFile):
#         with open(filename,'r+') as file:
#           # First we load existing data into a dict.
#             file_data = json.load(file)
#         # Join new_data with file_data inside emp_details
#             file_data["items"].append(new_data)
#         # Sets file's current position at offset.
#             file.seek(0)
#         # convert back to json.
#             json.dump(file_data, file)
 
#     # python object to be appended
#     y = Item(name, price, discount, contributers).__dict__
     
#     write_json(y)

# dict = json.loads(f.read())