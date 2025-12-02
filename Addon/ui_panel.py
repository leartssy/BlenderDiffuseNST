import bpy
from bpy.types import Panel
from mathutils import *

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
        props = context.scene.diffusest_props

        box = layout.box()
        box.label(text="Image Inputs", icon='FILE_FOLDER')
        box.prop(props, "content_folder")
        box.prop(props, "style_folder")

        box = layout.box()
        box.label(text="Generation Settings", icon='SETTINGS')
        box.prop(props, "strength")
        box.prop(props, "ddim_steps")
        box.prop(props, "seed")

        layout.separator()

        layout.operator("diffusest.run_generation", text="Run Style Transfer", icon='NODE')
