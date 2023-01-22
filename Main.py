import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import func
import json
import time

#To make it .exe
#python -m pysimplegui-exemaker.pysimplegui-exemaker

#Global variables and classes__________________________________________________

contributors = []
receipt = None
i = 0
itemIndex = 0
subtotal = 0
showContrib = None
itemList = []
prevFig = None

sg.theme('DarkGrey11')



#Layout functions and related______________________________________________________

def SayIfItems(rcpt = receipt):

    if rcpt == None:
        return sg.Text("No items to display", font = func.fonts.body)
    elif len(rcpt.item) == 0: 
        return sg.Text("No items to display", font = func.fonts.body)
    else:
        return sg.Text("Items:", font = func.fonts.body)


def Start():
    layout = [
        [sg.Text('Welcome to Budgeze!', font = func.fonts.header, justification="c")],
        [sg.Text('Your new budgeting friend!', justification="left")],
        [sg.Text('\tNew receipt:\t'), sg.Button("New", font = func.fonts.button, size=(7,1))],
        [sg.Text('\tLoad receipt:\t'), sg.Button("Load", font = func.fonts.button, size=(7,1))],
        [sg.Text('\tView statistics:\t'), sg.Button("Data", font = func.fonts.button, size=(7,1))],
        [sg.Button('Exit',font = func.fonts.button, size=(5,1))]
    ]
    return layout

def ReceiptCreate(itemList):
    layout = [
    [sg.Text('Please input a date:\t'), sg.CalendarButton("Calendar", target = "date", font = func.fonts.button, size=(9,1)), sg.In(key = "date",font=func.fonts.input, size=(40,1))],
    [sg.Text("Please input a store:\t"), sg.InputText(key = "store",font=func.fonts.input,size=(53,1))],
    [sg.Text("Please input who paid:\t"), sg.InputText(key = "paidBy",font=func.fonts.input,size=(53,1))],
    [sg.Text("Write name of contributor:\t"), sg.InputText(key = "contrib",font=func.fonts.input), sg.Button("Add", font = func.fonts.button, size=(5,1))],
    [sg.Text("List of contributors, not including who paid: ", font=func.fonts.body), sg.Text(key = "-OUTPUT-", font=func.fonts.body)],
    [sg.Button("Create receipt", key = "Create receipt", font = func.fonts.button, size=(13,1)), sg.Text(key = "-OUTPUT2-", font=func.fonts.body)],
    [sg.Button("Add item", font = func.fonts.button, disabled=True, size=(9,1))],
    [SayIfItems(), sg.Button("Edit item", font = func.fonts.button, disabled=True, size=(9,1))],
    [sg.Listbox(values = itemList, size= (80,6), key = "ItemList", font=func.fonts.body)],
    [sg.Text("Contibuters are to pay:", font=func.fonts.body), sg.Text("No contributors",key = "ToPay",font=func.fonts.input), sg.Text("Subtotal is:", font=func.fonts.body), sg.Text(subtotal,key = "subtotal",font=func.fonts.input)],
    [sg.Button('Exit', font = func.fonts.button, size=(5,1)), sg.Button("Finalize receipt", font = func.fonts.button, disabled=True, size=(15,1))]
]
    return layout

def ItemAdd(showContrib):
    col = [
        [sg.Text("Welcome to the item creator!", font=func.fonts.header)],
        [sg.Text("Name of item\t"), sg.Input(key = "name", font=func.fonts.input)],
        [sg.Text("Price of item\t"), sg.Input(key = "price", font=func.fonts.input)],
        [sg.Text("Discount on item\t"), sg.Input(key = "discount", font=func.fonts.input)]
    ]
    checkboxesItemCreator = [sg.Checkbox(x, font = func.fonts.body) for x in showContrib]

    layout = [
        [sg.Column(col)],
        [sg.Text("Check off contributors to pay for this item:")],
        [checkboxesItemCreator],
        [sg.Button("Finish", font = func.fonts.button), sg.Button("Cancel", font = func.fonts.button)]
    ]
    return checkboxesItemCreator,layout

def ItemEdit(showContrib):
    colEdit = [
        [sg.Text("Welcome to the item creator!", font=func.fonts.header)],
        [sg.Text("Name of item\t"), sg.Input(key = "nameEd", default_text = item_from_Recipt.name, font=func.fonts.input)],
        [sg.Text("Price of item\t"), sg.Input(key = "priceEd", default_text = item_from_Recipt.price, font=func.fonts.input)],
        [sg.Text("Discount on item\t"), sg.Input(key = "discountEd", default_text = item_from_Recipt.discount, font=func.fonts.input)]
    ]

    defaultCheck = []
    for option in showContrib:
        append = False
        for name in item_from_Recipt.contributors:
            if option == name:
                append = not append
        defaultCheck.append(append)
        append = False

    checkboxesItemEditor = [sg.Checkbox(x, default= defaultCheck[k], font = func.fonts.body) for k,x in enumerate(showContrib)]

    layout = [
        [sg.Column(colEdit)],
        [sg.Text("Check off contributors to pay for this item:")],
        [checkboxesItemEditor],
        [sg.Button("Update", font = func.fonts.button), sg.Button("Cancel", font = func.fonts.button)]
    ]
    return checkboxesItemEditor,layout

def Load():
    layoutL = [
        [sg.Text("You havent loaded anything yet", key = "didYouLoad")],
        [sg.Listbox(values = [], s=(40,17), key="listboxSelect", enable_events=True, font = func.fonts.body)]
    ]

    layoutR = [
        [sg.Text("Filter for month and year: "),sg.Spin([i for i in range(2023,2025)],key = "year",font=func.fonts.input, size=(10,1), initial_value=2023),sg.Spin([j for j in range(0,13)],key = "month",font=func.fonts.input, size=(10,1), initial_value=0)],
        [sg.Text("Filter for store:\t"), sg.In(key = "store",font=func.fonts.input, size=(33,1))],
        [sg.Text("Selected item:", font = func.fonts.body)],
        [sg.T(s=(5,1)),sg.Multiline(key = "showReceipt", s=(43,12), font = func.fonts.body)],
        [sg.T(s=(5,1)),sg.Button("Load all receipts", s=(15,1), font=func.fonts.button),sg.T("         or         ", font=func.fonts.body, justification = "c"),sg.Button("Apply filter", s=(10,1), font=func.fonts.button)]
    ]

    layout = [
        [sg.Text("Welcome to the receipt loader!",font = func.fonts.header)],
        [sg.Col(layoutL),sg.Col(layoutR)],
        [sg.Exit(s=(5,1), font=func.fonts.button), sg.T("", s=(12,1)),sg.Button("DELETE RECEIPT",s=(15,1), font=func.fonts.button, button_color='red')]
    ]
    return layout

def Stats():
    layoutL = [
        [sg.Canvas(s=(1000,600), key="canvas")],
        [sg.Button("Load data", font = func.fonts.button,s=(10,1)),sg.T("",s = (30,1)), sg.Button("Generate data", font = func.fonts.button,s=(14,1))],
        [sg.Exit(s=(5,1), font=func.fonts.button)]
    ]

    layoutR = [
        [sg.Text("Please select a year:"),sg.Spin([i for i in range(2023,2025)],key = "year",font=func.fonts.input, size=(10,1), initial_value=2023)],
        [sg.Text("Select month:")],
        [sg.Button(str(k+1), font = func.fonts.button, key = str(k+1), disabled=True, s = (4,1)) for k in range(6)],
        [sg.Button(str(l+1), font = func.fonts.button, key = str(l+1), disabled=True, s = (4,1)) for l in range(6,12)],
        [sg.Button("Show breakdown for entire year", font = func.fonts.button, s=(36,1), key = "evalYear")],
        [sg.T("Average spend per month:\t", font = func.fonts.body),sg.T("0", key = "avYear", font = func.fonts.input)],
        [sg.T("Spend for selected month:\t", font = func.fonts.body), sg.T("0", key = "avMonth", font = func.fonts.input)],
        [sg.T("Enter budget per month:\t", font = func.fonts.body), sg.In(default_text = "3042", key = "budget", font = func.fonts.input)]
    ]

    layout = [
        [sg.Text("Welcome to your statistics!",font = func.fonts.header)],
        [sg.Col(layoutL),sg.Col(layoutR)]
    ]
    return layout











#Build window____________________________________________________________________________________________

winStart = sg.Window('Start', Start(), font = ("Helvetica", "11", "bold"), icon="icon.ico")

winReceiptCreatorActive = False
winItemCreatorActive = False
winLoadActive = False
winDataActive = False

while True:
    #Window start____________________________________________________________________________________________
    ev1, vals1 = winStart.read(timeout=100)
    if ev1 == sg.WIN_CLOSED or ev1 == 'Exit':
        break

    elif not winReceiptCreatorActive and ev1 == 'New':
        winReceiptCreatorActive = True

        winReceiptCreator = sg.Window('New receipt', ReceiptCreate(itemList), font = ("Helvetica", "11", "bold"), icon="icon.ico")
    
    elif not winLoadActive and ev1 == "Load":
        winLoadActive = True

        winLoad = sg.Window('Load receipt', Load(), font = ("Helvetica", "11", "bold"), icon="icon.ico")
    
    elif not winDataActive and ev1 == "Data":
        winDataActive = True

        winData = sg.Window('Statistics', Stats(), font = ("Helvetica","11","bold"), icon="icon.ico").Finalize()

    #Window Data_____________________________________________________________________________________________________________
    if winDataActive:
        evData, valsData = winData.read(timeout=100)

        if evData == sg.WIN_CLOSED or evData == "Exit":
            winDataActive = False
            winData.close()
        
        if evData == "Generate data":
            answer = sg.popup_yes_no("You are about to generate all data for all receipt \nThe process might take a bit \n\nDid you mean to do this?",title="Generate data")
            if answer == "Yes":
                with open(f'ReceiptsFor{valsData["year"]}.JSON',"w") as f:
                    try:
                        f.write(json.dumps(func.GenerateAll()))
                        sg.popup("Data sucessfully generated",title = "Data generated")
                    except Exception:
                        sg.popup("Data couldnt generate",title = "ERROR data not generated")
                

        if evData == "Load data":
            if prevFig != None:
                func.delete_figure(prevFig)
            winData["canvas"]._TKcanvas = None
            figure, viableMonths, meanMonth = func.PlotForYear(valsData["year"])
            prevFig = func.draw_figure(winData['canvas'].TKCanvas, figure)
            func.EnableUpdate(viableMonths,winData)
            winData["avYear"].update(round(meanMonth,1))
            winData["avMonth"].update(0)
        
        if evData == "evalYear":
            func.delete_figure(prevFig)
            winData["canvas"]._TKcanvas = None
            figure, viableMonths, _ = func.PlotForYear(valsData["year"])
            prevFig = func.draw_figure(winData['canvas'].TKCanvas, figure)
            func.EnableUpdate(viableMonths,winData)
            winData["avMonth"].update(0)
            
        

        if evData in func.MonthDates.keys():
            month = evData
            func.delete_figure(prevFig)
            figure, totMonth = func.PlotForMonth(evData, valsData["year"], valsData["budget"])
            prevFig = func.draw_figure(winData['canvas'].TKCanvas, figure)
            winData["avMonth"].update(round(totMonth,1))



    #Window load receipt_____________________________________________________________________________
    if winLoadActive:
        evLoad, valsLoad = winLoad.read(timeout=100)

        if evLoad == sg.WIN_CLOSED or evLoad == "Exit":
            winLoadActive = False
            winLoad.close()

        elif evLoad == "listboxSelect":
            id, receiptName, *_ = valsLoad["listboxSelect"][0].split(".")
            receiptToShow = func.ReturnItem(id)
            winLoad["showReceipt"].update(receiptToShow)


        elif evLoad == "Load all receipts":
            listForListbox = func.LoadAll()
            winLoad["listboxSelect"].update(values = listForListbox)
            winLoad["didYouLoad"].update("Select receipt to view it")
            

        elif evLoad == "Apply filter":
            listForListbox = func.FilterYMS(valsLoad["month"],valsLoad["store"])
            if listForListbox == []:
                sg.popup("Sorry, no receips were found \nIf you belive this to be a mistake, please check if your spelling and the month requested \n\nIf you wish to veiw all receips, press 'Load all receipts'", button_type=sg.POPUP_BUTTONS_OK, title = "No receipts")

            winLoad["listboxSelect"].update(values = listForListbox)
            winLoad["didYouLoad"].update("Select receipt to view it")

        elif evLoad == "DELETE RECEIPT" :
            selectedReceipt = valsLoad["listboxSelect"]
            if selectedReceipt != []:
                id, receiptName, *_ = selectedReceipt[0].split(".")
                answer = sg.popup(f'Are you sure you wish to delete the following receipt: {receiptName} ?', button_type=sg.POPUP_BUTTONS_YES_NO)
                if answer == "Yes":
                    if func.TryDelete(id):
                        sg.popup("Deletion success!", button_type=sg.POPUP_BUTTONS_OK, title = "Success!")
                        winLoad["listboxSelect"].update(values = func.LoadAll())
                    else: sg.popup("Deletion failed!", button_type=sg.POPUP_BUTTONS_OK, title = "Failed!")
                else: sg.popup("Receipt not deleted", title = "Cancel deletion", button_type=sg.POPUP_BUTTONS_OK)
            else: 
                sg.popup("No receipt to delete \nPlease select a receipt from the list first", title = "No receipt", button_type=sg.POPUP_BUTTONS_OK)
                winLoad["listboxSelect"].update(values = func.LoadAll())
            
                





    #Window receipt calculator______________________________________________________________________________

    if winReceiptCreatorActive:
        ev2, vals2 = winReceiptCreator.read(timeout=100)

        if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
            contributors = []
            receipt = None
            i = 0
            itemIndex = 0
            item_from_Recipt = None
            subtotal = 0
            showContrib = None
            itemList = []
            winReceiptCreatorActive  = False
            winReceiptCreator.close()

        elif ev2 == "Add":
            contributors.append(vals2["contrib"])
            winReceiptCreator["-OUTPUT-"].update(contributors)
            winReceiptCreator['contrib'].Update('')

        elif ev2 == "Create receipt":
            if receipt == None:
                showContrib = [vals2["paidBy"], *contributors]
                receipt = func.Basics(vals2["date"][:10],vals2["store"], vals2["paidBy"], showContrib)

                winReceiptCreator["ToPay"].update(receipt.contributorToPay)
                winReceiptCreator["-OUTPUT2-"].update(f"Receipt is now active\nBegin adding items")
                winReceiptCreator["Create receipt"].update("Update receipt")
                winReceiptCreator["Finalize receipt"].update(disabled = False)
                winReceiptCreator["Add item"].update(disabled = False)

            else: 
                answer = sg.popup("Looks like you already have a receipt created, do you wish to update that one?\n\n\tThis will not delete your items. \n\nIf you have added too many contributors, the offending contributor will be removed later, so long they are set to pay 0 kr", button_type = sg.POPUP_BUTTONS_YES_NO)
                if answer == "Yes":
                    newContribs = []
                    for name in contributors:
                        if name not in showContrib:
                            newContribs.append(name)
                    receipt.date = vals2["date"][:10]
                    receipt.store = vals2["store"]
                    if receipt.paidBy != vals2["paidBy"]:
                        contributors.append(receipt.paidBy)
                        receipt.paidBy = vals2["paidBy"]
                        receipt.contributorToPay[receipt.paidBy] = 0
                    for name in newContribs:
                        receipt.contributorToPay[name] = 0
                    showContrib = [vals2["paidBy"], *contributors]
                    winReceiptCreator["-OUTPUT-"].update(contributors)
                    winReceiptCreator["ToPay"].update(receipt.contributorToPay)


        
        elif ev2 == "Finalize receipt":
            receipt.subtotal = round(subtotal,2)
            item_string = ""
            contribToPay_string = ""
            toRemove = []
            for contribName in receipt.contributorToPay:
                if receipt.contributorToPay[contribName] == 0:
                    toRemove.append(contribName)
                else:
                    contribToPay_string = f"{contribToPay_string}\n\t{contribName} is to pay {receipt.contributorToPay[contribName]} kr"
            if toRemove != []: 
                for useless in toRemove:
                    receipt.contributorToPay.pop(useless)
            for item in receipt.items:
                item_string =  f'{item_string}\n\tName: {item.name} \n\tPrice: {item.price} \n\tDiscount: {item.discount} \n\tContributors: {item.contributors} \n'
            answer = sg.popup_scrolled(f"Is the following information correct?: \nDate: {receipt.date} \nStore: {receipt.store} \nPaid by: {receipt.paidBy} \nSubtotal: {receipt.subtotal} kr \nContributors to pay: {contribToPay_string} \nItems: {item_string}",yes_no= True, title= "Overview")
            if answer == "Yes":
                for id in range(len(receipt.items)):
                    receipt.items[id] = receipt.items[id].__dict__
                receiptDict = receipt.__dict__
                func.WriteTo(receiptDict)
                sg.popup("Receipt saved, closing receipt creator", button_type = sg.POPUP_BUTTONS_OK, title = "Success!")
                contributors = []
                receipt = None
                i = 0
                itemIndex = 0
                item_from_Recipt = None
                subtotal = 0
                showContrib = None
                winReceiptCreatorActive  = False
                itemList = []
                winReceiptCreator.close()
            elif answer == "No":
                if toRemove != []: 
                    for useless in toRemove:
                        receipt.contributorToPay[useless] = 0
        
        elif ev2 == "Add item" and not winItemCreatorActive:
            winItemCreatorActive = True
            checkboxesItemCreator, layoutAddItem = ItemAdd(showContrib)
            winItemCreator = sg.Window("Item creator", layoutAddItem, font = ("Helvetica", "11", "bold"), icon="icon.ico")
        
        elif ev2 == "Edit item" and not winItemCreatorActive:
            if len(vals2["ItemList"]) == 0:
                sg.popup("No item was selected \n\nPlease select an item from the list", title = "ERROR no item selected")
            else: 
                itemIndex = vals2["ItemList"][0][0] - 1
                item_from_Recipt = receipt.items[itemIndex]
                newContrib = []
                winItemCreatorActive = True
                checkboxesItemEditor, layoutEditItem = ItemEdit(showContrib)
                winItemCreator = sg.Window("Item editor", layoutEditItem, font = ("Helvetica", "11", "bold"), icon="icon.ico")

            

        #Window Item creator______________________________________________________________________________

        if winItemCreatorActive:
            ev3, vals3 = winItemCreator.read(timeout = 100)

            if ev3 == sg.WIN_CLOSED or ev3 == "Cancel":
                winItemCreatorActive  = False
                winItemCreator.close()

            
            elif ev3 == "Finish":
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
                            receipt.contributorToPay[contrib] += round(sharedPrice,1)

                        i += 1

                        itemList.append([i,vals3["name"], vals3["price"] ,vals3["discount"], newContrib])

                        winReceiptCreator["ItemList"].update(values = itemList)
                        winReceiptCreator["subtotal"].update(subtotal)
                        winReceiptCreator["ToPay"].update(receipt.contributorToPay)
                        winReceiptCreator["Edit item"].update(disabled = False)

                        winItemCreatorActive  = False
                        winItemCreator.close()
                    else: sg.popup("No contributors chosen \n\nPlease check off at least one contributor", title = "ERROR no contributors")
                else:
                    sg.popup("Invalid characters in number exclusive fields \n\nPlease check that the fields price and discount does not contain any of the following: \n\tLetters \n\tCommas, use . instead \n\tOther non numbers", title = "ERROR invalid entry")

            
            elif ev3 == "Update":
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
                    oldContrib = receipt.items[itemIndex].contributors
                    oldSharedPrice = oldPriceTotal/len(oldContrib)
                    priceDiff = newPrice - oldPriceTotal

                    for contrib in oldContrib:
                        receipt.contributorToPay[contrib] -= round(oldSharedPrice,1)

                    receipt.items[itemIndex] = (func.Item(vals3["nameEd"], vals3["priceEd"],vals3["discountEd"], newContrib))

                    
                    newSharedPrice = newPrice/len(newContrib)
                    subtotal += priceDiff

                    for contrib in newContrib:
                        receipt.contributorToPay[contrib] += round(newSharedPrice,1)

                    itemList[itemIndex] = [itemIndex + 1,vals3["nameEd"], vals3["priceEd"] ,vals3["discountEd"], newContrib]

                    winReceiptCreator["ItemList"].update(values = itemList)
                    winReceiptCreator["subtotal"].update(subtotal)
                    winReceiptCreator["ToPay"].update(receipt.contributorToPay)

                    winItemCreatorActive  = False
                    winItemCreator.close()
                else:
                    sg.popup_error("ERROR \nLooks like something that was supposed to be a number wasn't \nPlease check that the fields price and discunt does not have any of the following: \n\tLetters \n\tCommas, use . instead \n\tOther non numbers", title = "ERROR invalid entry")
