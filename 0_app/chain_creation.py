#******************************************************************************************************************************

#content       = Chain creation tool in Maya 

#version       = 0.1.1

#date          = November 9th 

#dependencies  = maya.cmds

#author        = Elizabeth Guan <yijie.beth.guan@gmail.com>

#******************************************************************************************************************************

#only GUI part done 

import maya.cmds as cmds
import os

# Construct the asset folder path based on the project root directory
def get_asset_folder():
    # Get the root project directory (without the "scenes" subfolder)
    project_dir = cmds.workspace(query=True, rootDirectory=True)
    asset_folder = os.path.join(project_dir, "assets")

    # Ensure the asset folder exists
    if not os.path.exists(asset_folder):
        os.makedirs(asset_folder)
    print(f"Asset folder path: {asset_folder}")  # Debugging path confirmation
    
    return asset_folder

# Load all FBX shapes in the asset folder
def load_default_chain_shapes():
    asset_folder = get_asset_folder()
    loaded_shapes = []
    
    for filename in os.listdir(asset_folder):
        if filename.endswith(".fbx"):
            file_path = os.path.join(asset_folder, filename)
            shape_name = os.path.splitext(filename)[0]  # Remove the .fbx extension
            if not cmds.objExists(shape_name):
                cmds.file(file_path, i=True, type="FBX")
                print(f"Loaded {shape_name} from {file_path}")  # Debug each loaded shape
                loaded_shapes.append(shape_name)
    
    print(f"Shapes loaded: {loaded_shapes}")  # Debugging loaded shapes confirmation
    return loaded_shapes

# Add new base shape and save it to the asset folder
def add_new_base_shape():
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.warning("No object selected. Please select an object to add as a base shape.")
        return
    
    shape = selection[0]
    cmds.delete(shape, ch=True)  # Delete history
    cmds.xform(shape, centerPivots=True)  # Center pivot
    cmds.move(0, 0, 0, shape)  # Move to origin

    asset_folder = get_asset_folder()
    export_path = os.path.join(asset_folder, f"{shape}.fbx")
    cmds.file(export_path, force=True, options="v=0", type="FBX export", pr=True, es=True)
    print(f"Exported {shape} to {export_path}")

    # Update the dropdown to include the new shape
    populate_shape_menu()

# Populate shape dropdown with assets from the folder
def populate_shape_menu():
    cmds.optionMenu(shape_menu, edit=True, deleteAllItems=True)
    asset_folder = get_asset_folder()

    # Load and add each FBX file as a menu item
    for filename in os.listdir(asset_folder):
        if filename.endswith(".fbx"):
            shape_name = os.path.splitext(filename)[0]
            cmds.menuItem(parent=shape_menu, label=shape_name)  # Directly add menu items to optionMenu
            print(f"Added {shape_name} to the dropdown menu")  # Debug each menu item addition

# Function to create the chain based on user input
def create_chain(shape_menu, scale_field_grp, z_offset_field, link_count_field):
    selected_shape = cmds.optionMenu(shape_menu, query=True, value=True)
    scale_x, scale_y, scale_z = cmds.floatFieldGrp(scale_field_grp, query=True, value=True)
    z_offset_percentage = cmds.floatSliderGrp(z_offset_field, query=True, value=True)
    link_count = cmds.intField(link_count_field, query=True, value=True)

    # Ensure the selected shape is loaded into the scene
    asset_folder = get_asset_folder()
    file_path = os.path.join(asset_folder, f"{selected_shape}.fbx")
    if not cmds.objExists(selected_shape) and os.path.exists(file_path):
        cmds.file(file_path, i=True, type="FBX")
    
    # Create instances with specified attributes
    bounding_box = cmds.exactWorldBoundingBox(selected_shape)
    z_length = abs(bounding_box[5] - bounding_box[2]) * scale_z
    z_offset = z_length * z_offset_percentage
    instances = []

    for i in range(link_count):
        instance = cmds.instance(selected_shape)[0]
        instances.append(instance)
        cmds.scale(scale_x, scale_y, scale_z, instance)
        rotation = 90 if i % 2 == 0 else 0
        cmds.setAttr(f"{instance}.rotateZ", rotation)
        cmds.setAttr(f"{instance}.translateZ", i * z_offset)

    print(f"Created {link_count} instances of {selected_shape}.")

# GUI function to create the chain tool interface
def create_chain_tool_gui():
    loaded_shapes = load_default_chain_shapes()  # Load shapes from asset folder
    if cmds.window("chainToolWin", exists=True):
        cmds.deleteUI("chainToolWin")

    cmds.window("chainToolWin", title="Custom Chain Tool", widthHeight=(300, 400))
    cmds.columnLayout(adjustableColumn=True)

    # Dropdown for selecting chain shape
    cmds.text(label="Select Chain Shape:")
    global shape_menu
    shape_menu = cmds.optionMenu("shapeMenu")
    populate_shape_menu()  # Populate dropdown after loading shapes

    # Button to add a new base shape
    cmds.button(label="Add New Base Shape", command=lambda _: add_new_base_shape())

    # Input fields for X, Y, Z scale
    cmds.text(label="Chain Link Scale:")
    cmds.floatFieldGrp("scaleFieldGrp", numberOfFields=3, label="Scale (X Y Z)", value1=1.0, value2=1.0, value3=1.0)

    # Input for the Z offset percentage
    z_offset_field = cmds.floatSliderGrp("zOffsetField", field=True, minValue=0, maxValue=1.0, value=0.8)

    # Integer-only input for the number of links
    cmds.text(label="Number of Links:")
    link_count_field = cmds.intField("linkCountField", value=10)

    # Button to generate the chain
    cmds.button(label="Create Chain", command=lambda _: create_chain(shape_menu, "scaleFieldGrp", z_offset_field, link_count_field))

    cmds.showWindow("chainToolWin")

# Run the GUI function to launch the tool
create_chain_tool_gui()
