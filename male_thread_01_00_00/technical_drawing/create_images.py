# This script generates images into the current working directory
# that are used as a base for creating a technical drawing document.

import pyvista as pv

SQUARE_HIGH_RESOLUTION = (2048, 2048)

# File containing your part (STL format)
INPUT_STL = "../male_thread_visual.stl"

# Read the mesh
mesh = pv.read(INPUT_STL)

# Extract bounding box info for positioning the camera
xmin, xmax, ymin, ymax, zmin, zmax = mesh.bounds
xmid = 0.5 * (xmin + xmax)
ymid = 0.5 * (ymin + ymax)
zmid = 0.5 * (zmin + zmax)

# Helper function to capture views
def capture_view(mesh, camera_pos, camera_up, filename, show_edges=True):
    plotter = pv.Plotter(off_screen=True, window_size=SQUARE_HIGH_RESOLUTION)
    plotter.enable_parallel_projection()  # Use parallel projection for technical views
    if show_edges:
        plotter.add_mesh(mesh, color='white', edge_color='black', show_edges=True, line_width=0.5)
    else:
        plotter.add_mesh(mesh, color='lightgray')
    plotter.camera.position = camera_pos
    plotter.camera.focal_point = (xmid, ymid, zmid)
    plotter.camera.up = camera_up  # Camera's "up" direction
    plotter.show(screenshot=filename)
    plotter.close()

# Offset distance for the camera
offset = 2 * max(xmax - xmin, ymax - ymin, zmax - zmin)

# Capture views
# 1) Front view (from -Y)
front_cam = (xmid, ymid - offset, zmid)
capture_view(mesh, front_cam, (0, 0, 1), "front_view.png", show_edges=False)

# 2) Top view (from +Z, looking down)
top_cam = (xmid, ymid, zmax + offset)
capture_view(mesh, top_cam, (0, 1, 0), "top_view.png")

# 3) Side view (from +X)
side_cam = (xmid + offset, ymid, zmid)
capture_view(mesh, side_cam, (0, 0, 1), "side_view.png", show_edges=False)

# 4) Bottom view (from -Z, looking up)
bottom_cam = (xmid, ymid, zmin - offset)
capture_view(mesh, bottom_cam, (0, -1, 0), "bottom_view.png", show_edges=False)

# 5) Isometric view (from a corner direction, top)
iso_cam = (xmid + offset, ymid + offset, zmid + offset)
capture_view(mesh, iso_cam, (0, 0, 1), "isometric_top_view.png")

# 6) Isometric view (from a corner direction, bottom)
iso_cam = (xmid + offset, ymid + offset, zmid - offset)
capture_view(mesh, iso_cam, (0, 0, -1), "isometric_bottom_view.png", show_edges=False)

print("Done generating images.")
