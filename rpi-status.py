#!/usr/bin/python

import sys, os, logging, time, argparse
from waveshare_epd import epd2in13_V4
from PIL import Image,ImageDraw,ImageFont
from rpi_status import INA219
from rpi_status import DisplayBuilder

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--image', dest='image', action='store_true', help='For debugging purposes, display an image with pillow instead of refreshing the ePaper screen')
parser.add_argument('-f', '--font', dest='font', default='./resources/fhwa-series-d.otf', help='Specify path to font file to use.')
parser.add_argument('-s', '--symbol', dest='symbol', default='./resources/aristotelica.icons-bold.ttf', help='Specify path to symbol font to use.')
args = parser.parse_args()

try:
  logging.basicConfig(level=logging.DEBUG)

  if not args.image:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    width = epd.width
    height = epd.height
  else:
    width = 122
    height = 250

  logging.info("init successful. display size: %s w, %s h" % (width, height))

  buffer = DisplayBuilder.DisplayBuilder(width,height,args.font,args.symbol)

  # init UPS interface
  ups = INA219.INA219(addr=0x43)

except Exception as e:
  logging.error("init failed: %s" % (e))
  sys.exit(1)

try: 
  #epd.displayPartBaseImage(epd.getbuffer(buffer.image))

  #buffer.text_in_spot(0,10,30,buffer.textheight,"Hq")
  #epd.displayPartial(epd.getbuffer(buffer.image))
  while True:
    # if the current is negative, we are on ups power
    if ups.getCurrent_mA() > 0:
      power_state = '+'
    else:
      power_state = '-'

    # get the battery percentage
    p = (ups.getBusVoltage_V() - 3)/1.2*100
    if p > 100:
      p = 100
    elif p < 0:
      p = 0

    logging.info("battery: %s %d" % (power_state,p))
    buffer.text_in_spot(0,0,90,buffer.textheight, "%s%dp" % (power_state,p))

    if args.image:
      buffer.show()
      sys.exit(0)

    time.sleep(1)

except (KeyboardInterrupt, SystemExit):
  logging.info("done, cleaning up and exiting")

  if not args.image:
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()
