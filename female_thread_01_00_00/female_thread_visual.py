import cadquery as cq

# python3 -m pip install git+https://github.com/gumyr/cq_warehouse.git#egg=cq_warehouse
# Currently using: cq_warehouse==0.8.0
from cq_warehouse.fastener import IsoThread

# 1) Create the main cylinder:
#    Height: 6.00 mm
#    Diameter: 24 mm (diameter)
model = (
    cq.Workplane("XY")
    .circle(24.0 / 2)
    .extrude(6.0)
)

# 2) For a visual internal thread, make the through-hole 11.5 mm in diameter
#    so that the “female thread” model can be unioned inside.
THROUGH_HOLE_DIAMETER = 11.5

model = (
    model
    .faces(">Z")                 # pick the top face
    .workplane()
    .hole(THROUGH_HOLE_DIAMETER) # create the larger through hole
)

class SpecificCircularEdgeSelector(cq.selectors.Selector):
    """
    A custom selector to filter only the internal circular edge
    of the specified hole diameter.
    """
    def __init__(self, diameter):
        self.target_diameter = diameter
    
    def filter(self, objectList):
        # Return only edges that are circular and match the target diameter
        return [
            edge for edge in objectList 
            if edge.geomType() == "CIRCLE" and abs(edge.radius() * 2 - self.target_diameter) < 1e-5
        ]

# 3) Chamfer the female screw hole on top for easier male engagement
model = (
    model
    .faces(">Z")                           # pick the top face
    # keep only the circular edge(s) matching the hole diameter
    .edges(SpecificCircularEdgeSelector(diameter=THROUGH_HOLE_DIAMETER))
    .chamfer(0.3)
)

# Create the visual internal (female) thread.
#  - major_diameter=11.5 (nominal M11.5)
#  - pitch=0.5
#  - length=6 mm (entire thickness)
#  - external=False => female (internal) thread
#  - end_finishes=('square','fade') => square at bottom, fade at top (so chamfer looks nice)
#  - simple=False => full detailed thread geometry
pitch = 0.5
major_diam = 11.5
# Slightly less than full actual height, not to visually overwhelm the chamfer
thread_length = 5.80

iso_thread = cq.Solid(
    IsoThread(
        major_diameter=major_diam,
        pitch=pitch,
        length=thread_length,
        external=False,
        hand='right',
        end_finishes=('square', 'fade'),
        simple=False
    ).wrapped
)

# 4) Union the internal thread geometry with the larger hole cylinder
model = model.union(iso_thread)

# 5) Drill the magnet holes around the bottom face
#    - 12 holes
#    - Each hole diameter: 4.11 mm (4.06 diameter magnets with tolerance)
#    - Hole depth: 3.3 mm
#    - Hole centers on a circle of radius: 9.3mm
model = (
    model
    .faces("<Z")  # pick the bottom face
    .workplane()
    .polarArray(radius=9.3, startAngle=0, angle=360, count=12, fill=True)
    .hole(diameter=4.11, depth=3.3)
)

# === Export the final model to both STEP and STL files ===
output_file_step = "female_thread_visual.step"
output_file_stl  = "female_thread_visual.stl"

cq.exporters.export(model, output_file_step)
cq.exporters.export(model, output_file_stl)
