from src.external_services.iot.light import controlling_lights

# Test for contoling the lights from Hue bridge
def test_light_all_off():
    res = controlling_lights("kill the light")
    assert res is None
    
def test_light_valid_room():
    res = controlling_lights("turn off the light in the living room")
    assert res is None

def test_light_invalid_room():
    res = controlling_lights("turn on not a room")
    assert res == "Not a valid source"

def test_light_valid_status():
    res = controlling_lights("what's the status of the floor lamp")
    assert res is None
    
def test_light_invalid_status():
    res = controlling_lights("what's the status of the floor")
    assert res == "Not a valid source"

def test_light_valid_source():
    res = controlling_lights("turn off the floor lamp")
    assert res is None

def test_light_invalid_input():
    res = controlling_lights("turn off the floor")
    assert res == "Not a valid source"