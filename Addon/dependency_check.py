import sys

# Default state
IS_DEPENDENCIES_AVAILABLE = False

def check_dependencies():
    """Attempt to import core dependency and set the global flag."""
    global IS_DEPENDENCIES_AVAILABLE
    try:
        # Check for a core dependency like 'torch' or 'diffusers'
        import torch 
        IS_DEPENDENCIES_AVAILABLE = True
        print(f"Diffusion Style Transfer Addon: Dependencies loaded successfully.")

    except ImportError as e:
        print("Diffusion Style Transfer Addon: CRITICAL IMPORT FAILURE! Core dependency missing.")
        IS_DEPENDENCIES_AVAILABLE = False
    except Exception as e:
        print(f"Diffusion Style Transfer Addon: General error loading libraries: {e}")
        IS_DEPENDENCIES_AVAILABLE = False

# Call the check function immediately on import
check_dependencies()