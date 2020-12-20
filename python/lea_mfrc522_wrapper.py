import lea_spi_wrapper as lsw
import RPi.GPIO as GPIO
from rc522.SimpleMFRC522 import SimpleMFRC522

class lea_mfrc522_wrapper:

    def __init__(self):
        self.spi_wrapper = lsw.lea_spi_wrapper()
        self.ntag_rw = SimpleMFRC522()

    def __del__(self):
        del self.ntag_rw
        del self.spi_wrapper
        #GPIO.cleanup()

    # k and iv are 16 byte long bytearrays
    def read_tag(self, k, iv):
        print("place a tag near reader")
        (id, text) = self.ntag_rw.read()
        #print("text: %s" % (text))
        pb = self.spi_wrapper.cbc_lea_decrypt(self.spi_wrapper.fragment_text(text), k, iv)
        #print(pb)
        p = bytearray()
        for arr in pb:
            p.extend(arr)
        #print('raw pt:')
        #print(p)
        return p

    # p is a <=768 byte long string
    def write_tag(self, p, k, iv):
        print(p)
        cstring = bytearray()
        pt = bytearray(p, 'utf-8')
        pl = 768 - len(pt)
        if pl > 0:
            for i in range(pl):
                pt.append(0x00)
        c = self.spi_wrapper.cbc_lea_encrypt(self.spi_wrapper.fragment_text(pt), k, iv)
        #print(c)
        for arr in c:
            cstring.extend(arr)
        print('ciphertext:')
        #print(cstring)
        print("place tag to write")
        self.ntag_rw.write(cstring)
        print("Written")
