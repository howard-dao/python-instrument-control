"""
Python wrapper for Keysight Optical Power Meters
Author(s): Howard Dao
"""

import pyvisa as visa

class N7744A(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'Keysight Technologies' and self.idn[1] != 'N7744A':
            print('Device not recognized as Keysight Keysight N7744A.')
        self.visa = visa

        self.min_wl = 1250e-9
        self.max_wl = 1650e-9
    
    def get_wavelength(self, ch:int):
        """
        Returns the wavelength of a specified channel.
        """
        if ch in range(1,5):
            lam = self.visa.query_ascii_values(f':sens{ch}:pow:wav?')[0]
            return lam
        else:
            return ValueError('Input parameter <ch> must be 1, 2, 3, or 4.')
    
    def set_wavelength(self, lam:float, ch:int):
        """
        Sets the wavelength of a specified channel.

        Parameters:
            lam : float
                Wavelength in meters.
            ch : int
                Channel number.

        Raises:
            ValueError: <ch> is neither 1, 2, 3, or 4.
        """
        if ch in range(1,5):
            if lam >= self.min_wl and lam <= self.max_wl:
                self.visa.write(f':sens{ch}:pow:wav {lam}')
            else:
                return ValueError(f'Input parameter <lam> must be between 
                                  {self.min_wl} and {self.max_wl}.')
        else:
            return ValueError('Input parameter <ch> must be 1, 2, 3, or 4.')
    
    def get_power_unit(self, verbose=True):
        """
        Returns the optical power unit. Unit will either be dBm or Watts.

        Parameters:
            verbose : bool, optional
                Whether to return the unit as an integer (False) or string (True).
        Returns:
            str : Optical power unit.
        """
        unit = self.visa.query_ascii_values(':sens:pow:unit?')[0]
        if verbose:
            if unit == 1:
                return 'W'
            else:
                return 'dBm'
        else:
            return unit
        
    def set_power_unit(self, unit:str):
        """
        Sets the optical power unit.

        Parameters:
            unit : str
                Either 'dBm' or 'W'.
        
        Raises:
            ValueError: <unit> is neither 'W' or 'dBm'.
        """
        if unit == 'dBm':
            unit = 0
        elif unit == 'W':
            unit = 1
        else:
            raise ValueError('Input paramter <unit> must be "dBm" or "W".')
        self.visa.write(':sens:pow:unit ', unit)
        
    def meas_power(self, ch:int):
        """
        Returns the measured optical power from a specified channel.

        Parameters:
            ch : int
                Channel number.

        Raises:
            ValueError: <ch> is neither 1, 2, 3, or 4.
        """
        if ch in range(1,5):
            power = self.visa.query_ascii_values(f':read{ch}:pow?')[0]
            return power
        else:
            raise ValueError('Input parameter <ch> must be 1, 2, 3, or 4.')