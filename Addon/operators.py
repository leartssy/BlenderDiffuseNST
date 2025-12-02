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
        props = context.scene.diffusest_props

        #give warning when no images selected
        if not props.content_image:
            self.report({'ERROR'}, "Content Image not selected.")
            return {'CANCELLED'}
        if not props.style_image:
            self.report({'ERROR'}, "Style Image not selected.")
            return {'CANCELLED'}
        
        #get property settings
        content_name = props.content_image.name
        style_name = props.style_image.name
        strength = props.strength
        steps = props.ddim_steps

        return {'FINISHED'}