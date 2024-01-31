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
            print('Device not recognized as Santec TSL-710.')
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
                desc: laser output wavelength in nanometers
        
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
            raise AttributeError('Input parameter <lam> must be between 1480-1640.')

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
            raise AttributeError('Input parameter <lam> must be between 1480-1640.')
        
    def get_wave_sweep_speed(self):
        """
        Returns the wavelength sweep speed.

        Returns
            speed
                type: float
                desc: sweep speed in nm/sec
        """
        speed = self.visa.query_ascii_values(':wav:swe:spe?')[0]
        return speed
    
    def set_wave_sweep_speed(self, speed:float):
        """
        Sets the wavelength sweep speed.

        Parameters:
            speed
                type: float
                desc: sweep speed in nm/sec
        
        Raises:
            AttributeError: <speed> is outside the acceptable range
        """
        if speed >= 0.5 and speed <= 100:
            self.visa.write(':wav:swe:spe ', str(speed))
        else:
            raise AttributeError('Input parameter <speed> must be between 0.5-100.')
        
    def get_wave_sweep_delay(self):
        """
        Returns the wait time between wavelength sweeps.

        Returns:
            delay
                type: float
                desc: wait time in seconds
        """
        delay = self.visa.query_ascii_values(':wav:swe:del?')[0]
        return delay
    
    def set_wave_sweep_delay(self, delay:float):
        """
        Sets the wait time between wavelength sweeps.

        Parameters:
            delay
                type: float
                desc: wait time in seconds

        Raises:
            AttributeError: <delay> is outside of acceptable range
        """
        if delay >= 0 and delay <= 999.9:
            self.visa.write(':wav:swe:del ', str(delay))
        else:
            raise AttributeError('Input parameter <delay> must be between 0-999.9.')
        
    def get_wave_sweep_cycles(self):
        """
        Returns the number of wavelength sweep cycles.

        Returns:
            cycles
                type: int
                desc: number of sweep cycles
        """
        cycles = self.visa.query_ascii_values(':wav:swe:cycl?')[0]
        return cycles
    
    def set_wave_sweep_cycles(self, cycles:int):
        """
        Sets the number of wavelength sweep cycles.

        Parameters:
            cycles
                type: int
                desc: number of sweep cycles
        
        Raises:
            AttributeError: <cycles> is not an integer between 0-999.
        """
        if cycles in range(0, 1000):
            self.visa.write(':wav:swe:cycl ', str(cycles))
        else:
            raise AttributeError('Input parameter <cycles> must be an integer between 0-999.')
        
    def get_wave_sweep_mode(self):
        """
        Returns the wavelength sweeping mode.
        The output is an integer representing the following modes:
        0: Step operation, one-way
        1: Continuous operation, one-way
        2: Step operation, two-way
        3: Continuous operation, two-way

        Returns:
            mode
                type: int
                desc: 0, 1, 2, or 3
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
            mode
                type: int
                desc:
        
        Raises:
            AttributeError: 
        """
        if mode in range(0, 4):
            self.visa.write(':wav:swe:mod ', str(mode))
        else:
            raise AttributeError('Input parameter <mode> must be 0, 1, 2, or 3.')
        
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
            raise AttributeError('Input parameter <unit> must be either "mW" or "dBm".')
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

    def get_trig_out(self):
        """
        Returns the setting for trigger signal output timing.

        Returns:
            0 for no trigger
            1 for trigger at completion of a sweep
            2 for trigger at start of a sweep
            3 for trigger at each step in a sweep
        """
        trig = self.visa.query_ascii_values(':trig:outp?')[0]
        if trig == 0:
            return 'none'
        elif trig == 1:
            return 'stop'
        elif trig == 2:
            return 'start'
        elif trig == 3:
            return 'step'

    def set_trig_out(self, trig:str):
        """
        Sets the trigger signal output timing.

        Parameters:
            trig
                type: string
                desc: "none", "stop", "start", or "step"
        
        Raises:
            AttributeError: <trig> was not any of the above settings
        """
        settings = ['none', 'stop', 'start', 'step']
        if trig.lower() in settings:
            if trig == 'none':
                trig_num = 0
            elif trig == 'stop':
                trig_num = 1
            elif trig == 'start':
                trig_num = 2
            else:
                trig_num = 3
            self.visa.write(':trig:outp ', str(trig_num))
        else:
            raise AttributeError('Input parameter <trig> must be "none", "stop", "start", or "step".')

    def output_off(self):
        self.visa.write(':pow:stat 0')
    
    def output_on(self):
        self.visa.write(':pow:stat 1')