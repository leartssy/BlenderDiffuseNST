# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import importlib

bl_info = {
    "name": "DiffusionStyleTransfer",
    "author": "Lea Eschlberger",
    "description": "Addon for Diffusion-Based Neural Style Transfer for tileable texture creation in Blender",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "UV Editor > Sidebar > DiffuseST Tab",
    "warning": "",
    "category": "Generic",
}
# 2. Check if auto_load is already loaded (needed for VS Code reloads)
if "auto_load" in locals():
    # If the add-on is being reloaded by the VS Code extension,
    # we need to reload the auto_load module to ensure changes are picked up.
    importlib.reload(auto_load) 
# 3. Now perform the import reliably.
# Note: For typical Blender installation, you would still use 'from . import auto_load', 
# but for the VS Code development environment, sometimes an absolute import is forced.
try:
    from . import auto_load
except ImportError:
    # Fallback for when running __init__.py directly in some dev environments
    import auto_load

auto_load.init()

def register():
    auto_load.register()
 

def unregister():
    
    auto_load.unregister()
    

if __name__ == "__main__":
    register()
