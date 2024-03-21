"""
Python wrapper for Keithley Sourcemeters
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class KeithleySourceMeter(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'KEITHLEY INSTRUMENTS INC.':
            print('Device not recognized as a Keithley device.')
        self.visa = visa

        self.min_volt = None
        self.max_volt = None
        self.min_curr = None
        self.max_curr = None

    def get_source_mode(self):
        """
        Returns a string that represents the sourcemeter's output type, either voltage or current.

        Returns:
            mode : str
                Either 'volt' or 'curr'.
        """
        mode = self.visa.query_ascii_values(':source:func:mode?', converter='s')[0]
        mode = mode.rstrip('\n')
        return mode
    
    def set_source_mode(self, mode:str):
        """
        Sets the sourcemeter to output either voltage or current.

        Parameters:
            mode : str
                Either 'volt' or 'curr'.

        Raises:
            ValueError: <mode> is neither 'volt' nor 'curr'.
        """
        settings = ['volt', 'curr']
        if mode.lower() not in settings:
            raise ValueError(
                'Input parameter <mode> must be either "volt" or "curr".')
        self.visa.write(f':source:func:mode {mode}')
        
    def set_volt(self, volt:float):
        """
        Sets the sourcemeter output voltage in Volts.

        Parameters:
            volt : float
                Output voltage between -63 and 63 V.

        Raises:
            ValueError: <volt> is out of range.
        """
        if volt < self.min_volt or volt > self.max_volt:
            raise ValueError(
                f'Input parameter <volt> must be between {self.min_volt} and {self.max_volt}.')
        self.visa.write(f':source:volt {volt}')
        
    def set_curr(self, curr:float):
        """
        Sets the sourcemeter output current in Amperes.

        Parameters:
            curr : float
                Output current between -3.15 and 3.15 A.

        Raises:
            ValueError: <curr> is out of range.
        """
        if curr < self.min_curr or curr > self.max_curr:
            raise ValueError(
                f'Input parameter <curr> must be between {self.min_curr} and {self.max_curr}.')
        self.visa.write(f':source:curr {curr}')
    
    def get_clamp_limit(self):
        """
        Returns the compliance limit over which the output current/voltage cannot exceed. Limit will be a current limit if outputting voltage, or voltage limit if outputting current.
        
        Returns:
            limit : float
                Compliance limit. If the sourcemeter is set to outputting voltage, this will be a current limit. If set to outputting current, it will be a voltage limit.
        """
        mode = self.get_source_mode()
        if mode == 'VOLT':
            meas_type = 'curr'
        else:
            meas_type = 'volt'
        limit = self.visa.query_ascii_values(f':{meas_type}:prot:level?')[0]
        return limit
    
    def set_clamp_limit(self, limit:float):
        """
        Sets the output current limit if outputting voltage, or output voltage limit if outputting current. Input parameter <limit> may be set to be within the following ranges depending on measure type.

        Voltage range: -63 V to 63 V
        Current range: -3.15 A to 3.15 A

        Parameters:
            limit : float
                Compliance limit. If the sourcemeter is set to outputting voltage, this will be a current limit. If set to outputting current, it will be a voltage limit.

        Raises:
            ValueError: <limit> is out of range.
        """
        mode = self.get_source_mode()
        if mode == 'VOLT':
            meas_type = 'curr'
            if limit < self.min_curr and limit > self.max_curr:
                raise ValueError(
                    f'Outputting voltage, current compliance must be between {self.min_curr} and {self.max_curr} A.')
        else:
            meas_type = 'volt'
            if limit < self.min_volt and limit > self.max_volt:
                raise ValueError(
                    f'Outputting current, voltage compliance must be between {self.min_volt} and {self.max_volt} V.')
        self.visa.write(f':{meas_type}:prot {limit}')

    def reset_clamp(self):
        """
        Reverts the compliance limit to its default value.
        """
        mode = self.get_source_mode()
        if mode == 'VOLT':
            meas_type = 'curr'
        else:
            meas_type = 'volt'
        self.visa.write(f':{meas_type}:prot def')

    def is_output_on(self):
        """
        Returns True if the sourcemeter is outputting and False otherwise.
        """
        state = self.visa.query_ascii_values(':output?')[0]
        if state == 1:
            return True
        else:
            return False
    
    def output_on(self):
        self.visa.write(':output 1')

    def output_off(self):
        self.visa.write(':output 0')

    def meas_all(self):
        meas = self.visa.query_ascii_values(':read?')
        return meas
    
    def meas_volt(self):
        """
        Measures the voltage reading in Volts.

        Returns:
            volt : float
                Voltage reading in Volts.
        """
        volt = self.visa.query_ascii_values(':read?')[0]
        return volt
    
    def meas_curr(self):
        """
        Measures the current reading in Amperes.

        Returns:
            curr : float
                Current reading in Amperes.
        """
        curr = self.visa.query_ascii_values(':read?')[1]
        return curr
    
    def meas_res(self):
        """
        Measures the resistance in Ohms.

        Returns:
            res : float
                Resistance reading in Ohms.
        """
        res = self.visa.query_ascii_values(':read?')[2]
        return res
    
class Keithley2420(KeithleySourceMeter):
    def __init__(self, visa):
        super().__init__(visa)
        if self.idn[1] != 'MODEL 2420':
            print(f'{self.idn[0]} device not recognized as Model 2420.')
        self.visa = visa

        self.min_volt = -63
        self.max_volt = 63
        self.min_curr = -3.15
        self.max_curr = 3.15