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
from . import auto_load
import bpy
from . import operators, ui_panel

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

auto_load.init()

CLASSES = []


def register():
    auto_load.register()
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    auto_load.unregister()
    #unregister in reversed order for safety
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
