"""
Python wrapper for Yokogawa Optical Spectrum Analyzers
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class AQ6370D(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'YOKOGAWA' and self.idn[1] != 'AQ6370D':
            print('Device not recognized as Yokogawa AQ6370D.')
        self.visa = visa

        self.min_wl = 600e-9
        self.max_wl = 1700e-9
        self.min_span = 0.1e-9
        self.max_span = 1100e-9

    def get_wave_center(self):
        """
        Returns the center wavelength in meters.

        Returns:
            lam : float
                Center wavelength in meters.
        """
        lam = self.visa.query_ascii_values(':sens:wav:cent?')[0]
        return lam
    
    def set_wave_center(self, lam:float):
        """
        Sets the center wavelength in meters.
        
        Parameters:
            lam : float
                Center wavelength in meters.

        Raises:
            ValueError: <lam> is out of range.
        """
        if lam >= self.min_wl and lam <= self.max_wl:
            self.visa.write(f':sens:wav:cent {lam}')
        else:
            raise ValueError(f'Input parameter <lam> must be between {self.min_wl} and {self.max_wl}.')
    
    def get_wave_span(self):
        """
        Returns the wavelength span in meters.

        Returns:
            span : float
                Wavelength span in meters.
        """
        span = self.visa.query_ascii_values(':sens:wav:span?')[0]
        return span
    
    def set_wave_span(self, span:float):
        """
        Sets the wavelength span in meters.

        Parameters:
            span : float
                Wavelength span in meters.
        
        Raises:
            ValueError: <span> is out of range.
        """
        if span >= self.min_span and span <= self.max_span:
            self.visa.write(f':sens:wav:span {span}')
        else:
            raise ValueError(f'Input parameter <span> must be between {self.min_span} and {self.max_span}.')
    
    def get_sweep_mode(self):
        """
        Returns the measuring sweep mode.
        Could return 'single', 'repeat', 'auto', or 'segment'.

        Returns:
            str: Sweep mode.
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
    
    def set_sweep_mode(self, mode:str):
        """
        Sets the sweep mode.

        Parameters:
            mode : str
                Sweep mode. Either 'single', 'repeat', 'auto', or 'segment'.
        
        Raises:
            ValueError: <mode> is not one of the four accepted modes
        """
        settings = ['single', 'repeat', 'auto', 'segment']
        if mode.lower() in settings:
            self.visa.write(f':init:smode {mode}')
        else:
            raise ValueError('Input paramter <mode> must be "single", "repeat", "auto", or "segment".')
    
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
        x = self.visa.query_ascii_values(f':trace:x? {trace}')
        y = self.visa.query_ascii_values(f':trace:y? {trace}')

        return x,y