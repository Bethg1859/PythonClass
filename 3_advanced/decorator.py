#******************************************************************************************************************************

#content       = Decorator

#version       = 0.1.1

#date          = November 21th 

#author        = Elizabeth Guan <yijie.beth.guan@gmail.com>

#******************************************************************************************************************************

import time
from datetime import datetime

def print_process(func):
    def wrapper(*args, **kwargs):
        # Get function name
        func_name = func.__name__
        
        # Print start with function name
        print(f"START - {func_name}")
        print("*" * 7)
        
        # Get start time
        start_time = datetime.now()
        
        # Execute the function with its arguments
        result = func(*args, **kwargs)
        
        # Get end time and calculate duration
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Print end with duration
        print("END" + "*" * 7)
        print(f"END - {duration}")
        
        return result
    return wrapper

@print_process
def short_sleeping(name):
    time.sleep(0.1)
    print(name)

@print_process
def mid_sleeping():
    time.sleep(2)
    print("Mid sleep complete")

@print_process
def long_sleeping():
    time.sleep(4)
    print("Long sleep complete")

short_sleeping("so sleepy")
mid_sleeping()
long_sleeping()