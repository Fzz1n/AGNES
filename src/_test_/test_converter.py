import src.converter

def test_get_time():
    text = "30 minutes"
    res = src.converter.get_time(text)
    assert res == 30 * 60