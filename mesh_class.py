from meshpy.tet import MeshInfo, build

mesh_info = MeshInfo()

import os

class ImportMCellMDL(bpy.types.Operator, ImportHelper):
    '''Load an MCell MDL geometry file with regions'''
    bl_idname = "import_mdl_mesh.mdl"
    bl_label = "Import MCell MDL"
    bl_options = {'UNDO'}

    files = CollectionProperty(name="File Path",
                          description="File path used for importing "
                                      "the MCell MDL file",
                          type=bpy.types.OperatorFileListElement)

    directory = StringProperty()

    filename_ext = ".mdl"
    filter_glob = StringProperty(default="*.mdl", options={'HIDDEN'})

    add_to_model_objects = BoolProperty(
        name="Add to Model Objects",
        description="Automatically add all meshes to the Model Objects list",
        default=True,)

    def execute(self, context):
        paths = [os.path.join(self.directory, name.name) for name in self.files]
        if not paths:
            paths.append(self.filepath)

        # Attempt to use fast swig importer (assuming make was successful)
        try:
            from . import import_mcell_mdl
            from . import mdlmesh_parser

            for path in paths:
                import_mcell_mdl.load(
                    self, context, path, self.add_to_model_objects)

        # Fall back on slow pure python parser (pyparsing)
        except ImportError:
            from . import import_mcell_mdl_pyparsing
        
            for path in paths:
                import_mcell_mdl_pyparsing.load(
                    self, context, path, self.add_to_model_objects)


        return {'FINISHED'}











mesh_info.set_points([
    (0,0,0), (2,0,0), (2,2,0), (0,2,0),
    (0,0,12), (2,0,12), (2,2,12), (0,2,12),
    ])
mesh_info.set_facets([
    [1,3,0],
    [7,5,4],
    [4,1,0],
    [5,2,1],
    [2,7,3],
    [0,7,4],
    [1,2,3],
    [7,5,4],
    [4,1,0],
    [5,2,1],
    [2,7,3],
    [0,7,4],
    ])
mesh = build(mesh_info)
mesh.write_vtk("test.vtk")