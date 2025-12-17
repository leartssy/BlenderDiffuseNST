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
from .utils import *
from .main import *

D = bpy.data
C = bpy.context


#helper functions
def show_dependencies():
    command_list = [sys.executable, "-m", "pipdeptree"]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pipdeptree", "ipython"])
    from IPython import display
    display.clear_output()
    addon_env = os.environ.copy()
    addon_env['PYTHONPATH'] = MODULES_PATH
    result = subprocess.run(command_list,env=addon_env,capture_output=True, text=True, check=True)
    print("--- Dependency Tree ---")
    print(result.stdout)

def install_dependencies():
    
    target_path = get_user_modules_path()
    #clean out old content if it´s there
    #if os.path.exists(target_path):
     #   for item in os.listdir(target_path):
      #      path = os.path.join(target_path, item)
       #     try:
        #        if os.path.isdir(path):
         #           shutil.rmtree(path)
          #      else:
           #         os.remove(path)
            #except Exception as e:
             #   print(f"Error cleaning up: {path}, {e}")
    # Ensure the directory exists for the installation
    if not os.path.exists(target_path):
        os.makedirs(target_path)




    #Basic setup
    import ensurepip
    ensurepip.bootstrap()

    #make sure target path is in sys path
    #Install new dependencies
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    #subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])

    
    if target_path not in sys.path:
        sys.path.append(target_path)

    
    #numpy
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall","-y", "numpy"])
    subprocess.check_call([sys.executable, "-m", "pip", "install","--upgrade", "numpy==2.2.6", "--target",target_path,"--ignore-installed", "--force-reinstall"])

    #install torch -> 2.1.0 is safest version with blender
    #cuda 121 version
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "torch==2.5.1", "torchvision", "torchaudio",
        "--index-url", "https://download.pytorch.org/whl/cu121","--target", target_path, "--no-deps", "--ignore-installed","--upgrade"
    ])

    #install other stuff from requirements
    #get path of requirements file
    addon_dir = os.path.dirname(__file__)
    req_path = os.path.join(addon_dir, "requirements.txt")

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", req_path,"--target", target_path, "--ignore-installed"
    ])
    show_dependencies()
    #check if installed correctly
    try:
        check_dependencies()
        print("Dependencies installed. Restart Blender.")
    except ImportError:
        print("ImportError: Dependencies not found after installation. Restart Blender.")
    except Exception as e:
        print(f"ExceptionError during final check: {e}")


def setupStyleTransferModel():
    #Download the model

    #set an output directory
    output_dir = Path.home() / "Blender_AI_Models" / "blipdiffusion_download"
    #create directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading model to: {str(output_dir)}")
    
    try:
        import torch
        import diffusers
        from diffusers import BlipDiffusionPipeline
        pipe = BlipDiffusionPipeline.from_pretrained("salesforce/blipdiffusion", torch_dtype=torch.bfloat16, cache_dir=str(output_dir)).to("cuda")
        pipe.save_pretrained(str(output_dir))
        check_model_downloads()
        print("Model downloaded")
    
    except Exception as e:
        check_model_downloads()
        print(f"Error occurred during download: {str(e)}")

def download_DiffuseST_repo():
    #clone repository
    repo_url = "https://github.com/leartssy/DiffusionStyleTransfer_Tileable.git"
    #set an output directory
    parent_dir = Path.home() / "Blender_AI_Models"
    #create directory if doesn´t exist
    parent_dir.mkdir(parents=True, exist_ok=True)
    output_dir = get_repo_root_path()
    print(f"Downloading DiffuseST repo to: {str(parent_dir)}")
    if output_dir.is_dir():
        print(f"Repository already exists at: {str(output_dir)}")
        try:
                # --- PULL (UPDATE) THE EXISTING REPO ---
                print("Attempting to pull (update) the repository...")
                subprocess.check_call([
                    "git", "pull"
                ], cwd=str(output_dir)) # CRITICAL: run 'git pull' inside the repo folder
                print("Repository successfully updated.")
                return output_dir
        except subprocess.CalledProcessError:
            # This handles errors like no network, local uncommitted changes, etc.
            print("Error occurred while updating (pulling) the repository.")
            return output_dir # Return the existing path even if update failed
            
        except FileNotFoundError:
            print("Git executable not found. Ensure git is installed on operating system!")
            return output_dir
    else:
        try:
            subprocess.check_call([
                "git","clone",repo_url
            ], cwd=str(parent_dir))
            
            print(f"Repository successfully cloned to {output_dir}")
        except FileNotFoundError:
            print("Git executable not found. Ensure git is installed on operating system!")
        except:
            print("Error occured while cloning")

def install_textile():
    target_path = get_user_modules_path()
    subprocess.check_call([
        sys.executable, "-m", "pip","install", "textile-metric", "--target", target_path, "--ignore-installed", "--no-deps"
    ])
    subprocess.check_call([
        sys.executable, "-m", "pip","install", "progressbar2","python_utils", "--target", target_path, "--ignore-installed", "--no-deps"
    ])

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
            self.report({'INFO'}, "Starting Model Download...")
            try:
                setupStyleTransferModel()
                if IS_MODEL_DOWNLOADED:
                    self.report({'INFO'}, "Model successfully downloaded.")
                    return {'FINISHED'}
                else:
                    self.report({'ERROR'}, "Model download failed.")
                    return {'CANCELLED'}
            except Exception as e:
                self.report({'ERROR'},f"Model download failed: {str(e)}.")
                return {'CANCELLED'}
            
class DIFFUSEST_OLT_DownloadRepo(Operator):
    """Download the DiffuseST Repo."""
    bl_idname = "diffusest.download_repo"
    bl_label = "Download DiffuseST repo"
    def execute(self,context):
        if IS_DEPENDENCIES_AVAILABLE and IS_MODEL_DOWNLOADED:
            self.report({'INFO'}, "Starting Repo Download...")
            try:
                download_DiffuseST_repo()
                install_textile()
                check_repo_downloads()
                if IS_REPO_DOWNLOADED:
                    self.report({'INFO'}, "Repo successfully downloaded.")
                    print("Installing Textile")
                    return {'FINISHED'}
                else:
                    self.report({'ERROR'}, "Repo download failed.")
                    return {'CANCELLED'}
            except Exception as e:
                self.report({'ERROR'},f"Repo download failed: {str(e)}.")
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
        
        else:
            #get all needed properties
            props = context.scene.diffusest_props

            repo_dir = get_repo_root_path()
            script_path = str(repo_dir / "run.py")
            model_key = str(get_model_path()).replace('\\', '/')
            content_folder = str(props.content_folder).replace('\\', '/')
            style_folder = str(props.style_folder).replace('\\', '/')
            output_folder = str(props.output_folder).replace('\\', '/')
            strength = str(props.strength)
            #textile_strength = str(props.tileability_strength)
            is_tileable = str(props.is_tileable)
            gen_normal = str(props.gen_normal)
            #only_horizontal = str(props.only_horizontal)
            print (f"{is_tileable}")
            guidance_scale = str(props.guidance_scale)
            blur = str(props.blur)
            gap = str(props.gap)
            args = ["--content_path", content_folder, "--style_path", style_folder, "--output_dir", output_folder, "--alpha", strength, "--model_key", model_key, "--guidance_scale", guidance_scale,"--is_tileable",is_tileable, "--gap", gap, "--blur", blur, "--min_ratio","0.05", "--gen_normal", gen_normal]
            #delimiter_space = " "
            #args = str(delimiter_space.join(args))
            #print(args)
            try:
                #run normal batch style transfer
                run_style_transfer(repo_dir, script_path, args)
                self.report(f"Finished style transfer, Find images in {output_folder}")
                return {'FINISHED'}
            except Exception as e:
                self.report({'ERROR'}, f"Generation failed: Error: {e}")
                return {'CANCELLED'}
