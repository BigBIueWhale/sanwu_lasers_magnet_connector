import cadquery as cq

# 1) Create the main cylinder:
#    Height: 6.00 mm
#    Diameter: 24 mm (diameter)
model = (
    cq.Workplane("XY")
    .circle(24 / 2)
    .extrude(6.00)
)

# 2) We're using M11.5x0.5 ISO Metric fine thread, so we'll use
#    initial hole of 11.55mm (for tolerance).
model = (
    model
    .faces(">Z")              # pick the top face
    .workplane()              # new workplane for the through hole
    .hole(11.55)              # create the through hole
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

# Chamfer the female screw hole on top for easier male insertion
model = (
    model
    .faces(">Z")                           # pick the top face
    # keep only the circular edge(s) matching the hole diameter
    .edges(SpecificCircularEdgeSelector(diameter=11.55))
    .chamfer(0.3)
)

# 4) Drill the magnet holes around the bottom face
#    - 12 holes
#    - Each hole diameter: 4.16 mm
#    - Hole depth: 3.3 mm
#    - Hole centers on a circle of radius: 9.3mm and are equally spaced.
model = (
    model
    .faces("<Z")               # pick the bottom face
    .workplane()               # new workplane for drilling
    .polarArray(radius=9.3, startAngle=0, angle=360, count=12, fill=True)  # 12 holes in a full circle
    .hole(diameter=4.16, depth=3.3)  # create the holes as pockets
)

# === Export the final model to both STEP and STL files ===
output_file_step = "female_thread.step"
output_file_stl  = "female_thread.stl"

cq.exporters.export(model, output_file_step)
cq.exporters.export(model, output_file_stl)