import bpy
import os
import sys
from bpy.props import IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy.types import AddonPreferences
from .dependency_check import IS_DEPENDENCIES_AVAILABLE

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

    style_folder:StringProperty(
        name="Style Folder",
        description="Folder containing style images",
        default="",
        subtype='DIR_PATH'
    ) 

    strength:FloatProperty(
        name="Style Strength",
        description="Stylization strength (0.0 to 1.0)",
        default=0.8,
        min=0.0,
        max=1.0,
        precision=2,
        subtype='FACTOR',
    )

    ddim_steps:IntProperty(
        name="Stylization Steps",
        description="Number of steps for the diffusion process",
        default=50,
        min=10,
        max=150,
    )

    seed:IntProperty(
        name="Seed",
        description="The random seed for generation (-1 for random)",
        default=-1,
        min=-1,
    )

#addon Requirements in Addon Preferences -> button for installing
class DIFFUSEST_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    
    #show if installation is currently running
    is_installing: BoolProperty(
        name="Installation Running",
        default=False
    )
    

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[__package__].preferences
        
        #check installation status
        #if self.is_installing:
            #layout.separator()
            #layout.label(text="Installing Dependencies... Please wait.", icon='TIME')

            #row = layout.row()
            #row.prop(self, "is_installing", toggle=True, text="Installation in progress...", icon='PREVIEW_RANGE')
            #layout.separator()
            #return
        
        #if not self.is_installing and not IS_DEPENDENCIES_AVAILABLE:
            #box = layout.box()
            #box.label(text="Installation Complete!", icon='CHECKMARK')
            #box.label(text="**RESTART BLENDER** to load the dependencies.", icon='NONE')
            
            # Button is permanently disabled if installation is flagged as done
            #row = layout.row()
            #row.enabled = False 
            #row.operator("diffusest.install_deps", text="Dependencies Installed (Restart Required)", icon='IMPORT')
        #check installation status

        if IS_DEPENDENCIES_AVAILABLE:
            layout.label(text="Dependencies loaded and ready!", icon='CHECKMARK')

            # Button is permanently disabled
            row = layout.row()
            row.enabled = False 
            row.operator("diffusest.install_deps", text="Dependencies are Installed", icon='CHECKMARK')
        else:
            layout.label(text="Dependencies missing. Installation required", icon='ERROR')

            # Installation Button - enabled only if not installed and not installing
            row = layout.row()
            row.enabled = not IS_DEPENDENCIES_AVAILABLE and not self.is_installing
            row.operator("diffusest.install_deps", text="Install Dependencies", icon='IMPORT')

        #show path information for debugging
        layout.separator()
        layout.label(text=f"Blender Python Executable: {sys.executable}", icon='INFO')
        layout.label(text=f"Addon Path: {os.path.dirname(__file__)}", icon='ASSET_MANAGER')

#to make it accessible in the scene

def register():
        bpy.types.Scene.diffusest_props = bpy.props.PointerProperty(type=DIFFUSEST_Properties)
def unregister():
    
    if hasattr(bpy.types.Scene, 'diffusest_props'):
        del bpy.types.Scene.diffusest_props