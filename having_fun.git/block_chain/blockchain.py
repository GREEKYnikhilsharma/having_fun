import blockparam
import block
import time

class BlockChain():
  def __init__(self):
   self.blockchain_store = self.fetch_blockchain()
  
  def latest_block(self):
   return self.blockchain_store[-1]

  def generate_next_block(self,data):
   index = len(self.blockchain_store)
   previous_hash = self.latest_block().hash
   timestramp = int(time.time())
   params = blockparam.BlockParams(index, previous_hash, timestramp, data)
   new_block = block.Block(params)
   self.blockchain_store.append(new_block)

  def fetch_blockchain(self):
   return [block.Block.genesis_block()]

  def receive_new_block(self, new_block):
   previous_block = self.latest_block()
   if not new_block.has_valid_index(previous_block):
    print('index not valid')
    return
   if not new_block.has_valid_previous_hash(previous_block):
    print('previous hash is not valid')
   if not new_block.has_valid_hash():
    print('invalid hash')
    return
   self.blockchain_store.append(new_block)
