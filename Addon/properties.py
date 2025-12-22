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
        default=r"C:\Users\leaes\Documents\Studium\7. Semester\Bachelor\Bachelor Thesis\IndividualProject\Images\TrainingImages\ContentImages\Testing_Content",
        subtype='FILE_PATH'
    ) 

    style_folder:StringProperty(
        name="Style Folder",
        description="Folder containing style images",
        default=r"C:\Users\leaes\Documents\Studium\7. Semester\Bachelor\Bachelor Thesis\IndividualProject\Images\TrainingImages\StyleImages\Testing_Styles",
        subtype='FILE_PATH'
    ) 

    output_folder:StringProperty(
        name="Output Folder",
        description="Folder for output images",
        default=r"C:\Users\leaes\Documents\Studium\7. Semester\Bachelor\Bachelor Thesis\IndividualProject\Images\TrainingImages\Resulting Pictures\BlenderDiffuse\Test1",
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
        default=True,
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
        default=5.0,
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
        max=150,
    )

    seed:IntProperty(
        name="Seed",
        description="The random seed for generation (-1 for random)",
        default=-1,
        min=-1,
    )

#seam blending options
    gap:FloatProperty(
        name="Seamblend width",
        description="How wide the blending of seam should be (in px, or in percentage if <1)",
        default=0.21,
        min=0.05,
        max=100,
    )

    blur:IntProperty(
        name="Seam Blur",
        description="Blur strength at seam, only use odd numbers",
        default=7,
        min=1,
        max=9,
        step=2,
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
        #Button for downloading model
        if IS_DEPENDENCIES_AVAILABLE:
            if IS_MODEL_DOWNLOADED:
                row = layout.row()
                row.enabled =False
                row.operator("diffusest.download_blip", text = "Blipdiffusion Model already downloaded.", icon='CHECKMARK')
            else:
                row = layout.row()
                row.enabled =True
                row.operator("diffusest.download_blip", text = "Download Blipdiffusion Model.", icon='IMPORT')
        else:
            row = layout.row()
            row.enabled = False
            row.operator("diffusest.download_blip", text = "Install Dependencies first.", icon='IMPORT')
        #Button for installing repository
        layout.separator()
        if IS_DEPENDENCIES_AVAILABLE and IS_MODEL_DOWNLOADED:
            if IS_REPO_DOWNLOADED:
                row = layout.row()
                row.enabled =True
                row.operator("diffusest.download_repo", text = "Repository already downloaded, reload?", icon='CHECKMARK')
            else:
                row = layout.row()
                row.enabled =True
                row.operator("diffusest.download_repo", text = "Download DiffuseST Repository and textile.", icon='IMPORT')
        else:
            row = layout.row()
            row.enabled = False
            row.operator("diffusest.download_repo", text = "Install Dependencies and Model first.", icon='IMPORT')
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