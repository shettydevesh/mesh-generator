import trimesh
import numpy as np
import os

class MeshProcessor:
    def __init__(self):
        pass

    def load_mesh(self, path: str):
        """Loads a mesh or scene from a file."""
        try:
            mesh = trimesh.load(path)
            return mesh
        except Exception as e:
            print(f"Error loading mesh {path}: {e}")
            return None

    def inspect_glb(self, path: str):
        """Prints details about a GLB file."""
        mesh = self.load_mesh(path)
        if isinstance(mesh, trimesh.Scene):
            print(f"GLB contains a Scene with {len(mesh.geometry)} geometries.")
            for name, geom in mesh.geometry.items():
                print(f" - Geometry: {name}, Vertices: {len(geom.vertices)}")
        else:
            print(f"GLB contains a single Mesh. Vertices: {len(mesh.vertices)}")

    def merge_meshes(self, parts: list, output_path: str):
        """
        Merges multiple mesh files into one scene.
        """
        scene = trimesh.Scene()
        
        for part in parts:
            path = part['path']
            pos = part.get('position', [0, 0, 0])
            
            mesh = self.load_mesh(path)
            if mesh:
                if isinstance(mesh, trimesh.Scene):
                    for name, geom in mesh.geometry.items():
                        geom_copy = geom.copy()
                        geom_copy.apply_translation(pos)
                        scene.add_geometry(geom_copy)
                else:
                    mesh.apply_translation(pos)
                    scene.add_geometry(mesh)
        
        scene.export(output_path)
        print(f"Merged model saved to {output_path}")

    def split_scene(self, path: str, output_dir: str):
        """
        Splits a GLB scene into individual GLB files for each geometry.
        """
        mesh = self.load_mesh(path)
        if not mesh:
            return

        base_name = os.path.splitext(os.path.basename(path))[0]
        
        if isinstance(mesh, trimesh.Scene):
            print(f"Splitting scene '{base_name}' into {len(mesh.geometry)} parts...")
            for name, geom in mesh.geometry.items():
                # Clean up name
                clean_name = name.replace(":", "_").replace("/", "_")
                out_name = f"{base_name}_{clean_name}.glb"
                out_path = os.path.join(output_dir, out_name)
                
                # Export individual geometry
                # Trimesh can export a single Trimesh object as GLB
                geom.export(out_path)
                print(f"Saved part: {out_path}")
        else:
            print(f"File {path} is a single mesh, nothing to split.")
