import bpy
import os
import sys
from bpy.props import IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty

#all the properties used by StyleTransfer
class DIFFUSEST_Properties(bpy.types.PropertyGroup):
    """Container for all Diffusion Style Transfer settings."""

    #content_image: StringProperty(
        #type=bpy.types.Image,
        #name="Content Images Path",
        #description="The source content image",
    #)

    #style_image: StringProperty(
        #type=bpy.types.Image,
        #name="Style Images Path",
        #description="The source style image",
    #)
    content_folder: StringProperty(
        name="Content Folder",
        description="Folder containing content images",
        default="",
        subtype='DIR_PATH'
    ) 

    style_folder: StringProperty(
        name="Style Folder",
        description="Folder containing style images",
        default="",
        subtype='DIR_PATH'
    ) 

    strength: FloatProperty(
        name="Style Strength",
        description="Stylization strength (0.0 to 1.0)",
        default=0.8,
        min=0.0,
        max=1.0,
        precision=2,
        subtype='FACTOR',
    )

    ddim_steps: IntProperty(
        name="Stylization Steps",
        description="Number of steps for the diffusion process",
        default=50,
        min=10,
        max=150,
    )

    seed: IntProperty(
        name="Seed",
        description="The random seed for generation (-1 for random)",
        default=-1,
        min=-1,
    )

#addon Requirements in Addon Preferences
class DIFFUSEST_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    #check if dependencies are installed
    is_dependencies_installed: BoolProperty(
        name="Dependencies Installed",
        description="Status of required external Python libraries",
        default=False
    )

    def draw(self, context):
        layout = self.layout

        #display status
        if self.is_dependencies_installed:
            layout.label(text="Dependencies installed", icon='CHECKMARK')
        else:
            layout.label(text="Dependencies missing. Installation required", icon='ERROR')

    #Installation Button
    row = layout.row()

    row.operator("diffusest.install_deps", text="Install Dependencies", icon= 'DOWNLOAD')

    #show path information for debugging
    layout.label(text=f"Blender Python Executable: {sys.executable}", icon='INFO')
    layout.label(text=f"Addon Path: {os.path.dirname(__file__)}", icon='ASSET_MANAGER')

#to make it accessible in the scene

def register():
    bpy.types.Scene.diffusest_props = bpy.props.PointerProperty(type=DIFFUSEST_Properties)

def unregister():
    del bpy.types.Scene.diffusest_props