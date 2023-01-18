import streamlit as st
import numpy as np
import DontTouch.func as func

class Item:
    def __init__(self, name:str, price:float, discount:float, contributers:list):
        self.name = name
        self.price = price
        self.discount = discount
        self.contributers = contributers

st.set_page_config(
    page_title="Creating reciept"
)

date = st.date_input(label="What date is the reciept from?", key = "date")
store = st.text_input(label="Store name")

nameOfReciept = "none"
if st.button(label="Create reciept"):
    nameOfReciept = func.MakeFile(date, store)


pay = st.text_input(label="Who payed for this reciept?", key = "payee", on_change=func.WriteTo)

with st.form("Recipt creator", clear_on_submit=True):
    contriTemp = st.text_input(label="Enter contributer")
    addContri = st.form_submit_button()

if addContri:
    contri.append(contriTemp)
    contri










#pay = st.text_input(label="Who payed for this reciept?", key = "payee")
# contriTemp = st.text_input(label="Who owes money on this reciept?", key = "payer")
# contri = np.array([])
# def AddContributer(contributer):
#     global contri
#     contri = np.append(contri, contributer)
# st.button(label="Add contributer", on_click= AddContributer(contriTemp))

# contri

# date = st.date_input(label="What date is the reciept from?", key = "date")

# itemAmount = st.slider(label= "Item amount", min_value=0, max_value=50)

# itemList = []
# itemListNam = []
# for i in range(itemAmount):
#     item = Item("item " + str(i+1), 0,0,"None")
#     itemList.append(item)
#     itemListNam.append([item.name, i])

# if (itemAmount == 0):
#     "You currently dont have any items..."
# else:
#     def Formatting(option):
#         return option[0]
#     throw, index = st.selectbox(label="Edit item:",options = itemListNam, format_func=Formatting)

#     "Currently editing: ", itemList[index].name
#     tempName = st.text_input(label="Name of item", placeholder= itemList[index].name)
#     tempPrice = st.text_input(label="Price of item", placeholder= itemList[index].price)
#     tempDiscount = st.text_input(label="Discount on item", placeholder= itemList[index].discount)
#     tempContributers = st.multiselect(label="Contributers", options=(pay, contri))

#     if st.button(label="Update item"):
#         itemList[index].name = tempName
#         itemList[index].price = tempPrice
#         itemList[index].discount = tempDiscount
#         itemList[index].contributers = tempContributers
#         itemListNam[index][0] = tempName
#         "Item saved!"
#         itemList[index].name, itemListNam[index][0]
#     else:
#         "Item is currently not saved"

#     itemList[index].name, itemListNam[index][0]

