"""
Full CadQuery script to create:
- A 10 mm tall x 26 mm diameter cylinder
- 8 mm through-hole
- Bottom 3 mm turned into an external (male) M11.5 x 0.5 ISO fine thread
- Top 6 mm tapped as an internal (female) M11.5 x 0.5 ISO fine thread
- Exports an STL file of the final part
"""

import cadquery as cq

# You must install cq_warehouse from GitHub (not on PyPI):
#   python -m pip install git+https://github.com/gumyr/cq_warehouse.git#egg=cq_warehouse
from cq_warehouse.thread import IsoThread

# -----------------------------
# Parameters
# -----------------------------
BASE_HEIGHT = 10.0      # total height of the base cylinder (mm)
BASE_DIAM = 26.0        # outer diameter of the base cylinder (mm)
HOLE_DIAM = 8.0         # central through-hole (mm)

THREAD_PITCH = 0.5      # DIN 13-3, M11.5 x 0.5
THREAD_MAJOR_D = 11.5   # nominal diameter for M11.5

MALE_THREAD_LEN = 3.0   # length of external thread at bottom (mm)
FEMALE_THREAD_LEN = 6.0 # depth of internal thread at top (mm)

# -----------------------------
# 1) Create the base cylinder
# -----------------------------
# We'll build this in two parts to simplify combining with the threaded sections:
#   - The bottom 3 mm section (which we'll replace with external threads),
#   - The top 7 mm section (unchanged 26 mm diameter).
bottom_height = MALE_THREAD_LEN
top_height = BASE_HEIGHT - bottom_height

# Create a 3 mm cylinder for the bottom:
bottom_cyl = (
    cq.Workplane("XY")
    .circle(BASE_DIAM / 2.0)
    .extrude(bottom_height)
)

# Create a 7 mm cylinder for the top:
top_cyl = (
    cq.Workplane("XY")
    .circle(BASE_DIAM / 2.0)
    .extrude(top_height)
    # Shift it upward by 3 mm so it sits above the bottom portion
    .translate((0, 0, bottom_height))
)

# -----------------------------
# 2) Create the external (male) thread for the bottom 3 mm
# -----------------------------
male_thread_solid = IsoThread(
    major_diameter=THREAD_MAJOR_D,
    pitch=THREAD_PITCH,
    length=MALE_THREAD_LEN,
    external=True,                # "external" => male thread
    end_finishes=("square", "square"),  # make ends easy to intersect
    simple=False                  # full detailed thread geometry
)
# By default, IsoThread is aligned along Z from 0..length
# So the male thread goes from z=0 to z=3
# No translation needed for the bottom—just leave as-is.

# Intersect that 3 mm cylinder with the male thread shape
# to remove all material except the threaded form:
threaded_bottom = bottom_cyl.intersect(male_thread_solid)

# Combine the threaded bottom with the top cylinder:
model = threaded_bottom.union(top_cyl)

# -----------------------------
# 3) Create the internal (female) thread for the top 6 mm
# -----------------------------
female_thread_solid = IsoThread(
    major_diameter=THREAD_MAJOR_D,
    pitch=THREAD_PITCH,
    length=FEMALE_THREAD_LEN,
    external=False,               # "external=False" => female (internal) thread
    end_finishes=("square", "square"),
    simple=False
)
# The internal thread is modeled from z=0..6 by default,
# but we want it at the TOP of the part, from z=(10-6)=4..10.
female_thread_solid = female_thread_solid.translate((0, 0, BASE_HEIGHT - FEMALE_THREAD_LEN))

# Subtract the female thread volume from the main part
# so that "inside" is now tapped:
model = model.cut(female_thread_solid)

# -----------------------------
# 4) Add the 8 mm through-hole
# -----------------------------
# Finally, drill an 8 mm hole down the entire center:
model = model.faces(">Z").workplane().hole(HOLE_DIAM)

# -----------------------------
# 5) Export to STL
# -----------------------------
cq.exporters.export(model, "threads.stl")
