"""
Python wrapper for Keysight Lightwave Measurement System Modules
Author(s): Howard Dao
"""

import pyvisa as visa

class Keysight8164B(visa.resources.GPIBInstrument):
    def __init__(self, visa, wl_unit='m', pow_unit='mW'):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'Keysight Technologies' and self.idn[1] != '8164B':
            print('Device not recognized as Keysight 8164B.')
        self.visa = visa

        self.wl_unit = wl_unit
        self.pow_unit = pow_unit

class Keysight81689A(Keysight8164B):
    """
    Tunable laser
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa)
        self.idn2 = visa.query(f':slot{slot}:idn?')
        self.idn2 = self.idn2.split(',')
        if self.idn2[0] != 'Keysight Technologies' and self.idn2[1] != '81689A':
            print('Slot module not recognized as Keysight 81689A.')
        self.visa = visa
        self.slot = slot

    def get_wavelength(self):
        """
        Returns the laser wavelength.
        """
        lam = self.visa.query_ascii_values(f':sour{self.slot}:wav?')[0]
        return lam
    
    def set_wavelength(self, lam:float):
        """
        Sets the laser wavelength in the previously specified unit.

        Parameters:
            lam : float
                Laser wavelength in meters.
        """
        self.visa.write(f':sour{self.slot}:wav {lam}{self.wl_unit}')

    def get_power(self):
        """
        Returns the laser output power.
        """
        pow = self.visa.query_ascii_values(f':sour{self.slot}:pow?')[0]
        return pow
    
    def set_power(self, pow:float):
        """
        Sets the laser output power in the previously specified unit.

        Parameters:
            pow : float
                Laser output power.
        """
        self.visa.write(f'sour{self.slot}:pow {pow}{self.pow_unit}')

    def output_off(self):
        self.visa.write(f':sour{self.slot}:pow:stat 0')

    def output_on(self):
        self.visa.write(f':sour{self.slot}:pow:stat 1')

class Keysight81634B(Keysight8164B):
    """
    Power sensor
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa)
        self.visa = visa
        self.slot = slot

    def meas_pow(self):
        pow = self.visa.query_ascii_values(f':read{self.slot}:pow?')[0]
        return pow

class Keysight81636B(Keysight8164B):
    """
    Power sensor
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa)
        self.visa = visa
        self.slot = slot

class Keysight81595B(Keysight8164B):
    """
    Switch
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa)
        self.visa = visa
        self.slot = slot