import sys
import trimesh

def view_mesh(file_path):
    try:
        mesh = trimesh.load(file_path)
        mesh.show()
    except Exception as e:
        print(f"Error viewing mesh: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python view_model.py <path_to_model>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    view_mesh(file_path)
