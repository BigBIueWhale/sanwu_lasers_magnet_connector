"""
Creates a custom "guard sleeve" for the Sanwu Laser Rangers model so the
flashlight adapter can only be pulled off directly upwards.

Exports the final model to STL and STEP.
"""

import cadquery as cq

# === 1. Create the main cylinder ===
#    - Diameter = 29.00 mm (same as diameter of Laser Rangers head base)
#    - Height = 16.90 mm (4.3mm male + 6mm female + 0.3mm gap between them + 6.3mm for both stairs)
model = (
    cq.Workplane("XY")
    .circle(29.00 / 2.0)
    .extrude(16.90)
)

# === 2. Create a through-hole of 21.05 mm diameter from bottom to top ===
#     for the top stair that is 21.00mm in diameter.
model = (
    model
    .faces("<Z")           # Select bottom face
    .workplane()           # Workplane on the bottom
    .hole(21.05)           # Through-hole
)

# === 3. Cut a pocket from the top: 24.05 mm diameter (male piece width with tolerance),
#        10.60 mm depth (total of male + female + gap caused by magnets) ===
model = (
    model
    .faces(">Z")           # Select the top face
    .workplane()           
    .circle(24.05 / 2.0)
    .cutBlind(-10.60)      # Pocket 10.60 mm downward
)

# === 4. Cut a purposefully wider pocket (24.20 mm) from the top, 6.15 mm deep ===
#     This results in a stepped hole where the wider hole at the top overlaps the
#     female portion and half of the magnet gap portion.
model = (
    model
    .faces(">Z")
    .workplane()
    .circle(24.20 / 2.0)
    .cutBlind(-6.15)       # Pocket 6.15 mm downward
)

# === 5. Cut a 25.05 mm diameter pocket 4.00 mm deep at the bottom ===
#     For the bottom stair that is 25.00mm in diameter.
#     In addition to the already-existing through-hole for the top stair.
model = (
    model
    .faces("<Z")           # Select bottom face again
    .workplane()
    .circle(25.05 / 2.0)
    .cutBlind(-4.00)       # Pocket 4 mm upward from bottom
)

# === Export the final model to both STEP and STL files ===
output_file_step = "rangers_guard_sleeve.step"
output_file_stl  = "rangers_guard_sleeve.stl"

cq.exporters.export(model, output_file_step)
cq.exporters.export(model, output_file_stl)

print(f"Model exported to: {output_file_step}")
print(f"Model exported to: {output_file_stl}")
