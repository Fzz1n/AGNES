from src.calc import ingers_equation, water_to_rice

# Test the equation Inger's formular
def test_ingers_equ_proc_larger():
    value1 = 1000
    value2 = 250
    proc1 = 450
    assert ingers_equation(value1, value2, proc1) == 112.5
    
def test_ingers_equ_100p():
    value1 = 50
    value2 = 100
    assert ingers_equation(value1, value2) == 200.0
    
def test_ingers_equ_defined_proc():
    value1 = 200
    proc1 = 100
    proc2 = 150
    assert ingers_equation(value1, None, proc1, proc2) == 300

def test_ingers_equ_failing():
    assert ingers_equation(None, None) is None
    

# Test for calc warter
def test_water_to_rice():
    input = [450, "gram"]
    assert water_to_rice(input) == f"You will need 1 liter"
    
def test_water_to_rice():
    input = [250, "gram"]
    assert water_to_rice(input) == f"You will need 112 ml"
    
def test_water_to_rice():
    input = [2, "kg"]
    assert water_to_rice(input) == f"You will need 444 liter"
    
def test_water_to_rice():
    assert water_to_rice(None) == "sorry i don't understand"