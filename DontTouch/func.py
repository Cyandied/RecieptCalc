def MakeFile(date, store):
    f = open(f'Receipt\{str(date)}_{store}.txt', "x")
    f.close()
    return f'{str(date)}_{store}.txt'



def WriteTo():
    global pay
    global nameOfReciept
    f = open(f'Receipt\{nameOfReciept}', "a")
    f.write(f'"Payer" : {pay}')
    f.close()
    