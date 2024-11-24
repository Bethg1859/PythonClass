#******************************************************************************************************************************

#content       = Chain creation tool in Maya 

#version       = 0.1.2

#date          = November 9th 

#dependencies  = maya.cmds

#author        = Elizabeth Guan <yijie.beth.guan@gmail.com>

#******************************************************************************************************************************

"""
This tool will allow artists to easily create interlocked chain links in Maya through a user-friendly GUI.
Users can select from predefined chain shapes or add new custom shapes. The tool will provide options
to adjust the scale, link count, and offset of the chain elements. 

Predefined chain shapes are stored in project's asset folder.
New shapes can be added directly through one click.
"""

#!!! I only have the GUI part done, will need to work on the actual functions later#

import maya.cmds as cmds
import os

def get_asset_folder():
    project_dir  = cmds.workspace(query=True, rootDirectory=True)
    asset_folder = os.path.join(project_dir, "assets")

    #ensure the asset folder exists
    if not os.path.exists(asset_folder):
        os.makedirs(asset_folder)

<<<<<<< Updated upstream

    #debugging path confirmation
=======
    # debugging path confirmation
>>>>>>> Stashed changes
    print(f"Asset folder path: {asset_folder}")  
    
    return asset_folder


def load_default_chain_shapes():
    asset_folder = get_asset_folder()
    loaded_shapes = []
    
    for filename in os.listdir(asset_folder):

        if filename.endswith(".fbx"):
            file_path = os.path.join(asset_folder, filename)

            #remove the .fbx extension
            shape_name = os.path.splitext(filename)[0]  
            if not cmds.objExists(shape_name):
                cmds.file(file_path, i=True, type="FBX")

                #debug each loaded shape
                print(f"Loaded {shape_name} from {file_path}") 
                loaded_shapes.append(shape_name)

    #debugging loaded shapes 
    print(f"Shapes loaded: {loaded_shapes}")  
    return loaded_shapes

# add new base shape and save it to the asset folder
def add_new_base_shape():
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.warning("No object selected. Please select an object to add as a base shape.")
        return
    
    shape = selection[0]

<<<<<<< Updated upstream
    #delete history 
    cmds.delete(shape, ch=True) 

    #center pivot 
    cmds.xform(shape, centerPivots=True)  

    #move to origin
    cmds.move(0, 0, 0, shape)  

    #freeze transformation
=======
    cmds.delete(shape, constructionHistory=True) 
    cmds.xform(shape, centerPivots=True)  
    cmds.move(0, 0, 0, shape)  
>>>>>>> Stashed changes
    cmds.makeIdentity(shape, apply=True, translate=True, rotate=True, scale=True, normal=False)


    asset_folder = get_asset_folder()
    export_path = os.path.join(asset_folder, f"{shape}.fbx")
    cmds.file(export_path, force=True, options="v=0", type="FBX export", pr=True, es=True)
    print(f"Exported {shape} to {export_path}")

    #update the dropdown to include the new shape
    populate_shape_menu()

#populate shape dropdown with assets from the folder
def populate_shape_menu():
    cmds.optionMenu(shape_menu, edit=True, deleteAllItems=True)
    asset_folder = get_asset_folder()

    #load and add each FBX file as a menu item
    for filename in os.listdir(asset_folder):
        if filename.endswith(".fbx"):
            shape_name = os.path.splitext(filename)[0]

            #add menu items to optionMenu
            cmds.menuItem(parent=shape_menu, label=shape_name)  
<<<<<<< Updated upstream

            #debug each menu item addition
=======
            # debug each menu item addition
>>>>>>> Stashed changes
            print(f"Added {shape_name} to the dropdown menu")  

# function to create the chain based on user input
def create_chain(shape_menu, scale_field_grp, z_offset_field, link_count_field):
    selected_shape = cmds.optionMenu(shape_menu, query=True, value=True)
    scale_x, scale_y, scale_z = cmds.floatFieldGrp(scale_field_grp, query=True, value=True)
    z_offset_percentage = cmds.floatSliderGrp(z_offset_field, query=True, value=True)
    link_count = cmds.intField(link_count_field, query=True, value=True)

    # ensure the selected shape is loaded into the scene
    asset_folder = get_asset_folder()
    file_path    = os.path.join(asset_folder, f"{selected_shape}.fbx")
    if not cmds.objExists(selected_shape) and os.path.exists(file_path):
        cmds.file(file_path, i=True, type="FBX")
    
    # create instances with specified attributes
    bounding_box = cmds.exactWorldBoundingBox(selected_shape)
    z_length     = abs(bounding_box[5] - bounding_box[2]) * scale_z
    z_offset     = z_length * z_offset_percentage
    instances    = []

    for i in range(link_count):
        instance = cmds.instance(selected_shape)[0]
        instances.append(instance)
        cmds.scale(scale_x, scale_y, scale_z, instance)
        rotation = 90 if i % 2 == 0 else 0
        cmds.setAttr(f"{instance}.rotateZ", rotation)
        cmds.setAttr(f"{instance}.translateZ", i * z_offset)

    print(f"Created {link_count} instances of {selected_shape}.")

def create_chain_tool_gui():
<<<<<<< Updated upstream
    """
    sets up the GUI for the chain creation tool, including dropdowns, input fields, and buttons.
    """
    loaded_shapes = load_default_chain_shapes()  # Load shapes from asset folder
=======

    # Load shapes from asset folder
    loaded_shapes = load_default_chain_shapes()  
>>>>>>> Stashed changes
    if cmds.window("chainToolWin", exists=True):
        cmds.deleteUI("chainToolWin")

    cmds.window("chainToolWin", title="Custom Chain Tool", widthHeight=(300, 400))
    cmds.columnLayout(adjustableColumn=True)

    #dropdown for selecting chain shape
    cmds.text(label="Select Chain Shape:")
    global shape_menu
    shape_menu = cmds.optionMenu("shapeMenu")
    populate_shape_menu()

    #add new base shape button
    cmds.button(label="Add New Base Shape", command=lambda _: add_new_base_shape())

    #input fields for x, y, z scale
    cmds.text(label="Chain Link Scale:")
    cmds.floatFieldGrp("scaleFieldGrp", numberOfFields=3, label="Scale (X Y Z)", value1=1.0, value2=1.0, value3=1.0)

    #input z offset percentage
    z_offset_field = cmds.floatSliderGrp("zOffsetField", field=True, minValue=0, maxValue=1.0, value=0.8)

    #input for the number of links, integers only 
    cmds.text(label="Number of Links:")
    link_count_field = cmds.intField("linkCountField", value=10)

    #generate chain button
    cmds.button(label="Create Chain", command=lambda _: create_chain(shape_menu, "scaleFieldGrp", z_offset_field, link_count_field))

    cmds.showWindow("chainToolWin")

<<<<<<< Updated upstream
#launch GUI
create_chain_tool_gui()
=======
# launch GUI
create_chain_tool_gui()



>>>>>>> Stashed changes
