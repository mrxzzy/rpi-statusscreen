import json
import time
import logging

class In():

  def __init__(self,path='/tmp/StatusOut.json'):
    self.path = path
    self.data = {}

  def get(self):
    try:
      with open(self.path, 'r') as f:
        self.data = json.load(f)
      return self.data
    except Exception as e:
      logging.error(e)
      return False

class Out():

  def __init__(self,path='/tmp/StatusOut.json'):
    self.path = path
    self.data = {}

  def send(self,data = None):
    logging.debug(data)
    if data is None:
      data = self.data

    data['last'] = time.time()

    with open(self.path, 'w') as f:
      json.dump(data, f)

    self.data = data
