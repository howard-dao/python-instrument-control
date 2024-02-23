"""
Python wrapper for Santec Lazers
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class TSL710(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'Santec' and self.idn[1] != 'TSL-710':
            print('Device not recognized as Santec TSL-710.')
        self.visa = visa

        self.min_wl = 1480
        self.max_wl = 1640
        self.min_spd = 0.5
        self.max_spd = 100
        self.min_del = 0
        self.max_del = 999.9
        self.min_pow_mW = 0.1
        self.max_pow_mW = 10
        self.min_pow_dBm = -20
        self.max_pow_dBm = 10

    def get_wavelength(self):
        """
        Returns the laser's output wavelength in nanometers.

        Returns:
            lam : float
                Laser output wavelength in nanometers.
        """
        lam = self.visa.query_ascii_values(':wav?')[0]
        return lam
    
    def set_wavelength(self, lam:float):
        """
        Sets the laser's output wavelength in nanometers.

        Parameters:
            lam : float
                Laser output wavelength in nanometers.
        
        Raises:
            ValueError: <lam> is out of range.
        """
        if lam >= self.min_wl and lam <= self.max_wl:
            self.visa.write(f':wav {lam}')
        else:
            raise ValueError(f'Input parameter <lam> must be between 
                             {self.min_wl} and {self.max_wl}.')
        
    def get_wav_sweep_start(self):
        """
        Returns the start wavelength of the wavelength sweep, in nanometers.

        Returns:
            lam : float
                Start wavelength of laser sweep in nanometers.
        """
        lam = self.visa.query_ascii_values(':wav:swe:start?')[0]
        return lam
    
    def set_wav_sweep_start(self, lam:float):
        """
        Sets the start wavelength for wavelength sweep, in nanometers.

        Parameters:
            lam : float
                Start wavelength of laser sweep in nanometers.
        
        Raises:
            ValueError: <lam> is out of range.
        """
        if lam >= self.min_wl and lam <= self.max_wl:
            self.visa.write(f':wav:swe:start {lam}')
        else:
            raise ValueError(f'Input parameter <lam> must be between 
                             {self.min_wl} and {self.max_wl}.')

    def get_wav_sweep_stop(self):
        """
        Returns the stop wavelength of the wavelength sweep, in nanometers.

        Returns:
            lam : float
                Stop wavelength of laser sweep in nanometers.
        """
        lam = self.visa.query_ascii_values(':wav:swe:stop?')[0]
        return lam
    
    def set_wav_sweep_stop(self, lam:float):
        """
        Sets the stop wavelength for wavelength sweep, in nanometers.

        Parameters:
            lam : float
                Stop wavelength of laser sweep in nanometers.
        
        Raises:
            ValueError: <lam> is out of range.
        """
        if lam >= self.min_wl and lam <= self.max_wl:
            self.visa.write(f':wav:swe:stop {lam}')
        else:
            raise ValueError(f'Input parameter <lam> must be between 
                             {self.min_wl} and {self.max_wl}.')
        
    def get_wave_sweep_speed(self):
        """
        Returns the wavelength sweep speed in nm/s.

        Returns
            speed : float
                Sweep speed in nm/sec.
        """
        speed = self.visa.query_ascii_values(':wav:swe:spe?')[0]
        return speed
    
    def set_wave_sweep_speed(self, speed:float):
        """
        Sets the wavelength sweep speed in nm/s.

        Parameters:
            speed : float
                Sweep speed in nm/sec.
        
        Raises:
            ValueError: <speed> is out of range.
        """
        if speed >= self.min_spd and speed <= self.max_spd:
            self.visa.write(f':wav:swe:spe {speed}')
        else:
            raise ValueError(f'Input parameter <speed> must be between 
                             {self.min_spd} and {self.max_spd}.')
        
    def get_wave_sweep_delay(self):
        """
        Returns the wait time between wavelength sweeps.

        Returns:
            delay : float
                Wait time in seconds.
        """
        delay = self.visa.query_ascii_values(':wav:swe:del?')[0]
        return delay
    
    def set_wave_sweep_delay(self, delay:float):
        """
        Sets the wait time between wavelength sweeps.

        Parameters:
            delay : float
                Wait time in seconds.

        Raises:
            ValueError: <delay> is out of range.
        """
        if delay >= self.min_del and delay <= self.max_del:
            self.visa.write(f':wav:swe:del {delay}')
        else:
            raise ValueError(f'Input parameter <delay> must be between 
                             {self.min_del} and {self.max_del}.')
        
    def get_wave_sweep_cycles(self):
        """
        Returns the number of wavelength sweep cycles.

        Returns:
            cycles : int
                Number of sweep cycles.
        """
        cycles = self.visa.query_ascii_values(':wav:swe:cycl?')[0]
        return cycles
    
    def set_wave_sweep_cycles(self, cycles:int):
        """
        Sets the number of wavelength sweep cycles.

        Parameters:
            cycles : int
                Number of sweep cycles.
        
        Raises:
            ValueError: <cycles> is not an integer between 0-999.
        """
        if cycles in range(0, 1000):
            self.visa.write(f':wav:swe:cycl {cycles}')
        else:
            raise ValueError('Input parameter <cycles> must be an integer between 0 to 999.')
        
    def get_wave_sweep_mode(self):
        """
        Returns the wavelength sweeping mode.
        The output is an integer representing the following modes:
        0: Step operation, one-way
        1: Continuous operation, one-way
        2: Step operation, two-way
        3: Continuous operation, two-way

        Returns:
            mode : int
                Sweeping mode number.
        """
        mode = self.visa.query_ascii_values(':wav:swe:mod?')[0]
        return mode
    
    def set_wave_sweep_mode(self, mode:int):
        """
        Sets the wavelength sweeping mode.
        The input must be an integer representing the following modes:
        0: Step operation, one-way
        1: Continuous operation, one-way
        2: Step operation, two-way
        3: Continuous operation, two-way

        Parameters:
            mode : int
                Sweeping mode number.
        
        Raises:
            ValueError: <mode> is neither 0, 1, 2, nor 3.
        """
        if mode in range(0, 4):
            self.visa.write(f':wav:swe:mod {mode}')
        else:
            raise ValueError('Input parameter <mode> must be 0, 1, 2, or 3.')
        
    def get_power_unit(self, verbose=True):
        """
        Return the unit for output laser power.

        Parameters:
            verbose : bool, optional
                Whether to return <unit> as an integer (False) or string (True).

        Returns:
            unit : int or str
                Either 'dBm' or 'mW'.
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
            unit : str
            Either 'dBm' or 'mW'.
        
        Raises:
            ValueError: <unit> is neither 'mW' nor 'dBm'.
        """
        if unit == 'dBm':
            unit = 0
        elif unit == 'mW':
            unit = 1
        else:
            raise ValueError('Input parameter <unit> must be either "mW" or "dBm".')
        self.visa.write(f':pow:unit {unit}')
        
    def get_power(self, unit='mW'):
        """
        Returns the laser output power setting.

        Parameters:
            unit : str, optional
                Either 'dBm' or 'mW' ('mW' by default).

        Returns:
            pow : float
                Optical output power level.
        """
        self.set_power_unit(unit=unit)
        pow = self.visa.query_ascii_values(':pow?')[0]
        return pow
    
    def set_power(self, pow:float, unit='mW'):
        """
        Sets the laser output power. By default, it sets the power in mW,
        but can be set in dBm with the <unit> parameter.

        Parameters:
            pow : float
                Optical output power level.
            unit : str, optional
                Either 'dBm' or 'mW' ('mW' by default).
        """
        self.set_power_unit(unit=unit)
        if unit == 'mW':
            if pow >= self.min_pow_mW and pow <= self.max_pow_mW:
                pass
            else:
                raise ValueError(f'Input parameter <pow> must be between 
                                 {self.min_pow_mW} and {self.max_pow_mW} mW.')
        elif unit == 'dBm':
            if pow >= self.min_pow_dBm and pow <= self.max_pow_dBm:
                pass
            else:
                raise ValueError(f'Input parameter <pow> must be between 
                                 {self.min_pow_dBm} and {self.max_pow_dBm} dBm.')
        else:
            raise ValueError('Input parameter <unit> must be "mW" or "dBm".')
        self.visa.write(f':pow {pow}')

    def get_trig_out(self):
        """
        Returns the setting for trigger signal output timing.

        Returns:
            'none' for no trigger
            'stop' for trigger at completion of a sweep
            'start' for trigger at start of a sweep
            'step' for trigger at each step in a sweep
        """
        settings = {0:'none', 1:'stop', 2:'start', 3:'step'}
        trig = self.visa.query_ascii_values(':trig:outp?')[0]
        return settings[trig]

    def set_trig_out(self, trig:str):
        """
        Sets the trigger signal output timing.

        Parameters:
            trig : str
                Either "none", "stop", "start", or "step".
        
        Raises:
            ValueError: <trig> was not any of the above settings.
        """
        settings = {'none':0, 'stop':1, 'start':2, 'step':3}
        if trig.lower() in settings.keys():
            trig_num = settings[trig.lower()]
            self.visa.write(f':trig:outp {trig_num}')
        else:
            raise ValueError('Input parameter <trig> must be "none", "stop", "start", or "step".')

    def output_off(self):
        self.visa.write(':pow:stat 0')
    
    def output_on(self):
        self.visa.write(':pow:stat 1')