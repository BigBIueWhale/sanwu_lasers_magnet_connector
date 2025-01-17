import cadquery as cq

# 1) Create the main cylinder:
#    Height: 6.00 mm
#    Diameter: 24 mm (diameter)
model = (
    cq.Workplane("XY")
    .circle(24 / 2)
    .extrude(6.00)
)

# Minor diameter of M11.5x0.5 ISO Metric fine thread
# Calculation: (d₂) = 11.5 - 2 × (5/8 × (0.5 × √3/2))
# NOMINAL_MINOR_DIAMETER = 10.9587

# 2) We're using M11.5x0.5 ISO Metric fine thread, so we'll use
#    initial hole of 10.95mm.
#    That's just good enough for the threading tool to dig in.
#    Any number from 10.90 - 10.96 could probably work.
THROUGH_HOLE_DIAMETER = 10.95
model = (
    model
    .faces(">Z")                 # pick the top face
    .workplane()                 # new workplane for the through hole
    .hole(THROUGH_HOLE_DIAMETER) # create the through hole
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

# 4) Drill the magnet holes around the bottom face
#    - 12 holes
#    - Each hole diameter: 4.11 mm (4.06 diameter magnets with 5mm tolerance)
#    - Hole depth: 3.3 mm (still have 1mm floor)
#    - Hole centers on a circle of radius: 9.3mm and are equally spaced.
model = (
    model
    .faces("<Z")               # pick the bottom face
    .workplane()               # new workplane for drilling
    .polarArray(radius=9.3, startAngle=0, angle=360, count=12, fill=True)  # 12 holes in a full circle
    .hole(diameter=4.11, depth=3.3)  # create the holes as pockets in the top
)

# === Export the final model to both STEP and STL files ===
output_file_step = "female_thread.step"
output_file_stl  = "female_thread.stl"

cq.exporters.export(model, output_file_step)
cq.exporters.export(model, output_file_stl)
