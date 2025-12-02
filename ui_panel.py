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

    @classmethod
    
    def draw(self, context):
        """Draws the UI elements inside Panel"""
        layout = self.layout

        row = layout.row()
        row.label(text="Image Generation Parameters")

        layout.operator("diffusest.run_generation", text="Run Style Transfer", icon='NODE')
