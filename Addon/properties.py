import bpy
from bpy.props import IntProperty, FloatProperty, PointerProperty, EnumProperty

#all the properties used by StyleTransfer
class DIFFUSEST_Properties(bpy.types.PropertyGroup):
    """Container for all Diffusion Style Transfer settings."""

    content_image: PointerProperty(
        type=bpy.types.Image,
        name="Content Image",
        description="The source content image",
    )

    style_image: PointerProperty(
        type=bpy.types.Image,
        name="Style Image",
        description="The source style image",
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

#to make it accessible in the scene

def register():
    bpy.types.Scene.diffusest_props = bpy.props.PointerProperty(type=DIFFUSEST_Properties)

def unregister():
    del bpy.types.Scene.diffusest_props