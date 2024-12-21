#******************************************************************************************************************************
#content       = Chain creation tool in Maya 
#version       = 0.1.5
#date          = December 21th 
#dependencies  = maya.cmds, json, PyQT, PySide2
#author        = Elizabeth Guan <yijie.beth.guan@gmail.com>
#******************************************************************************************************************************

"""
This tool will allow artists to easily create interlocked chain links in Maya through a user-friendly GUI.
Users can select from predefined chain shapes or add new custom shapes. The tool will provide options
to adjust the scale, link count, and offset of the chain elements. 

Predefined chain shapes are stored in project's asset folder.
New shapes can be added directly through one click.
"""
import os
import json
import maya.cmds as cmds

def maya_error_handler(func):
    """Decorator for handling Maya operations and errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            cmds.warning(f"Error in {func.__name__}: {str(error)}")
            return None
    return wrapper
class ChainTool:
    """Main class for the Maya Chain Tool"""

    def __init__(self):
        self.window_name      = "chainToolWin"
        self.shape_menu       = None
        self.scale_field_grp  = None
        self.z_offset_field   = None
        self.link_count_field = None
        self.config = self._load_or_create_config()

    def _load_or_create_config(self):
        """Load existing config or create a default one."""
        project_dir = cmds.workspace(query=True, rootDirectory=True)
        config_path = os.path.join(project_dir, "chain_tool_config.json")
        
        # Debug: Log the configuration file path
        print(f"[DEBUG] Configuration file path: {config_path}")
    
        default_config = {
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0},
            'z_offset_percentage': 0.8,
            'link_count': 10,
            'asset_folder': 'assets',
            'supported_formats': ['.fbx']
        }
        
        # load existing config or create a new one
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as file:
                    return json.load(file)
            except Exception as e:
                cmds.warning(f"Failed to load config file: {str(e)}. Using default configuration.")
                return default_config
        else:
            try:
                with open(config_path, 'w') as file:
                    json.dump(default_config, file, indent=4)
            except Exception as e:
                cmds.warning(f"Failed to create config file: {str(e)}")
                return default_config


    def _save_config(self):
        """Save the current configuration to the JSON file."""
        project_dir = cmds.workspace(query=True, rootDirectory=True)
        config_path = os.path.join(project_dir, "chain_tool_config.json")

        try:
            with open(config_path, 'w') as file:
                json.dump(self.config, file, indent=4)
        except Exception as e:
            cmds.warning(f"Failed to save config file: {str(e)}")

    @maya_error_handler
    def get_asset_folder(self):
        """Retrieve or create the asset folder path."""
        project_dir = cmds.workspace(query=True, rootDirectory=True)
        asset_folder = os.path.join(project_dir, self.config['asset_folder'])

        if not os.path.exists(asset_folder):
            os.makedirs(asset_folder)

        print(f"[DEBUG] Asset folder path: {asset_folder}")
        return asset_folder

    @maya_error_handler
    def populate_shape_menu(self):
        """Populate the shape dropdown menu."""
        cmds.optionMenu(self.shape_menu, edit=True, deleteAllItems=True)
        asset_folder = self.get_asset_folder()
        shapes_found = False

        for filename in os.listdir(asset_folder):
            if filename.endswith(".fbx"):
                shape_name = os.path.splitext(filename)[0]
                cmds.menuItem(parent=self.shape_menu, label=shape_name)
                shapes_found = True

        if not shapes_found:
            cmds.menuItem(parent=self.shape_menu, label="No shapes available")
            cmds.warning("No shapes found in the asset folder.")

    @maya_error_handler
    def add_new_base_shape(self):
        """Add the selected object as a new base shape."""
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.warning("No object selected. Please select an object to add as a base shape.")
            return

        shape = selection[0]
        cmds.delete(shape, constructionHistory=True)
        cmds.xform(shape, centerPivots=True)
        cmds.move(0, 0, 0, shape)
        cmds.makeIdentity(shape, apply=True, translate=True, rotate=True, scale=True, normal=False)

        # export shape as FBX to asset folder
        asset_folder = self.get_asset_folder()
        export_path  = os.path.join(asset_folder, f"{shape}.fbx")
        cmds.file(export_path, force=True, options="v=0", type="FBX export", pr=True, es=True)
        print(f"[DEBUG] Exported {shape} to {export_path}")

        # update the shape menu to include the new shape
        self.populate_shape_menu()

    @maya_error_handler
    def create_chain(self):
        """Create chain based on user input."""
        selected_shape = cmds.optionMenu(self.shape_menu, query=True, value=True)
        if not selected_shape:
            cmds.warning("No shape selected. Please select a shape from the dropdown menu.")
            return

        print(f"[DEBUG] Selected Shape: {selected_shape}")
        scale_x, scale_y, scale_z = cmds.floatFieldGrp(self.scale_field_grp, query=True, value=True)
        z_offset_percentage = cmds.floatSliderGrp(self.z_offset_field, query=True, value=True)
        link_count = cmds.intField(self.link_count_field, query=True, value=True)

        # validate user inputs
        if link_count <= 0:
            cmds.warning("Link count must be greater than 0.")
            return

        if scale_x <= 0 or scale_y <= 0 or scale_z <= 0:
            cmds.warning("Scale values must be positive.")
            return
        
        # import shape if not already in the scene
        asset_folder = self.get_asset_folder()
        file_path = os.path.join(asset_folder, f"{selected_shape}.fbx")
        if not cmds.objExists(selected_shape) and os.path.exists(file_path):
            cmds.file(file_path, i=True, type="FBX")

        # calculate offsets and create chain
        bounding_box = cmds.exactWorldBoundingBox(selected_shape)
        z_length = abs(bounding_box[5] - bounding_box[2]) * scale_z
        z_offset = z_length * z_offset_percentage

        for i in range(link_count):
            instance = cmds.instance(selected_shape)[0]
            cmds.scale(scale_x, scale_y, scale_z, instance)
            rotation = 90 if i % 2 == 0 else 0
            cmds.setAttr(f"{instance}.rotateZ", rotation)
            cmds.setAttr(f"{instance}.translateZ", i * z_offset)

        cmds.inViewMessage(
            message=f"Successfully created {link_count} instances of {selected_shape}.",
            position='midCenter',
            fade=True
        )

    def create_gui(self):
        """Create the main GUI window."""
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        cmds.window(self.window_name, title="Custom Chain Tool", widthHeight=(300, 400))
        cmds.columnLayout(adjustableColumn=True)

        cmds.text(label="Select Chain Shape:")
        self.shape_menu = cmds.optionMenu("shapeMenu")
        self.populate_shape_menu()

        cmds.button(label="Add New Base Shape", command=lambda _: self.add_new_base_shape())

        self.scale_field_grp = cmds.floatFieldGrp(
            "scaleFieldGrp",
            numberOfFields=3,
            label="Scale (X Y Z)",
            value1=self.config['scale']['x'],
            value2=self.config['scale']['y'],
            value3=self.config['scale']['z']
        )

        cmds.text(label="Z Offset Percentage:")
        self.z_offset_field = cmds.floatSliderGrp(
            "zOffsetField",
            field=True,
            minValue=0,
            maxValue=1.0,
            value=self.config['z_offset_percentage']
        )

        cmds.text(label="Number of Links:")
        self.link_count_field = cmds.intField("linkCountField", value=self.config['link_count'])

        cmds.button(label="Create Chain", command=lambda _: self.create_chain())

        cmds.showWindow(self.window_name)


def launch_chain_tool():
    """Launch the Chain Tool."""
    tool = ChainTool()
    tool.create_gui()

if __name__ == "__main__":
    launch_chain_tool()
