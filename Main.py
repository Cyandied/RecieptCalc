import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import func
import json
import time

contributers = []
reciept = None

i = 0
item_index = 0
item_from_Recipt = None
subtotal = 0
showContri = None

sg.theme('DarkPurple3')

# All the stuff inside your window.
layout = [
    [sg.Text('Welcome to the receipt calculator!')],
    [sg.Text('Begin new receipt:'), sg.Button("New")],
    [sg.Text('Enter something on Row 2'), sg.InputText()],
    [sg.Button('Ok'), sg.Button('Exit')]
]

def ItemList(rcpt = reciept):

    if rcpt == None:
        return sg.Text("No items to display")
    elif len(rcpt.item) == 0: 
        return sg.Text("No items to display")
    else:
        return sg.Text("Items:")

itemList = []
layout2 = [
    [sg.Text('Please input a date:'), sg.CalendarButton("Calendar", target = "date"), sg.In(key = "date")],
    [sg.Text("Please input a store:"), sg.InputText(key = "store")],
    [sg.Text("Please input who payed:"), sg.InputText(key = "paidBy")],
    [sg.Text("Write name of contributer:"), sg.InputText(key = "contri"), sg.Button("Add")],
    [sg.Text("List of contributers not including who paid: "), sg.Text(key = "-OUTPUT-")],
    [sg.Button("Create reciept"), sg.Text(key = "-OUTPUT2-")],
    [sg.Button("Add item")],
    [ItemList(), sg.Listbox(values = itemList, size= (40,6), key = "ItemList"), sg.Button("Change item")],
    [sg.Text("Contibuters are to pay:"), sg.Text("shit",key = "ToPay"), sg.Text("Subtotal is:"), sg.Text(subtotal,key = "subtotal")],
    [sg.Button('Exit'), sg.Button("Finalize reciept")]
]

# Create the Window
win1 = sg.Window('Start', layout)

win2_active = False
winItem_active = False

while True:
    ev1, vals1 = win1.read(timeout=100)
    if ev1 == sg.WIN_CLOSED or ev1 == 'Exit':
        break

    if not win2_active and ev1 == 'New':
        win2_active = True
        win2 = sg.Window('New receipt', layout2)

    if win2_active:
        ev2, vals2 = win2.read(timeout=100)

        if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
            win2_active  = False
            win2.close()

        if ev2 == "Add":
            contributers.append(vals2["contri"])
            win2["-OUTPUT-"].update(contributers)
            win2['contri'].Update('')

        if ev2 == "Create reciept":
            showContri = [vals2["paidBy"], *contributers]
            reciept = func.Basics(vals2["date"][:10],vals2["store"], vals2["paidBy"], showContri)
            win2["-OUTPUT2-"].update(f"Receipt sucessfully created.")
        
        if ev2 == "Finalize reciept":
            item_string = ""
            for item in reciept.items:
                item_string =  f'{item_string}\n\tName: {item.name} \n\tPrice: {item.price} \n\tDiscount: {item.discount} \n\tContributers: {item.contributers} \n'
            answer = sg.popup_scrolled(f"Is the following information correct?: \nDate: {reciept.date} \nStore: {reciept.store} \nPaid by: {reciept.paidBy} \nItems: {item_string}",yes_no= True,title = "Check if into is correct")
            if answer == "Yes":
                sg.popup("Reciept pushed to external server.", button_type = sg.POPUP_BUTTONS_OK)
                print("Pushing data")
                win2_active  = False
                win2.close()
            if answer == "No":
                print("Not pushing data")
        
        if ev2 == "Add item" and not winItem_active:
            winItem_active = True
            col = [
                [sg.Text("Welcome to the item creator!")],
                [sg.Text("Name of item"), sg.Input(key = "name")],
                [sg.Text("Price of item"), sg.Input(key = "price")],
                [sg.Text("Discount on item"), sg.Input(key = "discount")]
            ]
            checkboxes = [sg.Checkbox(x) for x in showContri]
            layoutItem = [
                [sg.Column(col)],
                [checkboxes],
                [sg.Button("Finish"), sg.Button("Cancel")]
            ]
            winItem = sg.Window("Item creator", layoutItem)
        
        if ev2 == "Change item" and not winItem_active:
            if len(vals2["ItemList"]) == 0:
                sg.popup("No item was selected. \n\nPlease select an item from the list.", title = "Item selection error")
            # print(vals2["ItemList"])
            else: 
                item_index = vals2["ItemList"][0][0] - 1
                item_from_Recipt = reciept.items[item_index]

                winItem_active = True
                colEdit = [
                    [sg.Text("Welcome to the item creator!")],
                    [sg.Text("Name of item"), sg.Input(key = "nameEd", default_text = item_from_Recipt.name)],
                    [sg.Text("Price of item"), sg.Input(key = "priceEd", default_text = item_from_Recipt.price)],
                    [sg.Text("Discount on item"), sg.Input(key = "discountEd", default_text = item_from_Recipt.discount)]
                ]

                defaultCheck = []
                for option in showContri:
                    append = False
                    for name in item_from_Recipt.contributers:
                        if option == name:
                            append = not append
                    defaultCheck.append(append)
                    append = False

                checkboxes = [sg.Checkbox(x, default= defaultCheck[k]) for k,x in enumerate(showContri)]
                newContri = []
                layoutItemEditor = [
                    [sg.Column(colEdit)],
                    [checkboxes, sg.Text(key = "-OUTPUT3-")],
                    [sg.Button("Update"), sg.Button("Cancel")]
                ]
                winItem = sg.Window("Item editor", layoutItemEditor)

            



        if winItem_active:
            ev3, vals3 = winItem.read(timeout = 100)

            if ev3 == sg.WIN_CLOSED or ev3 == "Cancel":
                winItem_active  = False
                winItem.close()

                winItem["-OUTPUT3-"].update(f"List of contributers for this item: {newContri}")
            
            if ev3 == "Finish":

                if func.IsFloat(vals3["price"]) and func.IsFloat(vals3["discount"]):
                    newContri = []

                    for j, contrib in enumerate(showContri):
                        if checkboxes[j].Get():
                            newContri.append(contrib)

                    reciept.items.append(func.Item(vals3["name"], vals3["price"],vals3["discount"], newContri))
                    
                    priceTotal = float(vals3["price"]) - float(vals3["discount"])
                    sharedPrice = priceTotal/len(newContri)
                    subtotal += priceTotal
                    for contrib in newContri:
                        reciept.contributersToPay[contrib] += sharedPrice

                    i += 1

                    sg.popup("Item sucessfully added, closing item creator", auto_close=True, auto_close_duration=0.3, button_type = 5)

                    itemList.append([i,vals3["name"], vals3["price"] ,vals3["discount"], newContri])

                    win2["ItemList"].update(values = itemList)
                    win2["subtotal"].update(subtotal)

                    winItem_active  = False
                    winItem.close()
                else:
                    sg.popup_error("ERROR \nLooks like something that was supposed to be a number wasn't \nPlease check that the fields price and discunt does not have any of the following: \n\tLetters \n\tCommas, use . instead \n\tOther symbols or signs")

            
            if ev3 == "Update":
                newContri = []

                for i, contrib in enumerate(showContri):
                    if checkboxes[i].Get():
                        newContri.append(contrib)

                oldPriceTotal = float(reciept.items[item_index].price) - float(reciept.items[item_index].discount)
                newPrice = float(vals3["priceEd"]) - float(vals3["discountEd"])
                priceDiff = newPrice - oldPriceTotal



                reciept.items[item_index] = (func.Item(vals3["nameEd"], vals3["priceEd"],vals3["discountEd"], newContri))

                
                sharedPriceDiff = priceDiff/len(newContri)
                subtotal += priceDiff
                for contrib in newContri:
                    reciept.contributersToPay[contrib] += sharedPrice

                sg.popup("Item sucessfully changed, closing item creator", auto_close=True, auto_close_duration=0.3, button_type = 5)

                itemList[item_index] = [item_index + 1,vals3["nameEd"], vals3["priceEd"] ,vals3["discountEd"], newContri]

                win2["ItemList"].update(values = itemList)

                winItem_active  = False
                winItem.close()
