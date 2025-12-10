import bpy
from bpy.types import Panel
from mathutils import *
from .utils import IS_DEPENDENCIES_AVAILABLE, IS_MODEL_DOWNLOADED, IS_REPO_DOWNLOADED

D = bpy.data
C = bpy.context

class DIFFUSEST_PT_MainPanel(Panel):
    """Creates panel in UV sidebar"""
    bl_label = "DiffuseST"
    bl_idname = "DIFFUSEST_PT_MainPanel"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NST'

    def draw(self, context):
        """Draws the UI elements inside Panel"""
        layout = self.layout

        #guard clause to prevent crashing during add-on reload
        if not hasattr(context.scene, 'diffusest_props'):
            layout.label(text="Add-on loading...", icon='TIME')
            return
        
        props = context.scene.diffusest_props

        is_ready = False
        if IS_DEPENDENCIES_AVAILABLE and IS_MODEL_DOWNLOADED and IS_REPO_DOWNLOADED:
            is_ready = True
        else:
            is_ready = False

        
        box = layout.box()
        box.label(text="Image Inputs", icon='FILE_FOLDER')
        box.prop(props, "content_folder")
        box.prop(props, "style_folder")
        box.prop(props, "output_folder")

        box = layout.box()
        box.label(text="Generation Settings", icon='SETTINGS')
        box.prop(props, "strength")
        box.prop(props, "is_tileable")
        box.prop(props, "guidance_scale")
        box.prop(props, "ddim_steps")
        box.prop(props, "seed")

        layout.separator()
        row = layout.row()

        # Check dependency status and set button properties
        row.enabled = is_ready # Enable/disable the row
        row.operator("diffusest.run_generation", text="Run Style Transfer", icon='NODE')
        if not is_ready:
            row.label(text="Install all requirements in Addon Preferences", icon='INFO')
            # Show the Run button, which is disabled by the row.enabled flag
            