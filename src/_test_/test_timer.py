import time
from src.timer import older_than_x_days

# Test larger calc related to timers 
def test_older_than_X_days_older():
    max_days = 7
    assert older_than_x_days(1, max_days) is True
    
def test_older_than_X_days_newer():
    max_days = 5
    now = time.time()
    time.sleep(1) # 1 sec timeout
    assert older_than_x_days(now, max_days) is False