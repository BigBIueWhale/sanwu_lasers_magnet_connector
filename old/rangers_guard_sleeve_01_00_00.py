"""
Creates a custom "guard sleeve" for the Sanwu Laser Rangers model so the
flashlight adapter can only be pulled off directly upward. The key steps:

1. Start with a 30.20 mm diameter, 23.2 mm height cylinder (base shape).
2. Cut a centered 21.10 mm diameter through-hole from bottom to top.
3. From the top, cut a 28.10 mm diameter, 16.90 mm deep pocket.
4. From the top, cut a slightly wider 28.20 mm diameter, 8.40 mm deep pocket
   (this overlaps only the top portion, creating a step).
5. From the bottom, cut a 25.10 mm diameter, 4.00 mm deep pocket (in addition
   to the through-hole) for the lower stair.

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

# === 2. Create a through-hole of 21.10 mm diameter from bottom to top ===
model = (
    model
    .faces("<Z")           # Select bottom face
    .workplane()           # Workplane on the bottom
    .hole(21.10)           # Through-hole
)

# === 3. Cut a pocket from the top: 28.10 mm diameter, 16.90 mm depth ===
model = (
    model
    .faces(">Z")           # Select the top face
    .workplane()           
    .circle(28.10 / 2.0)
    .cutBlind(-16.90)      # Pocket 16.9 mm downward
)

# === 4. Cut a slightly wider pocket (28.20 mm) from the top, 8.40 mm deep ===
#     This overlaps only the top portion, resulting in a stepped hole.
model = (
    model
    .faces(">Z")          
    .workplane()
    .circle(28.20 / 2.0)
    .cutBlind(-8.40)       # Pocket 8.4 mm downward
)

# === 5. Cut a 25.10 mm diameter pocket 4.00 mm deep at the bottom ===
#     In addition to the through-hole, for the bottom stair.
model = (
    model
    .faces("<Z")           # Select bottom face again
    .workplane()
    .circle(25.10 / 2.0)
    .cutBlind(-4.00)       # Pocket 4 mm upward from bottom
)

# === Export the final model to both STEP and STL files ===
output_file_step = "rangers_guard_sleeve.step"
output_file_stl  = "rangers_guard_sleeve.stl"

cq.exporters.export(model, output_file_step)
cq.exporters.export(model, output_file_stl)

print(f"Model exported to: {output_file_step}")
print(f"Model exported to: {output_file_stl}")
