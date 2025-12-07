import bpy
import os
from importlib.util import find_spec
import sys
import subprocess
from pathlib import Path
import shutil
from mathutils import *
from bpy.types import Operator
from bpy.app.translations import pgettext_iface as _
from .__init__ import get_user_modules_path
from .utils import IS_DEPENDENCIES_AVAILABLE

D = bpy.data
C = bpy.context


#helper functions

def install_dependencies():
   
    target_path = get_user_modules_path()
    #clean out old content if it´s there
    if os.path.exists(target_path):
        for item in os.listdir(target_path):
            path = os.path.join(target_path, item)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                print(f"Error cleaning up: {path}, {e}")
    # Ensure the directory exists for the installation
    if not os.path.exists(target_path):
        os.makedirs(target_path)




    #Basic setup
    import ensurepip
    ensurepip.bootstrap()

    #make sure target path is in sys path
    #Install new dependencies
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    
    if target_path not in sys.path:
        sys.path.append(target_path)

    
    #numpy
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall","-y", "numpy"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==2.2.6", "--target",target_path,"--ignore-installed", "--force-reinstall"])

    #install torch -> 2.1.0 is safest version with blender
    #cuda 121 version
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "torch==2.1.0", "torchvision==0.16.0", "torchaudio==2.1.0",
        "--index-url", "https://download.pytorch.org/whl/cu121","--target", target_path, "--no-deps", "--ignore-installed","--force-reinstall"
    ])

    #install other stuff from requirements
    #get path of requirements file
    addon_dir = os.path.dirname(__file__)
    req_path = os.path.join(addon_dir, "requirements.txt")

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", req_path,"--target", target_path, "--ignore-installed"
    ])
    
    #check if installed correctly
    try:
        import torch
        import diffusers
        print("Dependencies installed. Restart Blender.")
    except ImportError:
        print("ImportError: Dependencies not found after installation. Restart Blender.")
    except Exception as e:
        print(f"ExceptionError during final check: {e}")


def setupStyleTransferModel():

    #set an output directory
    output_dir = Path.home() / "Blender_AI_Models" / "blipdiffusion_download"
    #create directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading model to: {str(output_dir)}")
    
    try:
        import torch
        from diffusers import BlipDiffusionPipeline
        pipe = BlipDiffusionPipeline.from_pretrained("salesforce/blipdiffusion", torch_dtype=torch.bfloat16, cache_dir=str(output_dir)).to("cuda")

        pipe.save_pretrained(str(output_dir))
        print("Model downloaded")
    
    except Exception as e:
        print(f"Error occurred during download: {str(e)}")




#main operator for installing
class DIFFUSEST_OT_InstallDependencies(Operator):
    """Installs required Python packages using Blender's Python environment"""
    bl_idname = "diffusest.install_deps"
    bl_label = "Install DiffusionST Dependencies"
    

    install_success: bool = False
    
    def execute(self,context):
        install_success = False
        self.report({'INFO'}, "Starting Dependency installation. Blender will freeze temporarily.")
        addon_prefs = context.preferences.addons.get(__package__).preferences
        #check if everything works
        install_dependencies()
        try:
            import torch
            #import diffusers
            print(torch.__version__, torch.version.cuda, torch.cuda.is_available())
            print("Dependencies installed.Restart Blender.")
            install_success=True
        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"Installation failed: {e.stderr.decode('utf-8')}")
            install_success = False
        except Exception as e:
            self.report({'ERROR'}, f"An unexpected error occurred: {e}")
            install_success = False

        if install_success:
            self.report({'INFO'}, "Installation complete. **Please restart Blender** to finalize and use the add-on.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Installation failed. Check the Console for details.")
            return {'CANCELLED'}
    
class DIFFUSEST_OLT_SetupModel(Operator):
    """Download and prepare blipdiffusion model."""
    bl_idname = "diffusest.download_blip"
    bl_label = "Download blipdiffusion model"

    def execute(self,context):
        if IS_DEPENDENCIES_AVAILABLE:
            setupStyleTransferModel()
            return {'FINISHED'}
        else:
            print("Install Dependencies First.")
            return {'CANCELLED'}
    
class DIFFUSEST_OLT_RunGeneration(Operator):
    """Run the image generation process using the diffusion model."""
    bl_idname = "diffusest.run_generation"
    bl_label = "Perform style transfer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not hasattr(context.scene, 'diffusest_props'):
            self.report({'ERROR'}, "Add-on properties failed to load.")
            return {'CANCELLED'}
        
        # 1. Dependency Check: Use the global flag
        if not IS_DEPENDENCIES_AVAILABLE:
            self.report({'ERROR'}, "Dependencies are not available. Install them in Add-on Preferences and restart Blender.")
            return {'CANCELLED'}

        # ... (Rest of the generation logic placeholder)
        
        self.report({'INFO'}, "Dependencies OK. Starting generation (Model logic placeholder)...")
        return {'FINISHED'}