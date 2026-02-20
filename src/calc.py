def ingers_equation(value1 = None, value2 = None, proc1 = None, proc2 = None):
    if value1 != None and proc1 == None and proc2 == None:
        return (value1 / proc1) * proc2
    elif value1 != None and value2 != None and proc1 == None and proc2 == None:
        proc1 = 100
        return (value2 * proc1) / value2
    elif value1 != None and value2 != None and proc1 != None and proc2 == None:
        return (value2 * proc1) / value1
    return None

def water_to_rice(info):
    if len(info) == 0:
        return "sorry i don't understand"
    amount = info[0]
    unit = info[1]
    warter_unit = "ml"
    benchmark_rice = 450
    benchmark_warter = 1000
    
    if unit == "kg":
        amount *= 1000
    
    amount_of_water = ingers_equation(benchmark_rice, amount, benchmark_warter)
    
    if amount_of_water >= benchmark_warter:
        amount_of_water = round(amount_of_water / benchmark_warter, 2)
        warter_unit = " liter"
    else:
        amount_of_water = int(amount_of_water)
    
    return f"You will need {amount_of_water}{warter_unit}"