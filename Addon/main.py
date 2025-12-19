import subprocess
import sys
import os
from pathlib import Path
from .utils import get_repo_root_path
from .__init__ import MODULES_PATH

def run_style_transfer(repo_dir:str,script_path:str, args:str):
    """runs basic style transfer"""
    import numpy
    import torch
    import transformers
    import textile
    from textile.utils.image_utils import read_and_process_image
    import progressbar
    

    #print("-" * 50)
    #print("RUN.PY SYSTEM PATH CHECK:")
    # Print the entire list of paths where the script is searching for modules
    #for i, path in enumerate(sys.path):
        #print(f"[{i}]: {path}")

    # Now, let's confirm the NumPy version being loaded, or confirm failure location
    #try:
        #print(f"NumPy successfully loaded from: {numpy.__file__}")
    #except AttributeError:
        # If NumPy fails, this won't execute, but the traceback will show where it's failing.
        #pass 
    #except Exception as e:
        #print(f"Error during NumPy check: {e}")

    #print("-" * 50)

    loss_textile = textile.Textile()
    #make sure environment is used in external script
    addon_env = os.environ.copy()
    addon_env['PYTHONPATH'] = MODULES_PATH
    
    if args is None:
        args =[]
    
    command = [sys.executable, script_path]
    command.extend(args)
    print(command)
    try:
        process = subprocess.Popen(
            command,
            cwd=repo_dir,
            env=addon_env,
            )
        return process
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.cmd}, {e.stderr}")
        raise
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise


