import cadquery as cq

# python3 -m pip install git+https://github.com/gumyr/cq_warehouse.git#egg=cq_warehouse
# Currently using: cq_warehouse==0.8.0
from cq_warehouse.fastener import IsoThread

# --------------------------------------------------------------------------------
# Create the main cylinder body
# Height: 6.5 mm total (3 mm of "rod" + 3.5 mm for magnet holes)
# Diameter: 24 mm
# --------------------------------------------------------------------------------
model = (
    cq.Workplane("XY")
    .circle(24 / 2)
    .extrude(6.5)
)

# --------------------------------------------------------------------------------
# Drill an 8 mm diameter through-hole from the bottom face all the way.
# --------------------------------------------------------------------------------
model = (
    model
    .faces("<Z")  # Select the bottom face
    .workplane()
    .hole(8)      # Through-hole 8 mm diameter for laser light
)

# Approximate minor diameter of m11.5x0.5 ISO Metric fine thread
minor_diameter = 10.88657

# --------------------------------------------------------------------------------
# Create a 3 mm deep pocket at the bottom, leaving a base rod for the thread
# --------------------------------------------------------------------------------
model = (
    model
    .faces("<Z")          # Select the bottom face
    .workplane()
    .circle(24 / 2)       # Outer diameter
    .circle(minor_diameter / 2)    # Keep the center region
    .cutBlind(-3)         # Remove 3 mm upward from the bottom
)

# --------------------------------------------------------------------------------
# Now create the actual thread geometry for the bottom 2 mm of the rod using
# IsoThread from the cq_warehouse library.
#   - major_diameter=11.5 (nominal M11.5)
#   - pitch=0.5
#   - length=2
#   - external=True => male (external) thread
#   - end_finishes=('fade', 'square') => fade at the bottom, square at top
#   - simple=False => full detailed thread geometry
# --------------------------------------------------------------------------------
pitch = 0.5
major_diam = 11.5
thread_length = 2

iso_thread = IsoThread(
    major_diameter=major_diam,
    pitch=pitch,
    length=thread_length,
    external=True,
    hand='right',
    end_finishes=('fade', 'square'),
    simple=False
).cq_object

# By default, IsoThread is oriented with z=0..thread_length, so we can place it
# so its bottom is at z=0. If your rod’s bottom is at z=0, you don’t need extra
# translation. But if you want to seat it differently, use .translate((0,0,z_offset)).
thread = iso_thread.translate((0, 0, 0))

# Union the new thread geometry onto the rod portion
model = model.union(thread)

# --------------------------------------------------------------------------------
# Drill the magnet holes around the TOP face (z=6.5) of the main cylinder
#   - 12 holes
#   - hole diameter: 4.16 mm
#   - hole depth: 3.3 mm
#   - holes centered on a circle radius=9.3 mm
# --------------------------------------------------------------------------------
model = (
    model
    .faces(">Z")  # pick the top face at z=6.5
    .workplane()
    .polarArray(radius=9.3, startAngle=0, angle=360, count=12, fill=True)
    .hole(diameter=4.16, depth=3.3)
)

# --------------------------------------------------------------------------------
# Export the final model to both STEP and STL so you can see the actual male threads
# in your CAD viewer or for a technical drawing.
# --------------------------------------------------------------------------------
cq.exporters.export(model, "male_thread_visual.step")
cq.exporters.export(model, "male_thread_visual.stl")
