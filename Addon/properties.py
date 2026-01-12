import bpy
import os
import sys
from bpy.props import IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy.types import AddonPreferences
from .utils import IS_DEPENDENCIES_AVAILABLE, IS_MODEL_DOWNLOADED, IS_REPO_DOWNLOADED

def update_tiling_preview(self,context):
    """Toggles Tiling Preview"""
    for window in bpy.context.window_manager.windows:
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.spaces.active.show_repeat = self.show_tiling
                area.tag_redraw()

#all the properties used by StyleTransfer
class DIFFUSEST_Properties(bpy.types.PropertyGroup):
    """Container for all Diffusion Style Transfer settings."""

    content_folder: StringProperty(
        name="Content Folder/File",
        description="Folder containing content images",
        default="",
        subtype='FILE_PATH'
    ) 

    style_folder:StringProperty(
        name="Style Folder/File",
        description="Folder containing style images",
        default="",
        subtype='FILE_PATH'
    ) 

    output_folder:StringProperty(
        name="Output Folder",
        description="Folder for output images",
        default="",
        subtype='DIR_PATH'
    ) 

    strength:FloatProperty(
        name="Content Strength",
        description="Stylization strength (0.0 to 1.0)",
        default=0.8,
        min=0.0,
        max=1.0,
        precision=2,
        subtype='FACTOR',
    )

    color_strength:FloatProperty(
        name="Color Transfer Strength",
        description="Strength of the Color Transfer (0.0 to 1.0)",
        default=1.0,
        min=0.0,
        max=1.0,
        precision=2,
        subtype='FACTOR',
    )

    #was used for testing textile
    #tileability_strength:FloatProperty(
        #name="Tileability Strength",
        #description="Tileability strength (0.0 to 1.0)",
        #default=0.0,
        #min=0.0,
        #max=1.0,
        #precision=2,
        #subtype='FACTOR',
    #)
    is_tileable: BoolProperty(
        name="Tileable",
        description="Tileable Option",
        default=False,
        )
    
    preserve_aspect_ratio: BoolProperty(
        name="Preserve Aspect Ratio",
        description="Preserve Aspect Ratio of content image",
        default=False,
        )
    
    prev_normal: BoolProperty(
        name="Preview with Normal Map",
        description="Preview also Normal Map",
        default=False,
        )
    
    show_tiling: BoolProperty(
        name="Show Tiling",
        description="Repeat image in UV/Image Editor",
        default=False,
        update=update_tiling_preview,
        )
    
    tiling_scale:FloatProperty(
        name="Tiling Scale",
        description="Tiling Scale Preview (0.1 to 10.0)",
        default=2.0,
        min=0.1,
        max=10.0,
        precision=2,
        subtype='FACTOR',
    )
    
    gen_normal: BoolProperty(
        name="Normalmap",
        description="Generate a normal map",
        default=False,
        )
    
    is_running: BoolProperty(
        name="Is Running",
        default=False,
        )
    
    normal_strength:FloatProperty(
        name="Normal Strength",
        description="Normal Strength (0.0 to 5.0)",
        default=2.0,
        min=0.0,
        max=5.0,
        precision=2,
        subtype='FACTOR',
    )

    guidance_scale:FloatProperty(
        name="Guidance Scale",
        description="Guidance Scale (0.0 to 10.0)",
        default=7.5,
        min=1.1,
        max=10.0,
        precision=2,
        subtype='FACTOR',
    )

    ddim_steps:IntProperty(
        name="Stylization Steps",
        description="Number of steps for the diffusion process",
        default=50,
        min=10,
        max=250,
    )

    attention_weight:FloatProperty(
        name="Attention Injection Weight",
        description="Weight of Attention Injection",
        default=0.7,
        min=0.0,
        max=1.0,
    )

#seam blending options
    gap:FloatProperty(
        name="Seamblend width",
        description="How wide the blending of seam should be (in px, or in percentage if <1)",
        default=0.0,
        min=0.00,
        max=0.99,
    )

    blur:IntProperty(
        name="Seam Blur",
        description="Blur strength at seam, only use odd numbers",
        default=3,
        min=1,
        max=9,
        step=2,
    )
    out_size:IntProperty(
            name="Output Size",
            description="Image Output Size",
            default=2048,
            min=128,
            max=8192,
            step=128,
        )
    #only_horizontal:BoolProperty(
       # name="Disable Vertical Tiling",
        #description="Option only tile horizontally (e.g. for skyboxes)",
       # default=False,
   # )
    progress:FloatProperty(
        name="Progress",
        subtype='PERCENTAGE',
        min=0.0,
        max=100.0,
        precision=0,
    )
#for arrow dropdown panels

    # This boolean will act as our arrow toggle
    show_advanced: BoolProperty(
        name="Advanced Settings",
        description="Show extra options",
        default=False
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
        from . import utils
        prefs = context.preferences.addons[__package__].preferences
        
        is_ready = utils.IS_DEPENDENCIES_AVAILABLE and utils.IS_MODEL_DOWNLOADED and utils.IS_REPO_DOWNLOADED
    
        if is_ready:
            layout.label(text="Everything is set up correctly!", icon='CHECKMARK')

            # Button is permanently disabled
            row = layout.row()
            row.enabled = False 
            row.operator("diffusest.setup_all", text="Setup successful", icon='CHECKMARK')
        else:
            layout.label(text="Setup required. (Dependencies, Model, Repo)", icon='ERROR')

            # Installation Button - enabled only if not installed and not installing
            row = layout.row()
            row.enabled = not self.is_installing
            row.operator("diffusest.setup_all", text="Install Everything", icon='IMPORT')
        
        #information
        layout.separator()
        layout.label(text=f"Blender Python Executable: {sys.executable}", icon='INFO')
        layout.label(text=f"Addon Path: {os.path.dirname(__file__)}", icon='ASSET_MANAGER')

#to make it accessible in the scene

def register():
        bpy.types.Scene.diffusest_props = bpy.props.PointerProperty(type=DIFFUSEST_Properties)
def unregister():
    
    if hasattr(bpy.types.Scene, 'diffusest_props'):
        del bpy.types.Scene.diffusest_props