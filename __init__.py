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
    "name" : "NX_SetSize",
    "author" : "Franck Demongin",
    "description" : "Set size proportionally by axis",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "Object > Transform > Set Size Proportionally",
    "warning" : "",
    "category" : "Object"
}

import bpy

def update_axis(self, context):
    self.dimension = context.object.dimensions[int(self.axis)]

class NXS_OT_SetSize(bpy.types.Operator):
    """Set size proportionally by axis"""
    bl_idname = "nxs.set_size"
    bl_label = "Set size proportionally"
    bl_options = {'REGISTER', 'UNDO'}
    
    axis: bpy.props.EnumProperty(items=[
            ("0", "X", "", 1),
            ("1", "Y", "", 2),
            ("2", "Z", "", 3)
        ],
        update = update_axis
    )
    dimension: bpy.props.FloatProperty(default=1.0)
    apply_scale: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return ( context.object is not None and
            context.object.type in ['MESH', 'CURVE', 'SURFACE'] )
    
    def execute(self, context):        
        obj = context.object
        
        mode = obj.mode
        bpy.ops.object.mode_set(mode='OBJECT') 
                
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=False)
        ax = int(self.axis)
        obj.dimensions[ax] = self.dimension
        scale = obj.scale[ax]
        obj.scale = scale, scale, scale
        
        if self.apply_scale:
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=False)
        
        bpy.ops.object.mode_set(mode=mode)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        self.dimension = context.object.dimensions[int(self.axis)]
        return self.execute(context)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        row = layout.row(align=True)
        row.prop(self, "axis", text="Axis", expand=True)
        col = layout.column()
        col.prop(self, "dimension", text='Dimension')
        col.prop(self, "apply_scale", text="Apply Scale")


def draw_menu(self, context):    
    layout = self.layout
    layout.separator()
    layout.operator('nxs.set_size', text="Set Size Proportionally")
                        
def register():
    bpy.utils.register_class(NXS_OT_SetSize)    
    bpy.types.VIEW3D_MT_transform_object.append(draw_menu)
    bpy.types.VIEW3D_MT_transform.append(draw_menu)
       
def unregister():
    bpy.utils.unregister_class(NXS_OT_SetSize)
    bpy.types.VIEW3D_MT_transform_object.remove(draw_menu)
    bpy.types.VIEW3D_MT_transform.remove(draw_menu)
