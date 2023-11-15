import sys, os, logging, time
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path

class DisplayBuilder:

  def __init__(self,width,height,font):
    self.width = width
    self.height = height

    self.textsize = 24
    self.font = ImageFont.truetype(font, self.textsize, index=1)

    ascent, descent = self.font.getmetrics()
    self.textheight = self.font.getmask('Aj').getbbox()[3] + descent

    ImageDraw.ImageDraw.font = self.font

    self.image = Image.new('1', (self.height, self.width), 255)
    self.draw = ImageDraw.Draw(self.image)

  def get(self):
    self.draw.line((0,100,122,100), fill = 0)
    self.draw.line((61,100,61,149), fill = 0)
    self.draw.line((0,149,122,149), fill = 0)
    return self.image.rotate(180)

  def blank(self):
    self.draw.rectangle((0,0,self.height,self.width), fill = 1)

  def show(self):
    self.image.show()

  def text_in_spot(self,x,y,message):
    self.draw.text((x,y+1), message, fill = 0, anchor = 'lt')

    return(self.image)

  def image_in_spot(self,location,size,image):
    if isinstance(image, (str, Path)):
      try:
        im = Image.open(image)

      except (OSError, FileNotFoundError, PermissionError) as e:
        logging.error("Unable to open image %s, reason: %s" % (image,e))

    elif isinstance(image, Image.Image):
      im = image

    else:
      logging.error("No valid image supplied.")


    im.convert('1')
    im.thumbnail(size, resample=Image.BICUBIC)
    self.image.paste(im, location)
