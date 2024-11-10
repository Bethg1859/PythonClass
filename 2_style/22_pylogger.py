#******************************************************************************************************************************

#content       = Assignment 

#date          = November 7, 2024

#to do         = Update style

#author        = Elizabeth Guan <yijie.beth.guan@gmail.com>

#******************************************************************************************************************************

# original: logging.init.py
import os
import inspect 

UNKNOWN_FILE     = "(unknown file)"
UNKNOWN_FUNCTION = "(unknown function)"
# stored these as variables

def find_caller():
    """"
    Retrieve the file name, line number, and function name of the caller.

    Returns the file name, line number, and function name of the caller,
    or default unknown values if not found.
    
    """
    caller_info = (UNKNOWN_FILE, 0, UNKNOWN_FUNCTION)
    
    for frame_info in inspect.stack()[2:]:  
        caller_info = (frame_info.filename, frame_info.lineno, frame_info.function)
        break  
        # for loop instead of while loop

    return caller_info


