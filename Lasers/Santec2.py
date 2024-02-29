"""
Python wrapper for Santec Lazers
Author(s): Howard Dao
"""

import pyvisa as visa

class TSL(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'SANTEC':
            print('Device not recognized as a Santec laser.')
        self.visa = visa

        self.min_wl = None
        self.max_wl = None
        self.min_spd = None
        self.max_spd = None
        self.max_del = None

        self.pow_unit = self.get_power_unit()
        self.min_pow_mW = None
        self.max_pow_mW = None
        self.min_pow_dBm = None
        self.max_pow_dBm = None

    def get_wavelength(self):
        """
        Returns the laser's output wavelength.
        """
        lam = self.visa.query_ascii_values(':wav?')[0]
        return lam
    
    def set_wavelength(self, lam:float):
        """
        Sets the laser's output wavelength.

        Parameters:
            lam : float
                Laser output wavelength.
        
        Raises:
            ValueError: <lam> is outside of range.
        """
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(
                f'Input parameter <lam> must be between {self.min_wl} to {self.max_wl}.')
        self.visa.write(f':wav {lam}')
        
    def get_wave_sweep_start(self):
        """
        Returns the start wavelength of the wavelength sweep.
        """
        lam = self.visa.query_ascii_values(':wav:swe:start?')[0]
        return lam
    
    def set_wave_sweep_start(self, lam:float):
        """
        Sets the start wavelength for wavelength sweep.

        Parameters:
            lam : float
                Laser sweep start wavelength.
        
        Raises:
            ValueError: <lam> is out of range.
        """
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(
                f'Input parameter <lam> must be between {self.min_wl} to {self.max_wl}.')
        self.visa.write(f':wav:swe:start {lam}')

    def get_wave_sweep_stop(self):
        """
        Returns the stop wavelength of the wavelength sweep.
        """
        lam = self.visa.query_ascii_values(':wav:swe:stop?')[0]
        return lam
    
    def set_wave_sweep_stop(self, lam:float):
        """
        Sets the stop wavelength for wavelength sweep.

        Parameters:
            lam : float
                Laser sweep stop wavelength.
        
        Raises:
            ValueError: <lam> is out of range.
        """
        if lam < self.min_wl or lam > self.max_wl:
            raise ValueError(
                f'Input parameter <lam> must be between {self.min_wl} to {self.max_wl}.')
        self.visa.write(f':wav:swe:stop {lam}')

    def get_wave_sweep_speed(self):
        """
        Returns the wavelength sweep speed in nm/s.
        """
        speed = self.visa.query_ascii_values(':wav:swe:spe?')[0]
        return speed
    
    def set_wave_sweep_speed(self, speed:float):
        """
        Sets the wavelength sweep speed.

        Parameters:
            speed : float
                Sweep speed.
        
        Raises:
            ValueError: <speed> is out of range.
        """
        if speed < self.min_spd or speed > self.max_spd:
            raise ValueError(
                f'Input parameter <speed> must be between {self.min_spd} to {self.max_spd}.')
        self.visa.write(f':wav:swe:spe {speed}')
        
    def start_sweep(self):
        """
        Starts a wavelength sweep.
        """
        self.visa.write(':wav:swe 1')
        
    def get_power_unit(self):
        unit = self.visa.query_ascii_values(':pow:unit?')[0]
        if unit == 0:
            return 'dBm'
        else:
            return 'mW'
        
    def set_power_unit(self, unit:str):
        if unit == 'dBm':
            unit_num = 0
        elif unit == 'mW':
            unit_num = 1
        else:
            raise ValueError(
                'Input parameter <unit> must be either "mW" or "dBm".')
        self.visa.write(f':pow:unit {unit_num}')
        self.pow_unit = unit
        
    def get_power(self):
        """
        Returns the laser output power.
        """
        pow = self.visa.query_ascii_values(':pow?')[0]
        return pow
    
    def set_power(self, pow:float):
        """
        Sets the laser output power.

        Parameters:
            pow : float
                Laser output power in either mW or dBm.
        
        Raises:
            ValueError: <pow> is outside of range.
        """
        if self.pow_unit == 'mW':
            if pow < self.min_pow_mW or pow > self.max_pow_mW:
                raise ValueError(
                    f'Input parameter <pow> must be between {self.min_pow_mW} and {self.max_pow_mW} mW.')
        else:
            if pow < self.min_pow_dBm or pow > self.max_pow_dBm:
                raise ValueError(
                    f'Input parameter <pow> must be between {self.min_pow_dBm} and {self.max_pow_dBm} dBm.')
        self.visa.write(f':pow {pow}')
        
    def output_off(self):
        self.visa.write(':pow:stat 0')

    def output_on(self):
        self.visa.write(':pow:stat 1')

class TSL710(TSL):
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

class TSL770(TSL):
    def __init__(self, visa):
        super().__init__(visa)
        if self.idn[1] != 'TSL-770':
            print(f'{self.idn[0]} laser not recognized as TSL-770')
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