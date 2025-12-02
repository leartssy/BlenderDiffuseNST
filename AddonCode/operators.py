import bpy
from mathutils import *
from bpy.types import Operator

D = bpy.data
C = bpy.context

#main operator for calling DiffuseST
class DIFFUSEST_OT_RunGeneration(Operator):
    """Run the image generation process"""
    bl_idname = "diffusest.run_generation"
    bl_label = "Perform style transfer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #add code logic
        return {'FINISHED'}