import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import func
import json

contributers = []
relavantFile = "none"

sg.theme('DarkPurple3')

# All the stuff inside your window.
layout = [  [sg.Text('Welcome to the receipt calculator!')],
            [sg.Text('Begin new receipt:'), sg.Button("New")],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Exit')] ]

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
        layout2 = [[sg.Text('Please input a date:'), sg.CalendarButton("Calendar", target = "date"), sg.In(key = "date")],
                    [sg.Text("Please input a store:"), sg.InputText(key = "store")],
                    [sg.Text("Please input who payed:"), sg.InputText(key = "payer")],
                    [sg.Text("Write name of contributer:"), sg.InputText(key = "contri"), sg.Button("Add")],
                    [sg.Text("List of contributers not including payer: "), sg.Text(key = "-OUTPUT-")],
                    [sg.Button("Create receipt"), sg.Text(key = "-OUTPUT2-")],
                    [sg.Button("Add item")],
                   [sg.Button('Exit')]]

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

        if ev2 == "Create receipt":
            relavantFile = func.CreateFile(vals2["date"][:10],vals2["store"], vals2["payer"], contributers)
            win2["-OUTPUT2-"].update(f"Receipt sucessfully created, relavant file is now: {relavantFile[8:]}")
        
        if ev2 == "Add item" and not winItem_active:
            winItem_active = True
            f = open(relavantFile)
            dict = json.loads(f.read())
            showContri = [dict["payer"], *dict["contributers"]]
            newContri = []
            checkboxes = [sg.Checkbox(x) for x in showContri]
            col = [
                [sg.Text("Welcome to the item creator!")],
                [sg.Text("Name of item"), sg.Input(key = "name")],
                [sg.Text("Price of item"), sg.Input(key = "price")],
                [sg.Text("Discount on item"), sg.Input(key = "discount")],
            ]
            f.close()
            layoutItem = [
                [sg.Column(col)],
                [checkboxes, sg.Button("Add"), sg.Text(key = "-OUTPUT3-")],
                [sg.Button("Finish"), sg.Button("Exit")]
            ]

            winItem = sg.Window("Item creator", layoutItem)
        
        if winItem_active:
            ev3, vals3 = winItem.read(timeout = 100)
            if ev3 == sg.WIN_CLOSED or ev3 == 'Exit':
                winItem_active  = False
                winItem.close()
            
            if ev3 == "Add":                  
                for i, contrib in enumerate(showContri):
                    if checkboxes[i].Get():
                        if contrib not in newContri:
                            newContri.append(contrib)


                winItem["-OUTPUT3-"].update(f"List of contributers for this item: {newContri}")
            
            if ev3 == "Finish":
                func.AppendItem(vals3["name"], vals3["price"],vals3["discount"], newContri, relavantFile)
                winItem_active  = False
                winItem.close()
