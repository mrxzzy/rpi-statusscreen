#!/usr/bin/python

import sys, os, logging, time, argparse
import subprocess
from PIL import Image,ImageDraw,ImageFont
from rpi_status import epd2in13_V4
from rpi_status import INA219
from rpi_status import DisplayBuilder
from rpi_status import Status

def power_state(ups):

  cur_amps = ups.getCurrent_mA()/1000
  if cur_amps > 0.01: 
    power_state = '+'
  elif cur_amps < 0: 
    power_state = '-'
  else:
    power_state = '='

  p = (ups.getBusVoltage_V() - 3)/1.2 * 100
  if p > 100:
    p = 100
  elif p < 0:
    p = 0

  # surely this is the best place to put logic to shut the system down
  if(p < 15 and power_state == '-'):
    call("sudo shutdown --poweroff", shell=True)

  if power_state == '=':
    return '100%'

  return '%s%d%%' % (power_state, p)

def load_average():
  load = os.getloadavg()[0]

  return "%0.2f" % (load)

def media_usage(path):
  if os.path.ismount(path):
    usage = os.statvfs(path)
    return "Disk: %d%%" % ((1 - usage.f_bfree / usage.f_blocks) * 100)
  else:
    return 'No media'

def when():
  return time.strftime('%H:%M:%S')

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--image', dest='image', action='store_true', help='For debugging purposes, display an image with pillow instead of refreshing the ePaper screen')
parser.add_argument('-f', '--font', dest='font', default='/usr/share/fonts/xzzycam/DinaRemasterII.ttc', help='Specify path to font file to use.')
parser.add_argument('-s', '--shutdown', action='store_true', help='Run with this option to blank the epaper screen.')
args = parser.parse_args()

if args.shutdown:
  logging.basicConfig(level=logging.DEBUG)
  logging.debug("Blanking e-paper in preparation for shutdown.")
  epd = epd2in13_V4.EPD()
  epd.init()
  epd.Clear(0xFF)
  epd.sleep()
  sys.exit(0)

try:
  logging.basicConfig(level=logging.DEBUG)

  logging.debug("Initializing e-paper display")
  if not args.image:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    width = epd.width
    height = epd.height
  else:
    width = 122
    height = 250

  logging.debug("display init successful. display size: %s w, %s h" % (width, height))

  buffer = DisplayBuilder.DisplayBuilder(height,width,args.font)

  # init UPS interface

  logging.debug("initializing UPS.")
  ups = INA219.INA219(addr=0x43)
  logging.debug("UPS initialization successful.")

except Exception as e:
  logging.error("init failed: %s" % (e))
  sys.exit(1)

try: 
  epd.displayPartBaseImage(epd.getbuffer(buffer.get()))
  while True:

    buffer.blank()

    # draw the OS stats at the top
    buffer.text_in_spot(0,0,"Bat: %s" % (power_state(ups)))
    buffer.text_in_spot(0,buffer.textheight,"Load: %s" % (load_average()))
    buffer.text_in_spot(0,buffer.textheight * 2, media_usage('/media/dest'))
    buffer.text_in_spot(0,buffer.textheight * 3, when())

    # draw the timelapse gui
    timelapse = Status.In('/tmp/rpi-timelapse.json').get()
    logging.debug(timelapse)
    if timelapse is not False:
      buffer.text_in_spot(0,103,str(timelapse['captures']))

      if os.path.exists('/tmp/rpi-eclipse.json'):
        buffer.image_in_spot((64,103),(58,58),timelapse['last_file'])
      else:
        buffer.image_in_spot((0,153),(123,160),timelapse['last_file'])
    else:
      y = 103
      buffer.text_in_spot(0,y,str("No"))
      buffer.text_in_spot(0,y + buffer.textheight,str("JSON"))

    if args.image:
      buffer.show()
      sys.exit(0)
    else:
      epd.displayPartial(epd.getbuffer(buffer.get()))

    time.sleep(1)

except (KeyboardInterrupt, SystemExit):
  logging.info("done, cleaning up and exiting")

  if not args.image:
    epd.init()
    epd.Clear(0xFF)
