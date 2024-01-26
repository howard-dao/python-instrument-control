"""
Python wrapper for Keithley Sourcemeters
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class Keithley2420(visa.resources.GPIBInstrument):
    def __init__(self, visa=None):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'KEITHLEY INSTRUMENTS INC.' and self.idn[1] != 'MODEL 2420':
            print('Device not recognized as Keithley 2420.')
        self.visa = visa

    def get_source_mode(self):
        """
        Returns a string that represents the sourcemeter's output type, either voltage or current.

        Returns:
            mode
                type: string
                desc: 'volt' or 'curr'
        """
        mode = self.visa.query_ascii_values(':source:func:mode?', converter='s')[0]
        mode = mode.rstrip('\n')
        return mode
    
    def set_source_mode(self, mode:str):
        """
        Sets the sourcemeter to output either voltage or current.

        Parameters:
            mode
                type: string
                desc: either 'volt' or 'curr'

        Raises:
            AttributeError: <mode> is neither 'volt' nor 'curr'
        """
        settings = ['volt', 'curr']
        if mode.lower() in settings:
            self.visa.write(':source:func:mode ', mode)
        else:
            raise AttributeError('Input parameter <mode> must be either "volt" or "curr".')
        
    def set_volt(self, volt:float):
        """
        Sets the sourcemeter output voltage in Volts.

        Parameters:
            volt
                type: float
                desc: output voltage between -63 and 63 V

        Raises:
            AttributeError: <volt> is outside the acceptable range
        """
        if volt >= -63 and volt <= 63:
            self.visa.write(':source:volt ', str(volt))
        else:
            raise AttributeError('Input parameter <volt> must be between -63 and 63 (V).')
        
    def set_curr(self, curr:float):
        """
        Sets the sourcemeter output current in Amperes.

        Parameters:
            curr
                type: float
                desc: output current between -3.15 and 3.15 A

        Raises:
            AttributeError: <curr> is outside the acceptable range
        """
        if curr >= -3.15 and curr <= 3.15:
            self.visa.write(':source:volt ', str(curr))
        else:
            raise AttributeError('Input parameter <curr> must be between -3.15 and 3.15 (A).')
    
    def get_clamp_limit(self):
        """
        Returns the compliance limit over which the output current/voltage cannot exceed.
        Limit will be a current limit if outputting voltage, or voltage limit if outputting current.
        
        Returns:
            limit
                type: float
                desc: compliance limit
        """
        mode = self.get_source_mode()
        if mode == 'VOLT':
            meas_type = 'curr'
        else:
            meas_type = 'volt'
        limit = self.visa.query_ascii_values(':' + meas_type + ':prot:level?')[0]
        return limit
    
    def set_clamp_limit(self, limit):
        """
        Sets the output current limit if outputting voltage, or output voltage limit if outputting current.
        Input parameter <limit> may be set to be within the following ranges depending on measure type.

        Voltage range: -63 V to 63 V
        Current range: -3.15 A to 3.15 A

        Parameters:
            limit: float
            desc: sourcemeter compliance limit
        """
        mode = self.get_source_mode()
        match mode:
            case 'VOLT':
                meas_type = 'curr'
                if limit < -3.15 and limit > 3.15:
                    raise AttributeError('Outputting voltage, current compliance must be between -3.15 and 3.15 A')
            case 'CURR':
                meas_type = 'volt'
                if limit < -63 and limit > 63:
                    raise AttributeError('Outputting current, voltage compliance must be between -63 and 63 V.')
            case _:
                raise AttributeError('Input parameter <mode> was not found to be either "curr" or "volt"')
        self.visa.write(':' + meas_type + ':prot ', str(limit))

    def reset_clamp(self):
        """
        Reverts the compliance limit to its default value.
        """
        mode = self.get_source_mode()
        if mode == 'VOLT':
            meas_type = 'curr'
        else:
            meas_type = 'volt'
        self.visa.write(':' + meas_type + ':prot def')

    def is_output_on(self):
        """
        Returns whether the source is outputting or not.

        Returns:
            True if sourcemeter is outputting
            False otherwise
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
            volt
                type: float
                desc: voltage reading in Volts
        """
        volt = self.visa.query_ascii_values(':read?')[0]
        return volt
    
    def meas_curr(self):
        """
        Measures the current reading in Amperes.

        Returns:
            curr
                type: float
                desc: current reading in Amperes
        """
        curr = self.visa.query_ascii_values(':read?')[1]
        return curr
    
    def meas_res(self):
        """
        Measures the resistance in Ohms.

        Returns:
            res
                type: float
                desc: resistance reading in Ohms
        """
        res = self.visa.query_ascii_values(':read?')[2]
        return res