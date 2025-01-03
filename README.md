# Problem Statement

SanwuLasers™️ Lasers such as Striker, Challenger II, Laser Rangers all have option for high powered blue diode (~7 watts).

SanwuLasers™️ offers flashlight adapters that [can be screwed onto the top](./docs/laser_and_flashlight_adapter.jpg). It's generic, the flashlight adapter fits all of the aforementioned host types.

Problem is: It takes way too long to physically unscrew the flashlight adapter, and it's way too annoying to screw it back on. It should be possible to just pull it off, and snap it right back in place 🧲.

[magnet holes standard triangle language](./magnet_holes.stl)

![Fully assembled](./docs/xometry_final_result_cropped.png)

# Solution

Custom order for CNC machined stainless steel part that converts the screw-on mechanism into a magnetic mechanism!

The flashlight adapter can be ordered with an [Adapter for striker](#threads). This adapter is super useful because it's already threaded with male and female sides.

The generic custom machined part has 16 small holes, each 4.10mm in diameter and 3.30mm depth.

It just so happens that in practice, my choice of 3.30mm depth works with the [neodymium disc magnets](./docs/neodymium_magnets_amazon_listing.png) I chose, which according to the listing are **2mm in height** (apparently they're less). 

It just so happens that the specific magnets I bought, somehow [fit perfectly](./docs/two_stacked_magnets_fit_in_3.3mm_hole_perfectly.jpg) into the 3.3mm hole when two are stacked on each other in each hole and with super glue prepared at the bottom (no super glue between the two magnets).

The magnets are **very** slightly extruding which does cause purple light to be slightly visible when flashlight mode is on, but it's still a [tight fit](./docs/tight_fit_despite_magnets_slightly_extruding.jpg).

The small gap is also a feature- it causes the flashlight adapter to **not** be air-tight which makes it easier to change focus without causing a vacuum (which was a feature that was bothering me in the default flashlight adapter behaviour).

I originally chose 4.04mm hole width but that was not enough to leave room for machine tolerance and temperature changes, so then I changed the design to 4.10mm hole to make it easier to push-in the magnets.

# Process

I learned the recently released `FreeCAD 1.0.0`, but I gave up on the design once I understood that the software requires the user to draw shapes with my laptop's touchpad. I'm not an artist 🎨🧑‍🎨.

I decided it's much more robust to define the 3d design with words and precise measurements than it is to start drawing like a preschool child.

Therefore **for the initial version** I had `ChatGPT o1` write Python code to generate both a `.step` file and an `.stl` file, using [this prompt](./prompt.txt).

I use the `.stl` file to view the design in `Microsoft Paint 3d`, I then uploaded the `.step` file as-is to `Xometry` website.

I chose standard stainless steel [settings in the website](./docs/xometry_order_settings.png) with the lowest tolerance quality.

The reason I chose such a low tolerance quality is that I'm using super glue and I made the holes slightly bigger than they need to be, so it's fine. Also, I want the CNC machine to just do everything automatically to avoice human error.

# Threads

This adapter from SanwuLasers™️ is the base of my design.\
It already comes with [male threads](./docs/sanwu_striker_adapter_male_view.jpg) and [female threads](./docs/sanwu_striker_adapter_female_view.jpg).

The part can be ordered via its [dedicated listing](./docs/sanwu_adapter_order_separately.png) on the website, or as part of the [flashlight converter listing](./docs/sanwu_adapter_in_flashlight_converter_listing.png).

The adapter is 17.55 mm in diameter, so I cut a 17.60mm hole in the cylinder of my custom design.

I [cut the adapter in half](./docs/sanwu_adapter_cut_in_half.jpg) using a [diamond blade circular saw](./docs/angle_grinder/angle_grinder_readme.pdf), sand it down, and super glue the male part into the large hole in one of my generic custom machined parts, and the female part of the adapter from Sanwu into another unit of my generic custom machined part.

This is my alternative to reverse-engineering the threads that Sanwu uses.

Just for general knowledge, Sanwu uses the following threading specs:

- Male:
  ```txt
  CNC machined
  Metric right-handed male threaded rod
  11.45mm diameter teeth (crest-to-crest). 0.05mm smaller diameter than the female tap.
  0.5mm pitch
  3mm length out of which only the tip 2mm are threaded and the base 1mm runoff is shaved down and not threaded.
  That's total of 4 threads.
  ```
- Female (laser head):
  ```txt
  CNC machined
  Metric right-handed female
  m11.5x0.5 tap (11.5mm diameter, 0.5mm pitch)
  6mm depth- total of 12 threads
  ```

I chose to use threads from an existing SanwuLasers™️ adapter instead of printing my custom part [with designed threads](./docs/attempt_design_screw.png) for multiple reasons:
1. 11.5mm diameter is not standard.
2. Thread specification required English language specification, and can only exist in a step file for show (being pretty). This makes the whole process more expensive, and less automatic- it might make it hard for the CNC machine to know what to do!
3. I can always later design another custom stainless steel piece to fit into the generic 17.60mm hole with super glue, and I can decide to make it have threads! This incurs less risk by making the components modular.
4. Generic- single design works as either male or female screw side. Only having to print one step file multiple times is significantly cheaper because it only requires one preparation stage for Xometry.

# Recreate 3d model from code

You can decide to change parameters in [main.py](./main.py) then re-run the script to update the design files.

## Requirements
- Tested on Windows 11 Pro 23H2
- Ran with Python 3.10.6
- Specific versions chose: `pip install cadquery==2.4.0 numpy==1.23.5`

## Run
1. Delete the existing `.step` file and `.stl` file.
2. Run command `python magnet_holes_01_00_01.py` in a cmd Window in the same directory as the project folder.
3. Use the newly created `magnet_holes.stl` and `magnet_holes.step` for the male and female sides (upload to PCBWay CNC machining, or to Xometry).

# Release Notes

## magnet_holes_01_00_01
- 4.10mm diameter magnet holes for better fitting

## magnet_holes_01_00_00
[magnet_holes_01_00_00.py](./magnet_holes_01_00_00.py)\
[Final result](./docs/xometry_final_result.jpg)

- 4.04mm diameter magnet holes
- 5 units ordered with https://get.xometry.eu/payments/ec0325ff-71c7-4672-9496-26f8077902b1
