import cadquery as cq

# 1) Create the main cylinder:
#    Height: 7.30 mm (3mm for male rod + 4.3mm for magnet holes)
#    Diameter: 24 mm (diameter)
model = (
    cq.Workplane("XY")
    .circle(24 / 2)
    .extrude(7.30)
)

# 2) Drill an 8.05 mm diameter through-hole from the bottom face all the way through.
model = (
    model
    .faces("<Z")       # Select the bottom face
    .workplane()
    .hole(8.05)        # Through-hole 8.05 mm diameter for laser light
)

# 3) Create a 3 mm deep pocket at the bottom, leaving an 11.45 mm diameter rod.
#    i.e., remove material from radius 11.45/2 out to 24/2 for 3 mm of depth.
#    11.45 is slightly smaller major diameter than M11.5x0.5 thread, for tolerance.
model = (
    model
    .faces("<Z")         # Select the bottom face
    .workplane()
    .circle(24 / 2)      # Outer diameter
    .circle(11.45 / 2)   # Keep this center region
    .cutBlind(-3)        # Remove 3 mm upward from the bottom
)

# At this point, we have:
#   - Main cylinder body of height 4.3mm (not including rod)
#   - A 3 mm-long "rod" at the bottom (z=0..3), diameter = 11.45 mm.

# 4) Shave off the TOP 1 mm of the 3 mm rod from 11.45 mm down to 10.90 mm.
#    That means:
#      - The bottom 2 mm of the rod (z=0..2) remains 11.45 mm diameter.
#      - The top 1 mm of the rod (z=2..3) becomes 10.90 mm diameter.
#
#    We'll do this by cutting a ring from radius 10.90/2 to 11.45/2
#    over the top 1 mm region of the rod.
#    Minor diameter of m11.5x0.5 thread (d₂) = 11.5 - 2 × (5/8 × (0.5 × √3/2)) ≈ 10.9587 mm
#    so we'll make the base 10.90 diameter which is slightly smaller for tolerance purposes.
#    This ensures that the base doesn't have to be threaded, because it's hard to thread
#    a rod all the way so close to the flat surface.

model = (
    model
    .faces("<Z")                  # Start from the bottom face
    .workplane()
    .transformed(offset=(0,0,-2)) # Move up 2 mm
    .circle(11.45 / 2)            # Outer edge of the rod
    .circle(10.90 / 2)            # New smaller diameter
    .cutBlind(-1)                 # Cut upward 1 mm
)

# 5) Drill the magnet holes around the top face
#    - 12 holes
#    - Each hole diameter: 4.11 mm (4.06 diameter magnets with 5mm tolerance)
#    - Hole depth: 3.3 mm (still have 1mm floor)
#    - Hole centers on a circle of radius: 9.3mm and are equally spaced.
model = (
    model
    .faces(">Z")               # pick the top face again
    .workplane()               # new workplane for drilling
    .polarArray(radius=9.3, startAngle=0, angle=360, count=12, fill=True)  # 12 holes in a full circle
    .hole(diameter=4.11, depth=3.3)  # create the holes as pockets in the top
)

# === Export the final model to both STEP and STL files ===
output_file_step = "male_thread.step"
output_file_stl  = "male_thread.stl"

cq.exporters.export(model, output_file_step)
cq.exporters.export(model, output_file_stl)
