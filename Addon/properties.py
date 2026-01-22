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
        name="Content File or Folder",
        description="File or Folder containing content images",
        default="",
        subtype='FILE_PATH'
    ) 

    style_folder:StringProperty(
        name="Style File or Folder",
        description="File or Folder containing style images",
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
        name="Stylization Strength",
        description="Strength of the Stylization",
        default=0.1,
        min=0.0,
        max=1.0,
        precision=2,
        subtype='FACTOR',
    )

    color_strength:FloatProperty(
        name="Color Transfer Strength",
        description="Strength of the Color Transferred from the Style Image",
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
        description="Tick to Generate a Tileable Texture",
        default=False,
        )
    
    preserve_aspect_ratio: BoolProperty(
        name="Preserve Aspect Ratio",
        description="Tick to Preserve Aspect Ratio of Content Image, Otherwise a Square Texture will be Produced",
        default=False,
        )
    
    prev_normal: BoolProperty(
        name="Preview with Normal Map",
        description="Tick to Preview the Texture Sphere with Normal Map Applied",
        default=False,
        )
    
    show_tiling: BoolProperty(
        name="Show Tiling",
        description="Preview Texture Tiling in the Image Editor",
        default=False,
        update=update_tiling_preview,
        )
    
    tiling_scale:FloatProperty(
        name="Tiling Scale",
        description="Scale of Texture on Preview Sphere",
        default=2.0,
        min=0.1,
        max=10.0,
        precision=2,
        subtype='FACTOR',
    )
    
    gen_normal: BoolProperty(
        name="Normalmap",
        description="Tick to also Generate a normal map",
        default=False,
        )
    
    is_preview: BoolProperty(
        name="Preview",
        description="Tick for Preview Mode",
        default=False,
        )
    
    is_running: BoolProperty(
        name="Is Running",
        default=False,
        )
    
    normal_strength:FloatProperty(
        name="Normal Strength",
        description="Strength of Generated Normal Map",
        default=2.0,
        min=0.0,
        max=5.0,
        precision=2,
        subtype='FACTOR',
    )

    guidance_scale:FloatProperty(
        name="Guidance Scale",
        description="Guidance Scale: High for more Artistic Results",
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
        max=200,
    )

    is_attention:BoolProperty(
        name="Attention Injection",
        description="_Switch of Attention Injection: High for following Style and Content Strictly",
        default=True,
    )

#seam blending options
    gap:FloatProperty(
        name="Seamblend width",
        description="Width of the Blended Seam in Percentage of Image Size",
        default=0.0,
        min=0.00,
        max=0.99,
    )

    blur:IntProperty(
        name="Seam Blur",
        description="Blur Strength of Seam Blending",
        default=3,
        min=1,
        max=9,
        step=2,
    )
    out_size:IntProperty(
            name="Output Size",
            description="Image Output Size, Longer edge on Non-Square Results",
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

            row = layout.row()
            row.operator("diffusest.reload_repo", text="Install Complete. Reload Repository?", icon='IMPORT')

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