"""
Transforms a Sanwu Laser Rangers head into a head with magnet connector
and sleeve into which the flashlight (with its own magnet connector) can slide in.

Purpose: save costs by merging rangers_guard_sleeve_01_00_00.py and magnet_holes_01_00_01.py
Issue: requires drilling 2mm diameter pockets at a surface that starts 8.4mm deep
       pocket depth shouldn't exceed 3x the diameter of the tool being used to make it

Exports the final model to STL and STEP.
"""

import cadquery as cq

# === 1. Create the main cylinder ===
#    - Diameter = 30.20 mm → radius = 15.10 mm
#    - Height = 23.2 mm
model = (
    cq.Workplane("XY")
    .circle(30.20 / 2.0)
    .extrude(23.2)
)

# === 2. Create a through-hole of 17.6 mm diameter from bottom to top
model = (
    model
    .faces("<Z")               # pick the bottom face
    .workplane()               # create a new workplane on that face
    .hole(17.6)                # cut a 17.6 mm diameter hole all the way through
)

# === 3. Cut a 28.20mm wide pocket from the top, 8.40 mm deep ===
#     This is an area designed to allow a connecting magnet piece to slide in.
model = (
    model
    .faces(">Z")          
    .workplane()
    .circle(28.20 / 2.0)
    .cutBlind(-8.40)       # Pocket 8.4 mm downward
)

# === 4. Drill the 16 magnet holes in the bottom of the 8.40 mm-deep pocket ===
#     - 16 holes
#     - Each hole diameter: 4.16 mm
#     - Hole depth: 3.3 mm (starting from the bottom of the pocket)
#     - Hole centers on a circle of radius: 11.4 mm
model = (
    model
    .faces(">Z")  # Select the top ring face (highest Z face)
    .workplane(offset=-8.40)  # Move the workplane down 8.40 mm to the bottom of the pocket
    .polarArray(radius=11.4, startAngle=0, angle=360, count=16)  # 16 holes evenly spaced
    .hole(diameter=4.16, depth=3.3)  # Create the holes as pockets
)

# === 5. Cut a 21.10 mm diameter pocket 4.00 mm deep at the bottom ===
#     For the bottom stair, in addition to the deeper hole for the top stair.
model = (
    model
    .faces("<Z")           # Select bottom face again
    .workplane()
    .circle(21.10 / 2.0)
    .cutBlind(-6.30)       # Pocket 6.3 mm upward from bottom- total height of both stairs
)

# === 6. Cut a 25.10 mm diameter pocket 4.00 mm deep at the bottom ===
#     For the bottom stair, in addition to the deeper hole for the top stair.
model = (
    model
    .faces("<Z")           # Select bottom face again
    .workplane()
    .circle(25.10 / 2.0)
    .cutBlind(-4.00)       # Pocket 4 mm upward from bottom
)

# === Export the final model to both STEP and STL files ===
output_file_step = "male_head.step"
output_file_stl  = "male_head.stl"

cq.exporters.export(model, output_file_step)
cq.exporters.export(model, output_file_stl)

print(f"Model exported to: {output_file_step}")
print(f"Model exported to: {output_file_stl}")
