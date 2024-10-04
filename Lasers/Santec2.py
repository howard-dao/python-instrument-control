"""
Python wrapper for Santec Lazers
Author(s): Howard Dao
"""

import pyvisa as visa

class SantecLaser(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'SANTEC':
            print('Device not recognized as a Santec device.')
        self.visa = visa

        self.min_wl = None
        self.max_wl = None
        self.min_spd = None
        self.max_spd = None
        self.max_del = None

        self.min_pow_mW = None
        self.max_pow_mW = None
        self.min_pow_dBm = None
        self.max_pow_dBm = None

    @property
    def wavelength(self):
        return self.visa.query_ascii_values(':wav?')[0]
    @property.setter
    def wavelength(self, lam:float):
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(
                f'Input parameter <lam> must be between {self.min_wl} to {self.max_wl}. It was given {lam}.')
        self.visa.write(f':wav {lam}')
    
    @property
    def wave_sweep_start(self):
        return self.visa.query_ascii_values(':wav:swe:start?')[0]
    @property.setter
    def wave_sweep_start(self, lam:float):
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(
                f'Input parameter <lam> must be between {self.min_wl} to {self.max_wl}. It was given {lam}.')
        self.visa.write(f':wav:swe:start {lam}')

    @property
    def wave_sweep_stop(self):
        return self.visa.query_ascii_values(':wav:swe:stop?')[0]
    @property.setter
    def wave_sweep_stop(self, lam:float):
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(
                f'Input parameter <lam> must be between {self.min_wl} to {self.max_wl}. It was given {lam}.')
        self.visa.write(f':wav:swe:stop {lam}')

    @property
    def wave_sweep_speed(self):
        return self.visa.query_ascii_values(':wav:swe:spe?')[0]
    @property.setter
    def wave_sweep_speed(self, speed:float):
        if speed < self.min_spd or speed > self.max_spd:
            raise ValueError(
                f'Input parameter <speed> must be between {self.min_spd} to {self.max_spd}. It was given {speed}.')
        self.visa.write(f':wav:swe:spe {speed}')
    
    @property
    def power_unit(self):
        unit = self.visa.query_ascii_values(':pow:unit?')[0]
        if unit == 0:
            return 'dBm'
        else:
            return 'mW'
    @property.setter
    def power_unit(self, unit:str):
        if unit == 'dBm':
            unit_num = 0
        elif unit == 'mW':
            unit_num = 1
        else:
            raise ValueError(f'Input parameter <unit> must be either "mW" or "dBm". It was given "{unit}".')
        self.visa.write(f':pow:unit {unit_num}')
        self.pow_unit = unit

    @property
    def power(self):
        return self.visa.query_ascii_values(':pow?')[0]
    @property.setter
    def power(self, pow:float):
        if self.pow_unit == 'mW':
            if pow < self.min_pow_mW or pow > self.max_pow_mW:
                raise ValueError(
                    f'Input parameter <pow> must be between {self.min_pow_mW} and {self.max_pow_mW} mW. It was given {pow}.')
        else:
            if pow < self.min_pow_dBm or pow > self.max_pow_dBm:
                raise ValueError(
                    f'Input parameter <pow> must be between {self.min_pow_dBm} and {self.max_pow_dBm} dBm. It was given {pow}.')
        self.visa.write(f':pow {pow}')
        
    def output_off(self):
        self.visa.write(':pow:stat 0')

    def output_on(self):
        self.visa.write(':pow:stat 1')

    def start_sweep(self):
        """
        Starts a wavelength sweep.
        """
        self.visa.write(':wav:swe 1')

class TSL710(SantecLaser):
    def __init__(self, visa):
        super().__init__(visa)
        if self.idn[1] != 'TSL-710':
            print(f'{self.idn[0]} device not recognized as TSL-710.')
        self.visa = visa

        self.min_wl = 1480
        self.max_wl = 1640
        self.min_spd = 0.5
        self.max_spd = 100
        self.max_del = 999.9

        self.min_pow_mW = 0.01
        self.max_pow_mW = 10
        self.min_pow_dBm = -20
        self.max_pow_dBm = 10

class TSL770(SantecLaser):
    def __init__(self, visa):
        super().__init__(visa)
        if self.idn[1] != 'TSL-770':
            print(f'{self.idn[0]} device not recognized as TSL-770')
        self.visa = visa

        self.min_wl = 1480
        self.max_wl = 1640
        self.min_spd = 0.5
        self.max_spd = 200
        self.max_del = 999.9

        self.min_pow_mW = 0.2
        self.max_pow_mW = 19.953
        self.min_pow_dBm = -7
        self.max_pow_dBm = 13