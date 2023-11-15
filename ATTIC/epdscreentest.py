#!/usr/bin/python

import pkgutil
import sys, time
import epdlib
from epdlib.Screen import list_compatible_modules
from epdlib import Screen

import waveshare_epd

print('loading Layout module')
try:
    from epdlib import Layout
    from epdlib import constants
except ModuleNotFoundError:
    try:
        print('trying alternative module')
        from Layout import Layout
        import constants
    except ModuleNotFoundError:
        sys.exit('failed to import')

panels = []
panels = list_compatible_modules()

print(f"{len(panels)-1}. {panels[-1]['name']}")

choice = input('Enter the number of your choice: ')

try:
    choice = int(choice)
except ValueError as e:
    print(f'"{choice}" does not appear to be an valid choice. Exiting.')
    sys.exit(0)
myepd = panels[choice]['name']

print(panels[choice]['name'])

if choice > len(panels)+1:
    print(f'"{choice}" is not a valid panel option. Exiting.')
    sys.exit(0)

if 'IT8951' in myepd:
    myepd = 'HD'
    voltage = input('Enter the vcom voltage for this panel (check the ribbon cable): ')
    try:
        voltage = float(voltage)
    except ValueError as e:
        print('vcom voltage must be a negative float. Exiting')
        sys.exit(0)
    if voltage > 0:
        print('vcom voltage must be a negative float. Exiting.')
        sys.exit(0)
else:
    voltage = 0.0

sys.path.append('../')

myLayout = {
        'title': {                       # text only block
            'type': 'TextBlock',
            'image': None,               # do not expect an image
            'max_lines': 3,              # number of lines of text
            'width': 1,                  # 1/1 of the width - this stretches the entire width of the display
            'height': .6,               # 1/3 of the entire height
            'abs_coordinates': (0, 0),   # this block is the key block that all other blocks will be defined in terms of
            'hcenter': True,             # horizontally center text
            'vcenter': True,             # vertically center text
            'relative': False,           # this block is not relative to any other. It has an ABSOLUTE position (0, 0)
            'font': str('./resources/Font.ttc'), # path to font file
            'font_size': None            # Calculate the font size because none was provided
        },

        'artist': {
            'type': 'TextBlock',
            'image': None,
            'max_lines': 2,
            'width': 1,
            'height': .4,
            'abs_coordinates': (0, None),   # X = 0, Y will be calculated
            'hcenter': True,
            'vcenter': True,
            'font': str('./resources/Font.ttc'), # path to font file
            'relative': ['artist', 'title'],# use the X postion from abs_coord from `artist` (this block: 0)
                                            # calculate the y position based on the size of `title` block

            'fill': 'Yellow',
            'bkground': 'Black'
        }
}

print(f"using font: {myLayout['title']['font']}")
s = Screen(epd=myepd, vcom=voltage, mode='RGB')

for r in [0, 90, 180]:
    print(f'setup for rotation: {r}')
    s.rotation = r
    l = Layout(resolution=s.resolution)
    l.layout = myLayout
    l.update_block_props('title', {}, force_recalc=True)
    l.update_block_props('artist', {}, force_recalc=True)
    l.update_contents({'title': 'item: spam, spam, spam, spam & ham', 'artist': 'artist: monty python'})
    print('print some text on the display')

    try:
        s.writeEPD(l.concat())
    except FileNotFoundError as e:
        print(f'{e}')
        print('Try: $ raspi-config > Interface Options > SPI')
        do_exit = True
    else:
        do_exit = False

    if do_exit:
        sys.exit()
    print('sleeping for 2 seconds')
    time.sleep(2)


    print('refresh screen -- screen should flash and be refreshed')
print('mirror output')
s.mirror = True
s.rotation = 0
s.writeEPD(l.concat())
time.sleep(3)

print('clear screen')
s.clearEPD()

