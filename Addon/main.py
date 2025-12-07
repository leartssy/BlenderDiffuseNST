import subprocess
import sys
import os
from pathlib import Path
from .utils import get_repo_root_path
from .__init__ import MODULES_PATH

def run_style_transfer(repo_dir:str,script_path: str, args:list=None):
    """runs basic style transfer"""

    #make sure environment is used in external script
    addon_env = os.environ.copy()
    existing_path = addon_env.get('PYTHONPATH', '')
    addon_env['PYTHONPATH'] = MODULES_PATH + os.pathsep + existing_path

    if args is None:
        args =[]

    command = [sys.executable, script_path]
    command.extend(args)

    try:
        result = subprocess.run(
            command,
            cwd=repo_dir,
            env=addon_env,
            check=True,
            capture_output=True,
            text=True
            )
        print("Running style transfer...")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.cmd}, {e.stderr}")
        raise
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise


