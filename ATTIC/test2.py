#!/usr/bin/python

import sys, os, logging, time, argparse
import pkgutil
import epdlib
import waveshare_epd
from epdlib import Screen
from epdlib import Layout
from epdlib import constants
from rpi_status import INA219
from rpi_status import Status

def power_state(ups):
  power_state = '-'
  if ups.getCurrent_mA() > 0:
    power_state = '+'

  p = (ups.getBusVoltage_V() - 3)/1.2 * 100
  if p > 100:
    p = 100
  elif p < 0:
    p = 0

  return '%s%d%%' % (power_state, p)


logging.basicConfig(level=logging.DEBUG)
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--font', dest='font', default='./resources/fhwa-series-d.otf', help='Specify path to font file to use.')
parser.add_argument('-s', '--symbol', dest='symbol', default='./resources/aristotelica.icons-bold.ttf', help='Specify path to symbol font to use.')
args = parser.parse_args()

myepd = 'epd2in13_V4'
voltage = 0.0

myLayout = {
        'system': {                       # text only block
            'type': 'TextBlock',
            'image': None,               # do not expect an image
            'max_lines': 4,              # number of lines of text
            'width': 1,                  # 1/1 of the width - this stretches the entire width of the display
            'height': .3,               # 1/3 of the entire height
            'abs_coordinates': (0, 0),   # this block is the key block that all other blocks will be defined in terms of
            'relative': False,           # this block is not relative to any other. It has an ABSOLUTE position (0, 0)
            'font': args.font, 
            'font_size': None ,
            'border_config':  {'fill': 'WHITE', 'width': 1, 'sides': ['bottom']},
        },

        'timelapse': {
            'type': 'TextBlock',
            'max_lines': 4,
            'width': .5,
            'height': .3,
            'abs_coordinates': (0, None),
            'font': args.font,
            'relative': ['timelapse', 'system'],
            'border_config':  {'fill': 'WHITE', 'width': 1, 'sides': ['right']},
        },

        'timelapseicon': {
          'type': 'ImageBlock',
          'image': True,
          'padding': 3,
          'width': .5,
          'height': .3,
          'abs_coordinates': (None,None),
          'relative': ['timelapse','system'],
        },

        'camera': {
            'type': 'TextBlock',
            'image': None,
            'max_lines': 4,
            'width': 1,
            'height': .3,
            'abs_coordinates': (0, None),   # X = 0, Y will be calculated
            'hcenter': False,
            'vcenter': False,
            'font': str('./resources/Font.ttc'), # path to font file
            'relative': ['camera', 'timelapse'],
            'border_config':  {'fill': 'WHITE', 'width': 1, 'sides': ['top']},
        }
}


logging.debug(f"using font: {myLayout['system']['font']}")
ups = INA219.INA219(addr=0x43)
s = Screen(epd=myepd, vcom=voltage, mode='RGB')

s.rotation = 90
l = Layout(resolution=s.resolution)
l.layout = myLayout

try:
  while True:

    l.update_block_props('system', {}, force_recalc=True)
    l.update_block_props('timelapse', {}, force_recalc=True)
    l.update_block_props('camera', {}, force_recalc=True)

    timelapse = Status.In('/tmp/rpi-timelapse.json').get()
    logging.debug(timelapse)

    l.update_contents({'system': power_state(ups), 'timelapse': timelapse['captures'], 'timelapseicon': timelapse['last_file'], 'camera': '0.00sec'})
    logging.debug('print some text on the display')

    try:
      s.writeEPD(l.concat())
    except FileNotFoundError as e:
      logging.error(f'{e}')
      logging.error('Try: $ raspi-config > Interface Options > SPI')
      do_exit = True
    else:
      do_exit = False

    if do_exit:
      sys.exit()

#    sleeptime = 0.2
#    logging.debug('sleeping for %f seconds' % (sleeptime))
#    time.sleep(sleeptime)

except (KeyboardInterrupt, SystemExit):
    logging.info('exit time, clear screen')
    s.clearEPD()

