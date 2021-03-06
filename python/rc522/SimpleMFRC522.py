#z Code by Simon Monk https://github.com/simonmonk/

from . import MFRC522
import RPi.GPIO as GPIO
  
class SimpleMFRC522:

  READER = None
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  BLOCK_ADDRS = [i for i in range(4, 196)]
  READ_ADDRS = [i for i in range(4, 196, 4)]
  
  def __init__(self):
    self.READER = MFRC522()
    #print(self.BLOCK_ADDRS)
    print(len(self.READ_ADDRS))
  
  def read(self):
      id, text = self.read_no_block()
      while not id:
          id, text = self.read_no_block()
      return id, text

  def read_id(self):
      id = self.read_id_no_block()
      while not id:
          id = self.read_id_no_block()
      return id

  def read_id_no_block(self):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None
      return self.uid_to_num(uid)
  
  def read_no_block(self):
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    #status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
    data = []
    text_read = bytearray()
    if status == self.READER.MI_OK:
        for block_num in self.READ_ADDRS:
            block = self.READER.MFRC522_Read(block_num) 
            if block:
              #data += block
        #if data:
        #    for i in data:
                for i in block:
                    text_read.append(i)
    self.READER.MFRC522_StopCrypto1()
    return id, text_read
    
  def write(self, text):
      # fragment the text:
      # text is always 768 bytes long
      #print('raw text:')
      #print(text)
      newtext = bytearray()
      for i in range(int(len(text)/4)):
          newtext.extend(text[(i*4):(i+1)*4])
          for j in range(12):
              newtext.append(0x00)
      if len(text) % 4 > 0:
          newtext.append(text[int(len(text)/4)*4:])
      #print(newtext)
      id, text_in = self.write_no_block(newtext)
      while not id:
          id, text_in = self.write_no_block(newtext)
      return id, text_in

  def write_no_block(self, text):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      self.READER.MFRC522_SelectTag(uid)
      #status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
      self.READER.MFRC522_Read(11)
      if status == self.READER.MI_OK:
          data = bytearray()
          data.extend(bytearray(text.ljust(len(self.BLOCK_ADDRS)*16)))
          print(len(data))
          #print(data)
          i = 0
          for block_num in self.BLOCK_ADDRS:
            self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
            i += 1
      self.READER.MFRC522_StopCrypto1()
      return id, text[0:(len(self.BLOCK_ADDRS) * 16)]
      
  def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n
