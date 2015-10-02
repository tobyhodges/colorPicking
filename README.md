# colorPicking

UPDATE: As of v0.9 of bokeh, a version of this script was included in the usage examples for the module. The version of the script provded here will no longer work with more recent releases of Bokeh. I recommend instead looking at the version at https://github.com/bokeh/bokeh/blob/master/examples/plotting/file/color_sliders.py.

REQUIRES: Python 2.7 and the 'bokeh' python library. Version 0.82 (the latest stable release ATOW) doesn't include the Callback functionality required for updating the color of the first plot, so you will need to install the master version from the developers' [GitHub page](https://github.com/bokeh/bokeh). Written and tested on Mac OSX 10.10 (Yosemite).

Execute the Python script to produce an HTML file of two plots. The first plot allows a color to be chosen by changing the RGB ratio using the sliders on the left. The second plot shows a spectrum, with a hover tool to show the hex codes. 

  `python colorPicker.py`
