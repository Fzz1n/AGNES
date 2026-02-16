def ingers_equation(value1 = None, value2 = None, proc1 = None, proc2 = None):
    # 1 case:
        # x value larger than y
            # value1 = x, value2 = y, proc1 = 100, return (value2 * proc1) / value1
    # 2 case:
        # x is valu at 100%, what is 120% more
            # v1 = x, p1 = 100, p2 = 120; return (v1 / p1) * p2
    if value1 != None and proc1 == None and proc2 == None:
        return (value1 / proc1) * proc2
    if value1 != None and value2 != None and proc1 == None and proc2 == None:
        proc1 = 100
        return (value2 * proc1) / value2
    if value1 != None and value2 != None and proc1 != None and proc2 == None:
        return (value2 * proc1) / value2
    return None

def water_to_rice(amount):
    benchmark_rice = 450
    benchmark_warter = 1000
    amount_of_water = ingers_equation(benchmark_rice, amount, benchmark_warter)
    return f"You will need {amount_of_water}ml"