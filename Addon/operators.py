import bpy
import os
import sys
from mathutils import *
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper 

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
        strength = props.strength
        steps = props.ddim_steps

        return {'FINISHED'}
    
#Install dependencies

class DIFFUSEST_OLT_InstallDependencies(Operator):
    """Installs the required Python packages"""
    bl_idname = "diffusest.install_deps",
    bl_label = "Install DiffusionST Dependencies",
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        
        addon_prefs = os.path.dirname(os.path.abspath(__file__))
        #path to requirements
        requirements_path = os.path.join(addon_dir, "requirements.txt")

        #safety for when it doesn´t exist
        if not os.path.extists(requirements_path):
            self.report({'ERROR'}), "requirements.txt not found!"
            return {'CANCELLED'}
        
        #path to Blenders executable
        python_exec = sys.executable

        #installation command
        command = [
            python_exec,
            '-m', 'pip', 'install',
            '--upgrade', '--user',
            '-r', requirements_path
        ]

        self.report({'INFO'}, "Starting dependency installation...")

        #execute command
        try:
            #run installation until finish
            process = subprocess.run(command, check=True, capture_output=True, text=True)

            #check if succeeded
            if process.returncode == 0:
                addon_prefs.is_dependencies_installed = True
                self.report({'INFO'}, "Installation complete. Restart Blender.")
            else:
                self.report({'INFO'}, "Installation failed: {process.stderr}") #process.strderr = the error message
                return {'CANCELLED'}
        except subprocess.CalledProcessError as e: #typical errors
            self.report({'ERROR'}, f"Installation failed (Error Code {e.returncode}): {e.stderr}")
            return {'CANCELLED'}
        except Exception as e: #unforseen errors
            self.report({'ERROR'}, f"An unexpected error occurred during installation: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
