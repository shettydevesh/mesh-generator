import inspect
from tripo3d import TripoClient

try:
    print("mesh_segmentation:", inspect.signature(TripoClient.mesh_segmentation))
    print("_add_optional_params:", inspect.signature(TripoClient._add_optional_params))
except Exception as e:
    print(e)
