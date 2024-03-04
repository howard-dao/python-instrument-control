"""
Python wrapper for Agilent Lightwave Measurement System Modules
Author(s): Howard Dao
"""

import pyvisa as visa

class AgilentMainframe(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'Agilent Technologies' or self.idn[1] != '8164B':
            print('Device not recognized as Keysight 8164B.')
        self.visa = visa

    def list_modules(self):
        """
        Prints whether the slots have modules and what those modules are.
        """
        for idx in range(0,5):
            is_empty = self.visa.query_ascii_values(f':slot{idx}:empt?')[0]
            if is_empty:
                print(f'Slot {idx} is empty.')
            else:
                module_id = self.visa.query(f':slot{idx}:idn?')
                module_id = module_id.split(',')
                print(f'Slot {idx} contains {module_id[0]} {module_id[1]}.')

    def get_trig_in(self):
        """
        Returns the input trigger response.
        """
        trig = self.visa.query_ascii_values(f':trig{self.slot}:inp?', converter='s')[0]
        trig = trig.rstrip('\n')
        return trig
    
    def set_trig_in(self, trig:str):
        """
        Sets the input trigger response.

        Parameters:
            trig : str
                IGN:    Ignore incoming trigger.
                SME:    Start a single measurement.
                CME:    Start a complete measurement.
                NEXT:   Perform next step of a stepped sweep.
                SWS:    Start a sweep cycle.
        """
        settings = ['ign', 'sme', 'cme', 'next', 'sws']
        if trig.lower() not in settings:
            raise ValueError(
                'Input parameter <trig> is not set to a correct string.')
        self.visa.write(f':trig{self.slot}:inp {trig}')

    def get_trig_out(self):
        """
        Returns the output trigger condition.
        """
        trig = self.visa.query_ascii_values(f':trig{self.slot}:outp?', converter='s')[0]
        trig = trig.rstrip('\n')
        return trig
    
    def set_trig_out(self, trig:str):
        """
        Sets the output trigger condition.

        Parameters:
            trig : str
                DIS:    Never.
                AVG:    When averaging time period finishes.
                MEAS:   When averaging time period begins.
                MOD:    For every leading edge of a digitally-modulated (TTL) signal.
                STF:    When a sweep step finishes.
                SWF:    When a sweep cycle finishes.
                SWST:   When a sweep cycle begins.
        """
        settings = ['dis', 'avg', 'meas', 'mod', 'stf', 'swf', 'swst']
        if trig.lower() not in settings:
            raise ValueError(
                'Input parameter <trig> is not one of the correct strings.')
        self.visa.write(f':trig{self.slot}:outp {trig}')

class AgilentLaser(AgilentMainframe):
    """
    Tunable laser
    """
    def __init__(self, visa, slot:int, wl_unit='m'):
        super().__init__(visa)
        self.visa = visa
        self.slot = slot
        self.wl_unit = wl_unit
        self.pow_unit = self.get_power_unit()

        self.min_wl = None
        self.max_wl = None

        self.min_pow_dBm = None
        self.max_pow_dBm = None
        self.min_pow_mW = None
        self.max_pow_mW = None

    def get_wavelength(self):
        """
        Returns the laser wavelength.
        """
        lam = self.visa.query_ascii_values(f':sour{self.slot}:wav?')[0]
        return lam
    
    def set_wavelength(self, lam:float):
        """
        Sets the laser wavelength.

        Parameters:
            lam : float
                Laser wavelength.
        """
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(
                f'Input parameter <lam> must be between {self.min_wl} and {self.max_wl}.')
        self.visa.write(f':sour{self.slot}:wav {lam}{self.wl_unit}')
        
    def get_power_unit(self):
        """
        Returns the laser's power unit.
        """
        unit = self.visa.query_ascii_values(f':sour{self.slot}:pow:unit?')[0]
        if unit == 0:
            return 'dBm'
        else:
            return 'W'
        
    def set_power_unit(self, unit:str):
        """
        Sets the laser's power unit.

        Parameters:
            unit : str
                Either 'dBm' or 'W'.
        """
        if unit != 'dBm' and unit != 'W':
            raise ValueError('Input parameter <unit> must be "dBm" or "W".')
        self.visa.write(f':sour{self.slot}:pow:unit {unit}')
        self.pow_unit = unit

    def get_power(self):
        """
        Returns the laser output power in Watts.
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

class Agilent81689A(AgilentLaser):
    """
    Tunable laser
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa, slot)
        self.module_id = visa.query(f':slot{slot}:idn?')
        self.module_id = self.module_id.split(',')
        if self.module_id[0] != 'HEWLETT-PACKARD' or self.module_id[1] != ' HP 81689A':
            print('Slot module not recognized as HP 81689A.')
        self.visa = visa
        self.slot = slot

        self.min_wl = 1465e-9
        self.max_wl = 1575e-9
        self.min_pow_dBm = -10
        self.max_pow_dBm = 13
        self.min_pow_mW = 100e-6
        self.max_pow_mW = 20e-3

class Agilent81600B(AgilentLaser):
    """
    Tunable laser
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa, slot)
        self.module_id = visa.query(f':slot{slot}:idn?')
        self.module_id = self.module_id.split(',')
        if self.module_id[0] != 'Agilent Technologies' or self.module_id[1] != '81600B':
            print('Slot module not recognized as Agilent 81600B.')
        self.visa = visa
        self.slot = slot

        self.min_wl = 1260e-9
        self.max_wl = 1640e-9
        self.min_pow_dBm = -10
        self.max_pow_dBm = 6
        self.min_pow_mW = 100e-6
        self.max_pow_mW = 5e-3

class Agilent81606A(AgilentLaser):
    """
    Tunable laser
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa, slot)
        self.module_id = visa.query(f':slot{slot}:idn?')
        self.module_id = self.module_id.split(',')
        if self.module_id[0] != 'HEWLETT-PACKARD' or self.module_id[1] != ' HP 81606A':
            print('Slot module not recognized as HP 81606A.')
        self.visa = visa
        self.slot = slot

        self.min_wl = 1450e-9
        self.max_wl = 1650e-9


class AgilentPowerMeter(AgilentMainframe):
    """
    Power sensor
    """
    def __init__(self, visa, slot:int, wl_unit='m'):
        super().__init__(visa)
        self.visa = visa
        self.slot = slot
        self.wl_unit = wl_unit
        self.pow_unit = self.get_power_unit()

        self.min_wl = None
        self.max_wl = None

    def get_wavelength(self):
        """
        Returns the laser wavelength in meters.
        """
        lam = self.visa.query_ascii_values(f':sens{self.slot}:pow:wav?')[0]
        return lam
    
    def set_wavelength(self, lam:float):
        """
        Sets the laser wavelength in the previously specified unit.

        Parameters:
            lam : float
                Laser wavelength.
        """
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(
                f'Input parameter <lam> must be between {self.min_wl} and {self.max_wl}.')
        self.visa.write(f':sens{self.slot}:pow:wav {lam}{self.wl_unit}')

    def get_power_unit(self):
        unit = self.visa.query_ascii_values(f'sens{self.slot}:pow:unit?')[0]
        if unit == 0:
            return 'dBm'
        else:
            return 'W'
        
    def set_power_unit(self, unit:str):
        if unit != 'dBm' and unit != 'W':
            raise ValueError('Input parameter <unit> must be "dBm" or "W".')
        self.visa.write(f':sens{self.slot}:pow:unit {unit}')
        self.pow_unit = unit

    def meas_pow(self):
        """
        Returns the input optical power in dBm.
        """
        self.visa.write(f':init{self.slot}')
        pow = self.visa.query_ascii_values(f':read{self.slot}:pow?')[0]
        return pow
    
class Agilent81634B(AgilentPowerMeter):
    """
    Power sensor
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa, slot)
        self.module_id = visa.query(f':slot{slot}:idn?')
        self.module_id = self.module_id.split(',')
        if self.module_id[0] != 'Agilent Technologies' or self.module_id[1] != '81634B':
            print('Slot module not recognized as Agilent 81634B.')
        self.visa = visa
        self.slot = slot

        self.min_wl = 800e-9
        self.max_wl = 1700e-9

class Agilent81636B(AgilentPowerMeter):
    """
    Power sensor
    """
    def __init__(self, visa, slot:int):
        super().__init__(visa, slot)
        self.module_id = visa.query(f':slot{slot}:idn?')
        self.module_id = self.module_id.split(',')
        if self.module_id[0] != 'Agilent Technologies' or self.module_id[1] != '81636B':
            print('Slot module not recognized as Agilent 81636B.')
        self.visa = visa
        self.slot = slot

        self.min_wl = 1250e-9
        self.max_wl = 1640e-9

# class Keysight81595B(Keysight8164B):
#     """
#     Switch
#     """
#     def __init__(self, visa, slot:int):
#         super().__init__(visa)
#         self.visa = visa
#         self.slot = slot