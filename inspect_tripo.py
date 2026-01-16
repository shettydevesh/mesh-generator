import tripo3d
import inspect

print("Tripo3D version:", tripo3d.__version__)
print("Dir(tripo3d):", dir(tripo3d))

# Try to find the main client class
for name, obj in inspect.getmembers(tripo3d):
    if inspect.isclass(obj):
        print(f"Class: {name}")
