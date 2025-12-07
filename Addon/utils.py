import sys
import shutil
import os
import time


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

# Call the check function immediately on import
check_dependencies()