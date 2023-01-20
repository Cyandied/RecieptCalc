import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import func
import json
import time

contributers = []
receipt = None
i = 0
itemIndex = 0
subtotal = 0
showContrib = None
itemList = []

sg.theme('DarkGrey11')

class fonts:
    header = ("","20", "bold")
    body = ("","10","")
    button = ("","10", "bold")
    input = ("","10","italic")

# All the stuff inside your window.
layoutStart = [
    [sg.Text('Welcome to the receipt calculator!', font = fonts.header)],
    [sg.Text('\tBegin new receipt:'), sg.Button("New", font = fonts.button)],
    [sg.Button('Exit',font = fonts.button)]
]

def ItemList(rcpt = receipt):

    if rcpt == None:
        return sg.Text("No items to display", font = fonts.body)
    elif len(rcpt.item) == 0: 
        return sg.Text("No items to display", font = fonts.body)
    else:
        return sg.Text("Items:", font = fonts.body)




# Create the Window
winStart = sg.Window('Start', layoutStart, font = ("Helvetica", "11", "bold"))

winReceiptCreatorActive = False
winItemCreatorActive = False

while True:
    ev1, vals1 = winStart.read(timeout=100)
    if ev1 == sg.WIN_CLOSED or ev1 == 'Exit':
        break

    if not winReceiptCreatorActive and ev1 == 'New':
        winReceiptCreatorActive = True
        layoutReceiptCreator = [
            [sg.Text('Please input a date:\t'), sg.CalendarButton("Calendar", target = "date", font = fonts.button, size=(10,1)), sg.In(key = "date",font=fonts.input, size=(39,1))],
            [sg.Text("Please input a store:\t"), sg.InputText(key = "store",font=fonts.input,size=(53,1))],
            [sg.Text("Please input who payed:\t"), sg.InputText(key = "paidBy",font=fonts.input,size=(53,1))],
            [sg.Text("Write name of contributer:\t"), sg.InputText(key = "contrib",font=fonts.input), sg.Button("Add", font = fonts.button, size=(5,1))],
            [sg.Text("List of contributers, not including who paid: ", font=fonts.body), sg.Text(key = "-OUTPUT-", font=fonts.body)],
            [sg.Button("Create receipt", key = "Create receipt", font = fonts.button), sg.Text(key = "-OUTPUT2-", font=fonts.body)],
            [sg.Button("Add item", font = fonts.button, disabled=True)],
            [ItemList(), sg.Button("Change item", font = fonts.button, disabled=True)],
            [sg.Listbox(values = itemList, size= (80,6), key = "ItemList", font=fonts.body)],
            [sg.Text("Contibuters are to pay:", font=fonts.body), sg.Text("No contributers",key = "ToPay",font=fonts.input), sg.Text("Subtotal is:", font=fonts.body), sg.Text(subtotal,key = "subtotal",font=fonts.input)],
            [sg.Button('Exit', font = fonts.button), sg.Button("Finalize receipt", font = fonts.button, disabled=True)]
        ]
        winReceiptCreator = sg.Window('New receipt', layoutReceiptCreator, font = ("Helvetica", "11", "bold"))

    if winReceiptCreatorActive:
        ev2, vals2 = winReceiptCreator.read(timeout=100)

        if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
            contributers = []
            receipt = None
            i = 0
            itemIndex = 0
            item_from_Recipt = None
            subtotal = 0
            showContrib = None
            itemList = []
            winReceiptCreatorActive  = False
            winReceiptCreator.close()

        if ev2 == "Add":
            contributers.append(vals2["contrib"])
            winReceiptCreator["-OUTPUT-"].update(contributers)
            winReceiptCreator['contrib'].Update('')

        if ev2 == "Create receipt":
            if receipt == None:
                showContrib = [vals2["paidBy"], *contributers]
                receipt = func.Basics(vals2["date"][:10],vals2["store"], vals2["paidBy"], showContrib)

                winReceiptCreator["ToPay"].update(receipt.contributersToPay[0])
                winReceiptCreator["-OUTPUT2-"].update(f"Receipt is now active\nBegin adding items")
                winReceiptCreator["Create receipt"].update("Update receipt")
                winReceiptCreator["Finalize receipt"].update(disabled = False)
                winReceiptCreator["Add item"].update(disabled = False)

            else: 
                answer = sg.popup("Looks like you already have a receipt created, do you wish to update that one?\n\n\tThis will not delete your items. \n\nIf you have added too many contributers, the offending contributer will be removed later, so long they are set to pay 0 kr", button_type = sg.POPUP_BUTTONS_YES_NO)
                if answer == "Yes":
                    newContribs = []
                    for name in contributers:
                        if name not in showContrib:
                            newContribs.append(name)
                    receipt.date = vals2["date"][:10]
                    receipt.store = vals2["store"]
                    if receipt.paidBy != vals2["paidBy"]:
                        contributers.append(receipt.paidBy)
                        receipt.paidBy = vals2["paidBy"]
                        receipt.contributersToPay[0][receipt.paidBy] = 0
                    for name in newContribs:
                        receipt.contributersToPay[0][name] = 0
                    showContrib = [vals2["paidBy"], *contributers]
                    winReceiptCreator["-OUTPUT-"].update(contributers)
                    winReceiptCreator["ToPay"].update(receipt.contributersToPay[0])


        
        if ev2 == "Finalize receipt":
            receipt.subtotal = subtotal
            item_string = ""
            contribToPay_string = ""
            toRemove = []
            for contribName in receipt.contributersToPay[0]:
                if receipt.contributersToPay[0][contribName] == 0:
                    toRemove.append(contribName)
                else:
                    contribToPay_string = f"{contribToPay_string}\n\t{contribName} is to pay {receipt.contributersToPay[0][contribName]} kr"
            if toRemove != []: 
                for useless in toRemove:
                    receipt.contributersToPay[0].pop(useless)
            for item in receipt.items:
                item_string =  f'{item_string}\n\tName: {item.name} \n\tPrice: {item.price} \n\tDiscount: {item.discount} \n\tContributers: {item.contributers} \n'
            answer = sg.popup_scrolled(f"Is the following information correct?: \nDate: {receipt.date} \nStore: {receipt.store} \nPaid by: {receipt.paidBy} \nSubtotal: {receipt.subtotal} kr \nContributers to pay: {contribToPay_string} \nItems: {item_string}",yes_no= True, title= "Overview")
            if answer == "Yes":
                sg.popup("This feature isnt ready yet, receipt deleted.", button_type = sg.POPUP_BUTTONS_OK, title = "Woops :(")
                contributers = []
                receipt = None
                i = 0
                itemIndex = 0
                item_from_Recipt = None
                subtotal = 0
                showContrib = None
                winReceiptCreatorActive  = False
                itemList = []
                winReceiptCreator.close()
            if answer == "No":
                if toRemove != []: 
                    for useless in toRemove:
                        receipt.contributersToPay[0][useless] = 0
        
        if ev2 == "Add item" and not winItemCreatorActive:
            winItemCreatorActive = True
            col = [
                [sg.Text("Welcome to the item creator!", font=fonts.header)],
                [sg.Text("Name of item\t"), sg.Input(key = "name", font=fonts.input)],
                [sg.Text("Price of item\t"), sg.Input(key = "price", font=fonts.input)],
                [sg.Text("Discount on item\t"), sg.Input(key = "discount", font=fonts.input)]
            ]
            checkboxesItemCreator = [sg.Checkbox(x, font = fonts.body) for x in showContrib]
            layoutItemCreator = [
                [sg.Column(col)],
                [sg.Text("Check off contributers to pay for this item:")],
                [checkboxesItemCreator],
                [sg.Button("Finish", font = fonts.button), sg.Button("Cancel", font = fonts.button)]
            ]
            winItemCreator = sg.Window("Item creator", layoutItemCreator, font = ("Helvetica", "11", "bold"))
        
        if ev2 == "Change item" and not winItemCreatorActive:
            if len(vals2["ItemList"]) == 0:
                sg.popup("No item was selected \n\nPlease select an item from the list", title = "ERROR no item selected")
            # print(vals2["ItemList"])
            else: 
                itemIndex = vals2["ItemList"][0][0] - 1
                item_from_Recipt = receipt.items[itemIndex]

                winItemCreatorActive = True
                colEdit = [
                    [sg.Text("Welcome to the item creator!", font=fonts.header)],
                    [sg.Text("Name of item\t"), sg.Input(key = "nameEd", default_text = item_from_Recipt.name, font=fonts.input)],
                    [sg.Text("Price of item\t"), sg.Input(key = "priceEd", default_text = item_from_Recipt.price, font=fonts.input)],
                    [sg.Text("Discount on item\t"), sg.Input(key = "discountEd", default_text = item_from_Recipt.discount, font=fonts.input)]
                ]

                defaultCheck = []
                for option in showContrib:
                    append = False
                    for name in item_from_Recipt.contributers:
                        if option == name:
                            append = not append
                    defaultCheck.append(append)
                    append = False

                checkboxesItemEditor = [sg.Checkbox(x, default= defaultCheck[k], font = fonts.body) for k,x in enumerate(showContrib)]
                newContrib = []
                layoutItemEditor = [
                    [sg.Column(colEdit)],
                    [sg.Text("Check off contributers to pay for this item:")],
                    [checkboxesItemEditor],
                    [sg.Button("Update", font = fonts.button), sg.Button("Cancel", font = fonts.button)]
                ]
                winItemCreator = sg.Window("Item editor", layoutItemEditor, font = ("Helvetica", "11", "bold"))

            



        if winItemCreatorActive:
            ev3, vals3 = winItemCreator.read(timeout = 100)

            if ev3 == sg.WIN_CLOSED or ev3 == "Cancel":
                winItemCreatorActive  = False
                winItemCreator.close()

            
            if ev3 == "Finish":
                if vals3["discount"] == '':
                    vals3["discount"] = 0

                if func.IsFloat(vals3["price"]) and func.IsFloat(vals3["discount"]):

                    vals3["price"] = np.sqrt(float(vals3["price"])**2)
                    vals3["discount"] = np.sqrt(float(vals3["discount"])**2)

                    newContrib = []

                    
                    for j, contrib in enumerate(showContrib):
                        if checkboxesItemCreator[j].Get():
                            newContrib.append(contrib)

                    if newContrib != []:

                        receipt.items.append(func.Item(vals3["name"], vals3["price"],vals3["discount"], newContrib))
                        
                        priceTotal = float(vals3["price"]) - float(vals3["discount"])
                        sharedPrice = priceTotal/len(newContrib)
                        subtotal += priceTotal
                        for contrib in newContrib:
                            receipt.contributersToPay[0][contrib] += round(sharedPrice,1)

                        i += 1

                        itemList.append([i,vals3["name"], vals3["price"] ,vals3["discount"], newContrib])

                        winReceiptCreator["ItemList"].update(values = itemList)
                        winReceiptCreator["subtotal"].update(subtotal)
                        winReceiptCreator["ToPay"].update(receipt.contributersToPay[0])
                        winReceiptCreator["Change item"].update(disabled = False)

                        winItemCreatorActive  = False
                        winItemCreator.close()
                    else: sg.popup("No contributers chosen \n\nPlease check off at least one contributer", title = "ERROR no contributers")
                else:
                    sg.popup("Invalid characters in number exclusive fields \n\nPlease check that the fields price and discount does not contain any of the following: \n\tLetters \n\tCommas, use . instead \n\tOther non numbers", title = "ERROR invalid entry")

            
            if ev3 == "Update":
                if vals3["discountEd"] == '':
                    vals3["discountEd"] = 0

                if func.IsFloat(vals3["priceEd"]) and func.IsFloat(vals3["discountEd"]):
                    vals3["priceEd"] = np.sqrt(float(vals3["priceEd"])**2)
                    vals3["discountEd"] = np.sqrt(float(vals3["discountEd"])**2)

                    newContrib = []

                    for j, contrib in enumerate(showContrib):
                        if checkboxesItemEditor[j].Get():
                            newContrib.append(contrib)
                    
                    

                    oldPriceTotal = float(receipt.items[itemIndex].price) - float(receipt.items[itemIndex].discount)
                    newPrice = float(vals3["priceEd"]) - float(vals3["discountEd"])
                    oldContrib = receipt.items[itemIndex].contributers
                    oldSharedPrice = oldPriceTotal/len(oldContrib)
                    priceDiff = newPrice - oldPriceTotal

                    for contrib in oldContrib:
                        receipt.contributersToPay[0][contrib] -= round(oldSharedPrice,1)

                    print(oldContrib, newContrib, receipt.contributersToPay[0])

                    receipt.items[itemIndex] = (func.Item(vals3["nameEd"], vals3["priceEd"],vals3["discountEd"], newContrib))

                    
                    newSharedPrice = newPrice/len(newContrib)
                    subtotal += priceDiff

                    print(f"Old = {oldPriceTotal}, new = {newPrice}, diff = {priceDiff},oldShared = {oldSharedPrice}, newShared = {newSharedPrice}")

                    for contrib in newContrib:
                        receipt.contributersToPay[0][contrib] += round(newSharedPrice,1)

                    sg.popup("Item sucessfully changed, closing item creator", auto_close=True, auto_close_duration=0.3, button_type = 5)

                    itemList[itemIndex] = [itemIndex + 1,vals3["nameEd"], vals3["priceEd"] ,vals3["discountEd"], newContrib]

                    winReceiptCreator["ItemList"].update(values = itemList)
                    winReceiptCreator["subtotal"].update(subtotal)
                    winReceiptCreator["ToPay"].update(receipt.contributersToPay[0])

                    winItemCreatorActive  = False
                    winItemCreator.close()
                else:
                    sg.popup_error("ERROR \nLooks like something that was supposed to be a number wasn't \nPlease check that the fields price and discunt does not have any of the following: \n\tLetters \n\tCommas, use . instead \n\tOther non numbers", title = "ERROR invalid entry")
