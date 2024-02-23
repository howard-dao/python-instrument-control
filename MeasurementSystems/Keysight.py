"""
Python wrapper for Keysight Lightwave Measurement System Modules
Author(s): Howard Dao
"""

import pyvisa as visa

class KeysightLightwave(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = None
        self.visa = None

class Keysight81689A(KeysightLightwave):
    """
    Tunable laser
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa)
        self.idn = visa.query('*IDN?')
        self.visa = visa
        self.slot = slot

    def set_power(self, pow:float, unit='mW'):
        self.visa.write(f'sour{self.slot}:pow {pow}{unit}')

class Keysight81636B(KeysightLightwave):
    """
    Power sensor
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa)
        self.visa = visa
        self.slot = slot

class Keysight81634B(KeysightLightwave):
    """
    Power sensor
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa)
        self.visa = visa
        self.slot = slot

class Keysight81595B(KeysightLightwave):
    """
    Switch
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa)
        self.visa = visa
        self.slot = slot