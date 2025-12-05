import bpy
import os
import platform
import ctypes
from importlib.util import find_spec
import sys
import subprocess
import threading
from mathutils import *
from bpy.types import Operator
from bpy.app.translations import pgettext_iface as _
from .__init__ import get_user_modules_path 
from .dependency_check import IS_DEPENDENCIES_AVAILABLE


D = bpy.data
C = bpy.context



#Paths Defined in __init__.py
MODULES_PATH = get_user_modules_path()
# Global variable if installed
IS_DEPENDENCIES_AVAILABLE = False

#######try to make Blender not freeze: currently not working because of permission issues######
#make function for installing, so blender doesn´t freeze while installing

#def install_thread_func(addon_dir, operator_instance, target_path):
    #"""Function run in seperate thread to install dependencies"""
    
    #path to requirements
    #normal_req_path = os.path.join(addon_dir, "requirements.txt")
    #requirements_path = f"{normal_req_path}"
    #path to Blenders executable
    #python_exec = sys.executable

    #installation command
    #command = [
        #python_exec,
        #'-m',
        #'pip',
        #'install',
        #'--upgrade',
        #'--target', target_path,
        #'-r',
        #requirements_path
    #]

    #execute command
    #try:
        # Run the installation (Blocking call in a separate thread)
        #operator_instance.install_report = f"Starting installation to: {target_path}..."
        
        #process = subprocess.run(
            #command,
            #stdout=subprocess.PIPE,
            #stderr=subprocess.PIPE,
            #check=True
        #)

        # Check output for potential warnings that aren't fatal errors
        #operator_instance.install_success = True
        #operator_instance.install_report = "Installation successful. Blender must be restarted to finalize dependency check."
        
    #except subprocess.CalledProcessError as e: #typical errors
        #store failure
        #operator_instance.install_success = False
        #operator_instance.report({'ERROR'}, f"Installation failed (Error Code {e.returncode}): {e.stderr.decode('utf-8')}")
        
    #except Exception as e: #unforseen errors
        #operator_instance.install_success = False
        #operator_instance.report({'ERROR'}, f"An unexpected error occurred during installation: {e}")
    #Mark thread as completed
    #finally:
        #operator_instance.is_thread_finished = True


def install_dependencies():
    #ensure pip is installed
    import ensurepip
    ensurepip.bootstrap()

    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    import pip

    #find path of python scripts blender
    custom_path = f"C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\Scripts"
    if custom_path not in sys.path:
        sys.path.append(custom_path)
    print(sys.path) # Verify the path has been added

    #uninstall old numpy (can lead to conflicts)
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "numpy"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==2.2.6"])
    #install torch etc
    #cuda 121 version
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "torch", "torchvision", "torchaudio",
        "--index-url", "https://download.pytorch.org/whl/cu121"
    ])
    #cpu version (not recommended, because slow)
    #subprocess.check_call([
        #sys.executable, "-m", "pip", "install", 
        #"torch+cpu", "torchvision+cpu", "torchaudio+cpu",
       # "--index-url", "https://download.pytorch.org/whl/cpu"
    #])
    #check if installed
    try:
        import torch
        print("Dependencies installed. Restart Blender.")
    except ImportError:
        print("ImportError")
    except Exception:
        print("ExceptionError")

#main operator for installing
class DIFFUSEST_OT_InstallDependencies(Operator):
    """Installs required Python packages using Blender's Python environment"""
    bl_idname = "diffusest.install_deps"
    bl_label = "Install DiffusionST Dependencies"
    
    #old background process install: doesn´t work currently
    # Properties to store state and results from the background thread
    #install_thread: threading.Thread = None
    #is_thread_finished: bool = False
    install_success: bool = False
    #install_report: str = ""
    #_timer =None

    #def execute(self, context):
    #    if self.install_thread and self.install_thread.is_alive():
    #        self.report({'WARNING'}, "Installation is already running.")
    #        return {'CANCELLED'}
        
        
    #    addon_prefs = context.preferences.addons.get(__package__).preferences
    #    addon_prefs.is_installing = True
        
    #    self.is_thread_finished = False
    #    self.install_success = False
    #    addon_dir = os.path.dirname(os.path.abspath(__file__))
        
    #    target_path = get_user_modules_path()

    #    self.install_thread = threading.Thread(
    #        target=install_thread_func, 
    #        args=(addon_dir, self, target_path) # Pass target_path here
        #)
    #    self.install_thread.start()
        
        #start modal timer
    #    context.window_manager.modal_handler_add(self)
    #    self._timer = context.window_manager.event_timer_add(0.1, window=context.window)

    #    return {'RUNNING_MODAL'}

    #def modal(self, context, event):
    #    if event.type == 'TIMER':
            
    #        if self.is_thread_finished:
    #            addon_prefs = context.preferences.addons.get(__package__).preferences
                
    #            context.window_manager.event_timer_remove(self._timer)
    #            addon_prefs.is_installing = False # Reset UI status
                
    #            if self.install_success:
                    
    #                self.report({'INFO'}, self.install_report)
    #                return {'FINISHED'}
    #            else:
    #                self.report({'ERROR'}, self.install_report)
    #                return {'CANCELLED'}

    #    return {'PASS_THROUGH'}
    
    #def cancel(self, context):
    #    context.window_manager.event_timer_remove(self._timer)
    #    context.preferences.addons.get(__package__).preferences.is_installing = False
    #    self.report({'CANCELLED'}, "Installation cancelled.")
    def execute(self,context):
        addon_prefs = context.preferences.addons.get(__package__).preferences
    #check if everything works
    try:
        import torch
        print(torch.__version__, torch.version.cuda, torch.cuda.is_available())
        print("Dependencies installed.Restart Blender.")
        install_success=True
    except:
        print("Install error occured")

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