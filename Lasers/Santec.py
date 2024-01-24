"""
Python wrapper for Santec Lazers
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class TSL710(visa.resources.GPIBInstrument):
    def __init__(self, visa=None):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'Santec' and self.idn[1] != 'TSL-710':
            print('Device not recognized as Santec TSL-710')
        self.visa = visa

    def get_wavelength(self):
        """
        Returns the laser's output wavelength.

        Returns:
            lam
                type: float
                desc: laser output wavelength in nanometers
        """
        lam = self.visa.query_ascii_values(':wav?')[0]
        return lam
    
    def set_wavelength(self, lam:float):
        """
        Sets the laser's output wavelength.

        Parameters:
            lam
                type: float
                desc: laser output wavelength in meters
        
        Raises:
            AttributeError: <lam> is outside the acceptable range
        """
        if lam >= 1480 and lam <= 1640:
            self.visa.write(':wav ', str(lam))
        else:
            raise AttributeError('Input parameter <lam> must be between 1480-1640.')
        
    def get_wav_sweep_start(self):
        """
        Returns the start wavelength of the wavelength sweep.

        Returns:
            lam
                type: float
                desc: start wavelength of laser sweep in nanometers
        """
        lam = self.visa.query_ascii_values(':wav:swe:start?')[0]
        return lam
    
    def set_wav_sweep_start(self, lam:float):
        """
        Sets the start wavelength for wavelength sweep.

        Parameters:
            lam
                type: float
                desc: start wavelength of laser sweep in nanometers
        
        Raises:
            AttributeError: <lam> is outside the acceptable range
        """
        if lam >= 1480 and lam <= 1640:
            lam = str(lam)
            self.visa.write(':wav:swe:start ', lam)
        else:
            raise AttributeError('Wavelength must be between 1250-1650 nm')

    def get_wav_sweep_stop(self):
        """
        Returns:
            lam
                type: float
                desc: stop wavelength of laser sweep in nanometers
        """
        lam = self.visa.query_ascii_values(':wav:swe:stop?')[0]
        return lam
    
    def set_wav_sweep_stop(self, lam:float):
        """
        Sets the stop wavelength for wavelength sweep.

        Parameters:
            lam
                type: float
                desc: stop wavelength of laser sweep in nanometers
        
        Raises:
            AttributeError: <lam> is outside the acceptable range
        """
        if lam >= 1480 and lam <= 1640:
            lam = str(lam)
            self.visa.write(':wav:swe:stop ', lam)
        else:
            raise AttributeError('Wavelength must be between 1250-1650 nm')
        
    def get_power_unit(self, verbose=True):
        """
        Return the unit for output laser power.

        Parameters:
            verbose
                type: Boolean
                desc: whether to return <unit> as an integer (False) or string (True)

        Returns:
            unit
                type: int or string
                desc: either 'dBm' or 'mW'
        """
        unit = self.visa.query_ascii_values(':pow:unit?')[0]
        if verbose:
            if unit == 0:
                return 'dBm'
            else:
                return 'mW'
        else:
            return unit
    
    def set_power_unit(self, unit:str):
        """
        Sets the unit for output laser power.

        Parameters:
            unit: string
            desc: either 'dBm' or 'mW'
        
        Raises:
            AttributeError: <unit> is neither 'mW' nor 'dBm'
        """
        if unit == 'dBm':
            unit = 0
        elif unit == 'mW':
            unit = 1
        else:
            raise AttributeError('Unit should be either "mW" or "dBm"')
        self.visa.write(':pow:unit ', str(unit))
        
    def get_power(self, unit='mW'):
        """
        Returns the laser output power setting.

        Parameters:
            unit
                type: string
                desc: either 'dBm' or 'mW' ('mW' by default)

        Returns:
            pow
                type: float
                desc: optical output power level
        """
        self.set_power_unit(unit=unit)
        pow = self.visa.query_ascii_values(':pow?')[0]
        return pow
    
    def set_power(self, pow:float, unit='mW'):
        """
        Sets the laser output power. By default, it sets the power in mW, but can be set in dBm with the <unit> parameter.

        Parameters:
            pow
                type: float
                desc: optical output power level
            unit
                type: string
                desc: either 'dBm' or 'mW' ('mW' by default)
        """
        self.set_power_unit(unit=unit)
        self.visa.write(':pow ', str(pow))

    def output_off(self):
        self.visa.write(':pow:stat 0')
    
    def output_on(self):
        self.visa.write(':pow:stat 1')