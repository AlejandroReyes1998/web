# first python example. write to lea P and K memory

import spidev
import RPi.GPIO
import time

class lea_spi_wrapper:

    # addrs
    cmd_addr = 0x0
    inst_addrs = [0x1, 0x2, 0x3, 0x4, 0x5]
    lea_addrs = [0x6, 0x7, 0x8, 0x9]
    status_addr = 0xa

    # db cmds
    db_idle_cmd = 0x0
    db_lea_exec_cmd = 0x1
    db_write_lea_mem_cmd = 0x2
    
    # lea and data_bridge reset
    def __init__(self, rst_pin=24, spi_max_speed=1000000, spi_delay=16):
        self.spi_max_speed = spi_max_speed
        self.spi_t_delay = spi_delay
        self.gpio = RPi.GPIO
        self.gpio.setmode(self.gpio.BCM)
        self.rst = rst_pin
        self.gpio.setup(self.rst, self.gpio.OUT)
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)

    def __del__(self):
        self.spi.close()
        self.gpio.cleanup()
        
    def hard_reset(self):
        self.gpio.output(self.rst, self.gpio.HIGH)
        time.sleep(.001)
        self.gpio.output(self.rst, self.gpio.LOW)

    # execute a 2 byte spi transaction, read or write
    def exec_transaction(self, byte0, byte1):
        to_send = [byte0, byte1]
        #print(to_send)
        words = self.spi.xfer(to_send, self.spi_max_speed, self.spi_t_delay)
        #time.sleep(self.spi_t_delay/100000)
        return words

    # address is 4 bits (0 to 15), rw is 1 bit (1 or 0)
    def format_addr_byte(self, addr, rw):
        return (rw << 7) | (addr << 3)

    def read_reg(self, addr):
        formatted_addr_byte = self.format_addr_byte(addr, 0)
        read_val = self.exec_transaction(formatted_addr_byte, 0x00)[1]
        return read_val
    
    def write_reg(self, addr, data):
        formatted_addr_byte = self.format_addr_byte(addr, 1)
        self.exec_transaction(formatted_addr_byte, data)

    # hex string test methods below:
    
    # write lea instruction. instruction is 40 bits long.
    # internally the first 2 bits are ignored.
    # receives a hex string
    def write_inst_regs(self, inst_string):
        #print('writing inst %s' % (inst_string))
        inst = []
        for i in range(5):
            inst.append(inst_string[(2*i):(2*i)+2])
        for i in range(5):
            self.write_reg(self.inst_addrs[i], int(inst[i], 16))

    def gen_inst_vect(self, opc, rw, addr, data_word):
        inst_vect = '00'
        inst_vect += opc
        inst_vect += rw
        inst_vect += addr
        new_inst_vect = hex(int(inst_vect, 2))[2:].zfill(2)
        new_inst_vect += data_word
        return new_inst_vect

    def split_word(self, w):
        ret_arr = []
        for i in range(4):
            ret_arr.append(w[(i*8):(i*8)+8])
        return ret_arr

    def exec_lea_write(self, opc_string, w_list):
        for i in range(4):
            self.write_inst_regs(self.gen_inst_vect(opc_string, '1', bin(int(3-i))[2:].zfill(2), w_list[i]))
            self.write_reg(self.cmd_addr, self.db_lea_exec_cmd)
            while (self.perform_sanity_check() == 1):
                pass
            #print('lea status %d' % (self.read_reg(self.status_addr)))

    # read the lea registers
    def read_lea_out_regs(self):
        lea_out_val = []
        for i in range(4):
            lea_out_val.append(self.read_reg(self.lea_addrs[i]))
        return lea_out_val

    def exec_lea_read(self, opc_string):
        out = []
        for i in range(4):
            self.write_inst_regs(self.gen_inst_vect(opc_string, '0', bin(int(3-i))[2:].zfill(2), '00000000'))
            self.write_reg(self.cmd_addr, self.db_lea_exec_cmd)
            while (self.perform_sanity_check() == 1):
                pass
            self.write_reg(self.cmd_addr, self.db_write_lea_mem_cmd)
            out.append(self.read_lea_out_regs())
        return out

    # end hex string test methods
    
    def perform_sanity_check(self, timeout_val = 7):
        status = self.read_reg(self.status_addr)
        breaker = 0
        timeout_count = 0
        while breaker == 0:
            #print('STATUS %d' %(self.read_reg(self.status_addr)))
            if self.read_reg(self.status_addr) == 0:
                breaker = 1
            elif self.read_reg(self.status_addr) > 1:
                return 1
            elif self.read_reg(self.status_addr) == 1:
                if timeout_count < timeout_val:
                    time.sleep(1/1000000)
                    timeout_count += 1
                else:
                    return 1
        return 0

    def db_write_inst_regs(self, inst_string):
        inst = []
        for i in range(5):
            inst.append(inst_string[(2*i):(2*i)+2])
        for i in range(5):
            self.write_reg(self.inst_addrs[i], int(inst[i], 16))
    # todo bytearray primitives
    # todo lea_encrypt with bytearray
    # todo lea_decrypt with bytearray
    # todo lea_write with bytearray

    def format_lea_inst_header(self, opc, rw, addr):
        return (0x00 | (opc << 3) | (rw << 2) | addr)
    
    def lea_write(self, opc, bytearr):
        for i in range(4):
            self.write_reg(self.inst_addrs[0], self.format_lea_inst_header(opc, 1, 3-i))
            for j in range(4):
                self.write_reg(self.inst_addrs[j+1], bytearr[4*i+j])
            self.write_reg(self.cmd_addr, self.db_lea_exec_cmd)
        
        
    def lea_read(self, opc):
        outl = []
        for i in range(4):
            # issue the read command
            self.write_reg(self.inst_addrs[0], self.format_lea_inst_header(opc, 0, 3-i))
            self.write_reg(self.cmd_addr, self.db_lea_exec_cmd)
            self.write_reg(self.cmd_addr, self.db_write_lea_mem_cmd)
            # read the db registers
            for i in range(4):
                # append the output
                outl.append(self.read_reg(self.lea_addrs[i]))
        return bytearray(outl)
            

    def lea_enc(self):
        self.write_reg(self.inst_addrs[0], self.format_lea_inst_header(0x3, 0, 0))
        self.write_reg(self.cmd_addr, self.db_lea_exec_cmd)

    def lea_dec(self):
        self.write_reg(self.inst_addrs[0], self.format_lea_inst_header(0x4, 0, 0))
        self.write_reg(self.cmd_addr, self.db_lea_exec_cmd)

    # receives a bytearray, returns a bytearray
    def format_bytes(self, bytearr):
        newbytes = bytearray()
        for i in range(4):
            for j in range(3, -1 , -1):
                newbytes.append(bytearr[(4*i)+j])
            
        return newbytes

    def lea_decrypt(self, k, c):
        self.hard_reset()
        self.lea_write(0x0, self.format_bytes(k))
        self.lea_write(0x2, self.format_bytes(c))
        self.lea_dec()
        return self.format_bytes(self.lea_read(0x1))

    def lea_encrypt(self, k, p):
        self.hard_reset()
        self.lea_write(0x0, self.format_bytes(k))
        self.lea_write(0x1, self.format_bytes(p))
        self.lea_enc()
        return self.format_bytes(self.lea_read(0x2))

    #receives bytearray
    def fragment_text(self, t):
        end_tb = []
        print('pt len %d' % (len(t)))
        newt  = bytearray(t.ljust(768))
        print(len(t))
        for i in range (int(len(newt)/16)):
            end_tb.append(newt[(i*16):(i*16)+16])
        return end_tb
    
    # p_arr is a list of bytearrays
    # iv is the initialization vector in a byte array
    # k is the kay in a bytearray
    def cbc_lea_encrypt(self, p_arr, k, iv):
        xor_res = bytearray()
        c  = []
        c.append(iv)
        for i in range(len(p_arr)):
            xor_res = bytearray()
            for j in range(16):
                xor_res.append(p_arr[i][j]^c[i][j])
            #for val in (p_arr[i]):
            #    print(hex(val)[2:].zfill(2), end='')
            #print()
            #for val in (c[i]):
            #    print(hex(val)[2:].zfill(2), end='')
            #print()
            #print(xor_res)
            c.append(self.lea_encrypt(k, xor_res))
        return c[1:]
    # todo cbc_lea_decrypt(self, c, k, iv)
    def cbc_lea_decrypt(self, c_arr, k, iv):
        xor_res = bytearray()
        auxval = bytearray()
        p  = []
        c_arr.insert(0, iv)
        for i in range(len(c_arr)-1):
            xor_res = bytearray()
            auxval = self.lea_decrypt(k, c_arr[i+1])
            for j in range(16):
                xor_res.append(auxval[j]^c_arr[i][j])
            #print(xor_res)
            p.append(xor_res)
        return p
    
