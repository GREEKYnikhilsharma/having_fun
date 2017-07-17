GENESIS_INDEX = 0
GENESIS_PREVIOUS_HASH = '0'
GENESIS_TIMESTRAMP = 119274
GENESIS_DATA = 'first block'

class BlockParams():
 def __init__(self, index, previous_hash, timestramp, data):
  self.index = index
  self.previous_hash = previous_hash
  self.timestramp = timestramp
  self.data = data

 def __str__(self):
  return str(self.index) + self.previous_hash + str(self.timestramp) + self.data

 @classmethod
 def genesis_params(cls):
  return cls(GENESIS_INDEX, GENESIS_PREVIOUS_HASH,GENESIS_TIMESTRAMP, GENESIS_DATA)
