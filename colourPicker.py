#! /usr/bin/env python

import numpy as np
from bokeh import plotting as bkplt
from bokeh.models import LinearColorMapper, HoverTool, TapTool
from bokeh.models.actions import Callback
from bokeh.models.widgets import Slider
from bokeh.io import vform
import colorsys

def generate_color_range(N, I):
	HSV_tuples = [ (x*1.0/N, 0.5, I) for x in range(N) ]
	RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
	for_conversion = []
	for tuple in RGB_tuples:
		for_conversion.append((tuple[0]*255, tuple[1]*255, tuple[2]*255))
	hex_colors = [ rgb_to_hex(rgb_tuple) for rgb_tuple in for_conversion ]
	return hex_colors

def rgb_to_hex(rgb):
	return '#%02x%02x%02x' % rgb

def hex_to_dec(hex):
	red = ''.join(hex.strip('#')[0:2])
	green = ''.join(hex.strip('#')[2:4])
	blue = ''.join(hex.strip('#')[4:6])
	return (int(red, 16), int(green, 16), int(blue,16))

x = [0]
y = [0]
red   = 255
green = 255
blue  = 255
hex_color = rgb_to_hex((red,green,blue))

text_color = '#000000'

source = bkplt.ColumnDataSource(data=dict(x = x, y = y, color = [hex_color], text_color = [text_color]))

p1 = bkplt.figure(x_range=(-8, 8), y_range=(-4, 4), plot_width=600, plot_height=300, title=None)
color_block = p1.rect(x='x', y='y', width=18, height=10, fill_color='color', line_color = 'black', source=source)
hex_code_text = p1.text('x', 'y', text='color', text_color='text_color', alpha=0.6667, text_font_size='36pt', text_baseline='middle', text_align='center', source=source)

callback = Callback(args=dict(source=source), code="""
	function componentToHex(c) {
		var hex = c.toString(16);
		return hex.length == 1 ? "0" + hex : hex;
	}
	function rgbToHex(r, g, b) {
		return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
	}
	var data = source.get('data');
	var RS = red_slider;
	var GS = green_slider;
	var BS = blue_slider;
	color = data['color'];
	var red_from_slider = RS.get('value');
	var green_from_slider = GS.get('value');
	var blue_from_slider = BS.get('value');
	text_color = data['text_color'];
	color[0] = rgbToHex(red_from_slider, green_from_slider, blue_from_slider);
	if ((red_from_slider > 127) || (green_from_slider > 127) || (blue_from_slider > 127)) {
		text_color[0] = '#000000';
	}
	else {
		text_color[0] = '#ffffff';
	}
	source.trigger('change');
""")

intensity = 0.8
crx = range(1,1001)
cry = [ 5 for i in range(len(crx)) ]
crcolor = generate_color_range(1000,intensity)

crsource = bkplt.ColumnDataSource(data=dict(x = crx, y = cry, crcolor = crcolor))

tools = 'reset, save, hover'

p2 = bkplt.figure(x_range=(0,1000), y_range=(0,10), plot_width=600, plot_height=150, tools=tools, title = 'pick color')
color_range1 = p2.rect(x='x', y='y', width=1, height=10, color='crcolor', source=crsource)

hover = p2.select(dict(type=HoverTool))
hover.tooltips = [('color', '$color[hex, swatch]:crcolor')]


red_slider = Slider(start=0, end=255, value=255, step=1, title="R", callback=callback)
green_slider = Slider(start=0, end=255, value=255, step=1, title="G", callback=callback)
blue_slider = Slider(start=0, end=255, value=255, step=1, title="B", callback=callback)
callback.args['red_slider'] = red_slider
callback.args['green_slider'] = green_slider
callback.args['blue_slider'] = blue_slider

p1.ygrid.grid_line_color = None
p1.xgrid.grid_line_color = None
p1.axis.axis_line_color  = None
p1.axis.major_label_text_color = None
p1.axis.major_tick_line_color = None
p1.axis.minor_tick_line_color = None

p2.ygrid.grid_line_color = None
p2.xgrid.grid_line_color = None
p2.axis.axis_line_color  = None
p2.axis.major_label_text_color = None
p2.axis.major_tick_line_color = None
p2.axis.minor_tick_line_color = None

layout = bkplt.hplot(
    vform(red_slider, green_slider, blue_slider),
    vform(p1, p2)
)

bkplt.output_file("colourPicker.html")
bkplt.show(layout)