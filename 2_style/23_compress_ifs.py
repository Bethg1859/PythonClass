#******************************************************************************************************************************

#content       = Assignment 

#date          = November 7, 2024

#to do         = Update style

#author        = Elizabeth Guan <yijie.beth.guan@gmail.com>

#******************************************************************************************************************************

import maya.cmds as mc
#VScodes keep telling me mc is not defined

def set_color(ctrlList=None, color=None):

    #instead of using if statements, I created a dictionary 
    color_map = {
        1:4,
        2:13,
        3:25,
        4:17,
        5:17,
        6:15,
        7:6,
        8:16
    }

    for ctrlName in ctrlList:
        try:
            mc.setAttr(ctrlName + 'Shape.overrideEnabled', 1)
    
            if color in color_map:
                mc.setAttr(ctrlName + 'Shape.overrideColor', color_map[color])

        except:
            pass


