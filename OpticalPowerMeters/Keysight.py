"""
Python wrapper for Keysight Optical Power Meters
Author(s): Howard Dao
"""

import pyvisa as visa

class N7744A(visa.resources.GPIBInstrument):
    def __init__(self, visa=None):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'Keysight Technologies' and self.idn[1] != 'N7744A':
            print('Device not recognized as Keysight Keysight N7744A.')
        self.visa = visa

    def get_power(self):
        power = self.visa.query_ascii_values(':read1:pow?')[0]
        return power
    
    def get_wavelength(self):
        lam = self.visa.query_ascii_values(':sens:pow:wav?')[0]
        return lam
    
    def get_power_unit(self):
        unit = self.visa.query_ascii_values(':sens:pow:unit?')[0]
        return unit