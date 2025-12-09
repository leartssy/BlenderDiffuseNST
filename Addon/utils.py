import sys
import shutil
import os
import time
from pathlib import Path

IS_DEPENDENCIES_AVAILABLE = False
IS_MODEL_DOWNLOADED = False
IS_REPO_DOWNLOADED = False

def check_dependencies():
    """Attempt to import core dependency and set the global flag."""
    global IS_DEPENDENCIES_AVAILABLE
    IS_DEPENDENCIES_AVAILABLE = False

    try:
        # Check for a core dependencies, correct numpy version and cuda availability
        import torch
        import diffusers
        import numpy

        if numpy.__version__ == "2.2.6" and torch.cuda.is_available():
            
            IS_DEPENDENCIES_AVAILABLE = True
            print(f"Diffusion Style Transfer Addon: Dependencies loaded successfully.")
        
        else: 
            IS_DEPENDENCIES_AVAILABLE = False
            if numpy.__version__ != "2.2.6":
                print(f"Error: NumPy version conflict!")
            if not torch.cuda.is_available():
                print("Cuda not working, refer to README")
    except ImportError as e:
        print("Diffusion Style Transfer Addon: CRITICAL IMPORT FAILURE! Core dependency missing.")
        IS_DEPENDENCIES_AVAILABLE = False
    except Exception as e:
        print(f"Diffusion Style Transfer Addon: General error loading libraries: {e}")
        IS_DEPENDENCIES_AVAILABLE = False

def get_model_path():
    """Calculates and returns the standard path for the cloned repository."""
    # Ensure this path EXACTLY matches the destination used in your clone function
    return Path.home() / "Blender_AI_Models" / "blipdiffusion_download"

def check_model_downloads():
    """Check if all needed models are downloaded"""
    global IS_MODEL_DOWNLOADED
    IS_MODEL_DOWNLOADED = False
    model_path = get_model_path()
    if model_path.exists() and (model_path / "model_index.json").exists():
        IS_MODEL_DOWNLOADED = True

def get_repo_root_path():
    """Calculates and returns the standard path for the cloned repository."""
    # Ensure this path EXACTLY matches the destination used in your clone function
    return Path.home() / "Blender_AI_Models" / "DiffusionStyleTransfer_Tileable"

def check_repo_downloads():
    """Check if all needed models are downloaded"""
    global IS_REPO_DOWNLOADED
    IS_REPO_DOWNLOADED = False
    repo_path = get_repo_root_path()
    if repo_path.exists():
        IS_REPO_DOWNLOADED = True



# Call the check functions immediately on import
check_dependencies()
check_model_downloads()
check_repo_downloads()