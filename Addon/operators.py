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
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==2.2.6", "--target",target_path])

    #install torch -> 2.1.0 is safest version with blender
    #cuda 121 version
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "torch==2.5.1", "torchvision", "torchaudio",
        "--index-url", "https://download.pytorch.org/whl/cu121","--target", target_path, "--no-deps", "--ignore-installed"
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

def display_image(image_path, is_tileable):
    #absolute path
    abs_path = os.path.abspath(image_path)
    bpy_image = bpy.data.images.load(abs_path, check_existing=True)
    bpy_image.reload()
    #find open UV/Image editor area
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            area.spaces.active.image = bpy_image

            #update the view
            area.tag_redraw()
            return
def install_colormatch():
    target_path = get_user_modules_path()
    subprocess.check_call([
        sys.executable, "-m", "pip","install", "color-matcher", "--target", target_path, "--no-deps"
    ])

def preview(albedo_image_path,normal_path):
    albedo_path = albedo_image_path
    normal_path = normal_path
    
    #create ico sphere if not already existing
    sphere = bpy.data.objects.get("Preview_Sphere")

    if not sphere:
        bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions=4, 
                radius=1.0,
                enter_editmode=False, 
                align='WORLD', 
                location=(0, 0, 0)
            )
        sphere = bpy.context.active_object
        sphere.name = "Preview_Sphere"
        bpy.ops.object.shade_smooth()
    

    #add material
    mat_name = os.path.basename(albedo_path)
    mat_name = os.path.splitext(os.path.basename(albedo_path))[0] #without .png
    mat = bpy.data.materials.new(f"M_{mat_name}") # Creates a default node tree
    obj = sphere
    obj.active_material = mat
    mat.use_nodes = True # Deprecated, has no effect.
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear() #clear nodes

    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_tex_coord = nodes.new(type='ShaderNodeTexCoord')

    
    #Albedo texture
    node_albedo = nodes.new(type='ShaderNodeTexImage')
    try:
        img_albedo = bpy.data.images.load(albedo_path)
        node_albedo.image = img_albedo
    except:
        print(f"Albedo not found at: {albedo_path}")
    #list of existing nodes
    active_tex_nodes = [node_albedo]
    if normal_path:
        #Normal map texture
        node_normal = nodes.new(type='ShaderNodeTexImage')
        node_normal_map = nodes.new(type='ShaderNodeNormalMap')
        try:
            img_normal = bpy.data.images.load(normal_path)
            node_normal.image = img_normal
            img_normal.colorspace_settings.name = 'Non-Color'
            active_tex_nodes.append(node_normal) #append if there is a normal
        except:
            print(f"Normal texture not found at: {normal_path}")
    else:
        print("No Normal Map available for this texture.")
        

    #Box mapping for seamless
    for tex_node in active_tex_nodes:
        tex_node.projection = 'BOX'
        tex_node.projection_blend = 0.2
        links.new(node_tex_coord.outputs['Generated'], tex_node.inputs['Vector'])
        
    #connecting nodes
    links.new(node_albedo.outputs['Color'], node_bsdf.inputs['Base Color'])
    if normal_path:
        links.new(node_normal.outputs['Color'], node_normal_map.inputs['Color'])
        links.new(node_normal_map.outputs['Normal'], node_bsdf.inputs['Normal'])
    
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

    #assign material or replace when already has one

    if sphere.data.materials:
            sphere.data.materials[0] = mat
    else:
        sphere.data.materials.append(mat)

    #make sphere active object for visibility
    bpy.context.view_layer.objects.active = sphere
    sphere.select_set(True)

def get_preview_image(prev_normal):
    #get the displayed image
         
    img = None
    has_normal = False
    normal_path = None
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            img = area.spaces.active.image
            break
    if not img:
        print("No image found in the UV Editor")
        return
    #get the albedo path
    albedo_path = bpy.path.abspath(img.filepath)
    if prev_normal: #only get path to normal map if desired
        #get normal map path
        base, ext = os.path.splitext(albedo_path)
        normal_path = f"{base}_normal{ext}"
        #check if normal map exists
        has_normal = os.path.exists(normal_path)
    #return albedo and normal if it´s there
    return img, normal_path if has_normal else None

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
                install_colormatch()
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

    _timer = None
    _process = None
    _total_expected = 1
    _session_start_time = 0.0
    _last_display_time = 0.0

    def modal(self,context,event):
        #check if process is still running
        if self._process is None or self._process.poll() is not None:
            #clear progress bar
            self.cancel(context)
            self.report({'INFO'}, "Style Transfer Finished.")
            
            return {'FINISHED'}
        
        #on every timer tick
        if event.type == 'TIMER':
            props = context.scene.diffusest_props
            output_path = Path(bpy.path.abspath(props.output_folder))
            is_tileable = props.is_tileable

            if output_path.exists():
                all_files = list(output_path.glob('*.png'))
                #newly generated images
                current_session_results = [f for f in all_files if ("_raw" in f.name or "_tiled" in f.name) and f.stat().st_mtime > (self._session_start_time - 0.5)]
                current_count= len(current_session_results)
                #update the percentage progressbar in ui panel
                if self._total_expected > 0:
                    percent = (current_count / self._total_expected) * 100
                    props.progress = percent
                #update progress bar
                context.window_manager.progress_update(current_count)
                context.workspace.status_text_set(
                    f"Generating Style Transfer: {current_count}/{self._total_expected}"
                )
                context.area.tag_redraw()
                    
                #if new file appeared, display it, do color transfer if needed
                if current_session_results:
                    #get newest file and its time
                    newest_file = max(current_session_results, key=lambda f: f.stat().st_mtime)
                    newest_time = newest_file.stat().st_mtime

                    if newest_time > self._last_display_time:
                        display_image(str(newest_file),is_tileable)
                        
                        self._last_display_time = newest_time
                        self.report({'INFO'}, f"Updated: {newest_file.name}")

                #Force UI to redraw
                for area in context.screen.areas:
                    if area.type in {'STATUSBAR','PROPERTIES','IMAGE_EDITOR'}:
                        area.tag_redraw()
        
        return {'PASS_THROUGH'}

    def execute(self, context):
        import time
        if not hasattr(context.scene, 'diffusest_props'):
            self.report({'ERROR'}, "Add-on properties failed to load.")
            return {'CANCELLED'}
        
        else:
            #get all needed properties
            props = context.scene.diffusest_props
            props.is_running = True
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
            normal_strength = str(props.normal_strength)
            #only_horizontal = str(props.only_horizontal)
            print (f"{is_tileable}")
            guidance_scale = str(props.guidance_scale)
            color_strength = str(props.color_strength)
            blur = str(props.blur)
            gap = str(props.gap)
            args = ["--content_path", content_folder, "--style_path", style_folder, "--output_dir", output_folder, "--alpha", strength, "--model_key", model_key, "--guidance_scale", guidance_scale,"--is_tileable",is_tileable, "--gap", gap, "--blur", blur, "--min_ratio","0.05", "--gen_normal", gen_normal, "--normal_strength", normal_strength,"--color_strength",color_strength]
            #delimiter_space = " "
            #args = str(delimiter_space.join(args))
            #print(args)

            #### progress bar ####
            #total files to process (content_files *styleFiles)
            content_path = Path(bpy.path.abspath(props.content_folder))
            style_path = Path(bpy.path.abspath(props.style_folder))
            exts = ('.png', '.jpg', '.jpeg', '.webp')
            #count them
            if content_path.is_file():
                content_count = 1
            else:
                content_count = len([f for f in content_path.glob('*') if f.suffix.lower() in exts])
            
            if style_path.is_file():
                style_count = 1
            else:
                style_count = len([f for f in style_path.glob('*') if f.suffix.lower() in exts])

            if props.gen_normal:
                self._total_expected = content_count * style_count * 2 #double the images because need to generate normal maps
            else:
                self._total_expected = content_count * style_count
            
            now = time.time()
            self._session_start_time = now
            self._last_display_time = now
            context.window_manager.progress_begin(0, self._total_expected) 

            #########
            try:
                #run normal batch style transfer
                self.report({'INFO'},"Loading style transfer model...")
                self._process = run_style_transfer(repo_dir, script_path, args)
            except Exception as e:
                context.window_manager.progress_end()
                self.report({'ERROR'}, f"Failed to start: {e}")
                return {'CANCELLED'}
            #start modal timer
            self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
            
    
    def cancel(self,context):
        context.scene.diffusest_props.is_running = False
        context.window_manager.progress_end()
        context.workspace.status_text_set(None)
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        
class DIFFUSEST_OT_Preview(Operator):
    """Preview current displayed texture."""
    bl_idname = "diffusest.preview"
    bl_label = "Perform texture preview"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        props = context.scene.diffusest_props
        prev_normal = props.prev_normal
        result = get_preview_image(prev_normal)
        if not result:
            self.report({'WARNING'}, "No image found in Image Editor!")
            return {'CANCELLED'}
        img_obj, norm_path = result
        albedo_path = bpy.path.abspath(img_obj.filepath)
        if norm_path is None:
            self.report({'INFO'}, "Preview created (No Normal Map found).")
        else:
            self.report({'INFO'}, "Preview created with Normal Map.")
        preview(albedo_path, norm_path)
        return {'FINISHED'}