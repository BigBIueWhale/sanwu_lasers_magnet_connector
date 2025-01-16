import cadquery as cq

# python3 -m pip install git+https://github.com/gumyr/cq_warehouse.git#egg=cq_warehouse
# Currently using: cq_warehouse==0.8.0
from cq_warehouse.fastener import IsoThread

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

# Approximate minor diameter of m11.5x0.5 ISO Metric fine thread:
# 11.5 - 2 × (5/8 × (0.5 × √3/2)) ≈ 10.9587 mm
minor_diameter = 10.9587

# 3) Create a 3 mm deep pocket at the bottom, leaving a base rod for the thread
model = (
    model
    .faces("<Z")          # Select the bottom face
    .workplane()
    .circle(24 / 2)       # Outer diameter
    .circle(minor_diameter / 2)    # Keep the center region
    .cutBlind(-3)         # Remove 3 mm upward from the bottom
)

# 4) Make the base 1mm of the rod unthreaded, slightly thinner than even the minor diameter.
model = (
    model
    .faces("<Z")                # Start from the bottom face
    .workplane()
    .transformed(offset=(0,0,-2)) # Move up 2 mm
    .circle(minor_diameter / 2)   # Outer edge of the rod
    .circle(10.90 / 2)            # New smaller diameter
    .cutBlind(-1)                 # Cut upward 1 mm
)

# Now create the actual thread geometry for the bottom 2 mm of the rod using
# IsoThread from the cq_warehouse library.
# - major_diameter=11.5 (nominal M11.5)
# - pitch=0.5
# - length=2
# - external=True => male (external) thread
# - end_finishes=('fade', 'square') => fade at the bottom, square at top
# - simple=False => full detailed thread geometry
pitch = 0.5
major_diam = 11.5
thread_length = 2

iso_thread = cq.Solid(IsoThread(
    major_diameter=major_diam,
    pitch=pitch,
    length=thread_length,
    external=True,
    hand='right',
    end_finishes=('fade', 'square'),
    simple=False
).wrapped)

# By default, IsoThread is oriented with z=0..thread_length, so we can place it
# so its bottom is at z=0. If your rod’s bottom is at z=0, you don’t need extra
# translation. But if you want to seat it differently, use .translate((0,0,z_offset)).
thread = iso_thread.translate((0, 0, 0))

# 5) Union the new thread geometry onto the rod portion
model = model.union(thread)

# 6) Drill the magnet holes around the top face
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

# --------------------------------------------------------------------------------
# Export the final model to both STEP and STL so you can see the actual male threads
# in your CAD viewer or for a technical drawing.
# --------------------------------------------------------------------------------
cq.exporters.export(model, "male_thread_visual.step")
cq.exporters.export(model, "male_thread_visual.stl")
