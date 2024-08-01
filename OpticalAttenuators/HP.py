"""
Python wrapper for Hewlett-Packard Optical Attenuators
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class HPAttenuator(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'HEWLETT-PACKARD':
            print('Device not recognized as a Hewlett-Packard device.')
        self.visa = visa

        self.min_att = None
        self.max_att = None

        self.min_wl = None
        self.max_wl = None
    
    def get_attenuation(self):
        """
        Returns the attenuation.
        """
        return self.visa.query_ascii_values(':inp:att?')[0]
    
    def set_attenuation(self, att:float):
        """
        Sets the attenuation.

        Parameters:
            att : float
                Attenuation in dB.
        
        Raises:
            ValueError: <att> is out of range.
        """
        if att < self.min_att or att > self.max_att:
            raise ValueError(f'Input parameter <att> must be between {self.min_att} and {self.max_att}, given {att}.')
        self.visa.write(f':inp:att {att}')

    # def get_output_power(self):
    #     """
    #     Returns the through-power that is used to set the filter attenuation.
    #     """
    #     return self.visa.query_ascii_values(':outp:pow?')[0]
    
    # def set_output_power(self, power:float):
    #     """
    #     Sets the through-power that is used to set the filter attenuation.

    #     Parameters:
    #         power : float
    #             Through-power in dBm.
    #     """
    #     self.visa.write(f':outp:pow {power}')

    def get_wavelength(self):
        """
        Returns the wavelength.
        """
        return self.visa.query_ascii_values(':inp:wav?')[0]
    
    def set_wavelength(self, lam:float):
        """
        Sets the wavelength.

        Parameters:
            lam : float
                Wavelength in meters.
        
        Raises:
            ValueError: <lam> is out of range.
        """
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(f'Input parameter <lam> must be between {self.min_wl} and {self.max_wl}, given {lam}.')
        self.visa.write(f':inp:wav {lam}')

    def output_off(self):
        self.visa.write(':outp off')
    
    def output_on(self):
        self.visa.write(':outp on')

class HP8156A(HPAttenuator):
    def __init__(self, visa):
        super().__init__(visa)
        if self.idn[1] != 'HP8156A':
            print(f'{self.idn[0]} device not recognized as HP8156A.')
            self.visa = visa

        self.min_att = 0
        self.max_att = 60

        self.min_wl = 1200e-9
        self.max_wl = 1650e-9