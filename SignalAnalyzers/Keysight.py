"""
Python wrapper for Keysight Signal Analyzers
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class KeysightSA(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'Agilent Technologies':
            print('Device not recognized as a Keysight device.')
        self.visa = visa

        self.min_freq = None
        self.max_freq = None

    def get_center_freq(self):
        freq = self.visa.query_ascii_values(':freq:cent?')[0]
        return freq
    
    def set_center_freq(self, freq:float):
        self.visa.write(f':freq:cent {freq}Hz')

    def get_freq_span(self):
        span = self.visa.query_ascii_values(':freq:span?')[0]
        return span
    
    def set_freq_span(self, span:float):
        self.visa.write(f':freq:span {span}Hz')

    def get_freq_start(self):
        freq = self.visa.query_ascii_values(':freq:start?')[0]
        return freq
    
    def set_freq_start(self, freq:float):
        self.visa.write(f':freq:start {freq}Hz')
    
    def get_freq_stop(self):
        freq = self.visa.query_ascii_values(':freq:stop?')[0]
        return freq
    
    def set_freq_stop(self, freq:float):
        freq = self.visa.write(f':freq:stop {freq}Hz')

    def get_trace(self):
        self.visa.write(':form:data real,32')

        byte_order = self.visa.query_ascii_values(':form:bord?', converter='s')[0].rstrip()
        if byte_order == 'NORM':
            self.visa.write(':form:bord swap')

        trace = self.visa.query_binary_values(':trace:data? trace1', datatype='f', is_big_endian=False)

        trace_arr = np.asarray(trace)

        return trace_arr


class N9010A(KeysightSA):
    def __init__(self, visa):
        super().__init__(visa)
        if self.idn[1] != 'N9010A':
            print(f'{self.idn[0]} device not recognized as N9010A.')
        self.visa = visa

        self.min_freq = 10
        self.max_freq = 44e9