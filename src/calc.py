
# Simpel calc.
def addition(n1, n2):
    return n1 + n2
def subtraction(n1, n2):
    return n1 - n2
def multiplication(n1, n2):
    return n1 * n2
def division(n1, n2):
    return n1 / n2

# Finding the procentage of a number
def ingers_equation(value1, value2, proc1 = None, proc2 = None):
    if value1 is not None and proc1 is not None and proc2 is not None:
        return (value1 / proc1) * proc2
    elif value1 is not None and value2 is not None and proc1 is None and proc2 is None:
        proc1 = 100
        return (value2 * proc1) / value1
    elif value1 is not None and value2 is not None and proc1 is not None and proc2 is None:
        return (value2 * proc1) / value1
    return None

# Warter to rice ration calc.
def water_to_rice(info):
    if not isinstance(info, list):
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