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

bl_info = {
    "name": "Diffusion Style Transfer",
    "author": "Lea Eschlberger",
    "description": "Diffusion-Based Neural Style Transfer",
    "blender": (5, 00, 0),
    "version": (0, 0, 1),
    "location": "UV > Sidebar",
    "warning": "",
    "category": "NST",
}

import bpy
import sys
import site
from . import auto_load
from . import operators, ui_panel, properties, dependency_check

# Function to get the user's Blender-specific modules path
def get_user_modules_path():
    return bpy.utils.user_resource("SCRIPTS", path="modules", create=True)

MODULES_PATH = get_user_modules_path()
if MODULES_PATH not in sys.path:
    sys.path.append(MODULES_PATH)
    # Use site.addsitedir to properly register the directory for package discovery
    site.addsitedir(MODULES_PATH)

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()
    
if __name__ == "__main__":
    register()