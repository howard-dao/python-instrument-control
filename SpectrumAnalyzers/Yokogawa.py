"""
Python wrapper for Yokogawa Optical Spectrum Analyzers
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class AQ6370D(visa.resources.gpib.GPIBInstrument):
    def __init__(self, visa=None):

        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'YOKOGAWA' or self.idn[1] != 'AQ6370D':
            print('Device not recognized as Yokogawa AQ6370D')

        self.visa = visa

    def get_wave_center(self):
        """
        Returns:
            lam
                type: float
                desc: center wavelength in meters
        """
        lam = self.visa.query_ascii_values(':sens:wav:cent?')[0]
        return lam
    
    def set_wave_center(self, lam=float):
        """
        Sets the center wavelength
        
        Parameters:
            lam
                type: float
                desc: center wavelength in meters

        Raises:
            AttributeError: <lam> is outside the acceptable range
        """
        if lam >= 600e-9 and lam <= 1700e-9:
            lam = str(lam)
            self.visa.write(':sens:wav:cent ', lam)
        else:
            raise AttributeError('Wavelength must be between 600-1700 nm')
    
    def get_wave_span(self):
        """
        Returns:
            span
                type: float
                desc: wavelength span in meters
        """
        span = self.visa.query_ascii_values(':sens:wav:span?')[0]
        return span
    
    def set_wave_span(self, span=float):
        """
        Sets the wavelength span of a sweep

        Parameters:
            span
                type: float
                desc: wavelength span in meters
        
        Raises:
            AttributeError: <span> is out of the accepted range
        """
        if span >= 0.1e-9 and span <= 1100e-9:
            span = str(span)
            self.visa.write(':sens:wav:span ', span)
        else:
            raise AttributeError('Wavelength span should be between 0.1-1100.0 nm')
    
    def get_sweep_mode(self):
        """
        Returns:
            sweep mode in a string
        """
        mode = self.visa.query_ascii_values(':init:smode?')[0]
        if mode == 1:
            return 'single'
        elif mode == 2:
            return 'repeat'
        elif mode == 3:
            return 'auto'
        else:
            return 'segment'
    
    def set_sweep_mode(self, mode=str):
        """
        Sets the sweep mode.

        Parameters:
            mode
                type: string
                desc: 'single', 'repeat', 'auto', or 'segment'
        
        Raises:
            AttributeError: <mode> is not one of the four accepted modes
        """
        settings = ['single', 'repeat', 'auto', 'segment']
        if mode in settings:
            self.visa.write(':init:smode ', mode)
        else:
            raise AttributeError('Mode must be "single", "repeat", "auto", or "segment".')
    
    def run_sweep(self):
        """
        Runs a sweep. Currently requires settings to be done prior to running this.
        """
        self.visa.write(':initiate')

    def extract_data(self):
        """
        Take a single shot of the on-screen data from the OSA.

        Returns:
            x
                type: float, array-like
                desc: x data of the active trace
            y
                type: float, array-like
                desc: y data of the active trace
        """

        # Stop the sweep
        self.visa.write(':abort')

        # Query which trace is active
        trace = self.visa.query_ascii_values(':trace:active?', converter='s')[0]
        trace = trace.rstrip()

        # Pull data from the active trace
        x = self.visa.query_ascii_values(':trace:x? ' + trace)
        y = self.visa.query_ascii_values(':trace:y? ' + trace)

        return x,y