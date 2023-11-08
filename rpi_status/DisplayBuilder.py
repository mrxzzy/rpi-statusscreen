import sys, os, logging, time
from PIL import Image,ImageDraw,ImageFont

class DisplayBuilder:

  def __init__(self,width,height,font,symbol):
    self.width = width
    self.height = height

    self.font = ImageFont.truetype(font, 24)
    self.symbols = ImageFont.truetype(symbol, 24)

    ascent, descent = self.font.getmetrics()
    self.textheight = self.font.getmask('Aj').getbbox()[3] + descent

    ImageDraw.ImageDraw.font = self.font

    self.image = Image.new('1', (self.height, self.width), 255)
    self.draw = ImageDraw.Draw(self.image)

  def show(self):
    self.image.show()

  def text_in_spot(self,x,y,width,height,message):
    self.draw.rectangle((x,y,x + width, y + height), fill = 0)
    self.draw.text((x,y+1), message, fill = 255, anchor = 'lt')

    return(self.image)

  def symbol_in_spot(self,x,y,width,height,char):
    self.draw.rectangle((x,y,x + width, y + height), fill = 0)
    self.draw.text((x,y+1), char, fill = 255, font = self.symbols, anchor = 'lt')

    return(self.image)

