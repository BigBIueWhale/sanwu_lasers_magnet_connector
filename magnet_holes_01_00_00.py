"""
Creates a 'toilet paper roll' shaped cylinder with:
  - Outer diameter: 28.0 mm
  - Inner hole diameter: 17.6 mm (fully through)
  - Height: 8.3 mm
Then adds 16 equally spaced magnet holes at the top:
  - Diameter: 4.04 mm
  - Depth: 3.3 mm
  - Circle radius for hole centers: 11.4 mm
Exports the model to both STL and STEP formats.
"""

import cadquery as cq

# === 1. Create main cylinder ===
#   - Outer diameter: 28 mm → radius = 14 mm
#   - Height: 8.3 mm
model = (
    cq.Workplane("XY")
    .circle(14)        # radius for 28 mm diameter
    .extrude(8.3)      # height
)

# === 2. Hollow out the center (like a toilet paper roll) ===
#   - Through-hole with diameter: 17.6 mm → radius = 8.8 mm
model = (
    model
    .faces(">Z")               # pick the top face
    .workplane()               # create a new workplane on that face
    .hole(17.6)                # cut a 17.6 mm diameter hole all the way through
)

# === 3. Drill the magnet holes around the top face ===
#   - 16 holes
#   - Each hole diameter: 4.04 mm
#   - Hole depth: 3.3 mm
#   - Hole centers on a circle of radius: 11.4 mm
#     so they are equally spaced 360/16=22.5 degrees apart
model = (
    model
    .faces(">Z")               # pick the top face again
    .workplane()               # new workplane for drilling
    .polarArray(radius=11.4, startAngle=0, angle=360, count=16, fill=True)  # 16 holes in a full circle
    .hole(diameter=4.04, depth=3.3)  # create the holes as pockets in the top
)

# === 4. Export the final model to both STL and STEP files ===
output_file_step = "magnet_holes.step"
output_file_stl = "magnet_holes.stl"

# Export to STEP format
cq.exporters.export(model, output_file_step)

# Export to STL format
cq.exporters.export(model, output_file_stl)

# Print file names for confirmation
print(f"Model exported to: {output_file_step}")
print(f"Model exported to: {output_file_stl}")
