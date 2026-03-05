import time
from src.timer import older_than_7_days

# Test larger calc related to timers 
def test_older_than_7_days_older():
    assert older_than_7_days(1) is True
    
def test_older_than_7_days_newer():
    now = time.time()
    time.sleep(1) # 1 sec timeout
    assert older_than_7_days(now) is False