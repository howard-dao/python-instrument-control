"""
Python wrapper for Keysight Signal Analyzers
Author(s): Howard Dao
"""

import pyvisa as visa
import numpy as np

class KeysightSA(visa.resources.GPIBInstrument):
    def __init__(self, visa):
        self.idn = visa.query('*IDN?')
        self.idn = self.idn.split(',')
        if self.idn[0] != 'Agilent Technologies':
            print('Device not recognized as a Keysight device.')
        self.visa = visa

        self.min_freq = None
        self.max_freq = None

    def get_center_freq(self):
        """
        Returns the center frequency.
        """
        return self.visa.query_ascii_values(':freq:cent?')[0]
    
    def set_center_freq(self, freq:float):
        """
        Sets the center frequency.

        Parameters:
            freq : float
                Frequency in Hz.
        """
        if freq < self.min_freq or freq > self.max_freq:
            raise ValueError(f'Input parameter <freq> must between {self.min_freq} and {self.max_freq}, given {freq}.')
        self.visa.write(f':freq:cent {freq}Hz')

    def get_freq_span(self):
        """
        Returns the frequency span.
        """
        return self.visa.query_ascii_values(':freq:span?')[0]
    
    def set_freq_span(self, span:float):
        """
        Sets the frequency span.

        Parameters:
            span : float
                Frequency span in Hz.
        """
        self.visa.write(f':freq:span {span}Hz')

    def get_freq_start(self):
        """
        Returns the start frequency.
        """
        return self.visa.query_ascii_values(':freq:start?')[0]
    
    def set_freq_start(self, freq:float):
        """
        Sets the start frequency.

        Parameters:
            freq : float
                Start frequency in Hz.
        """
        if freq < self.min_freq or freq > self.max_freq:
            raise ValueError(f'Input parameter <freq> must between {self.min_freq} and {self.max_freq}, given {freq}.')
        self.visa.write(f':freq:start {freq}Hz')
    
    def get_freq_stop(self):
        """
        Returns the stop frequency.
        """
        return self.visa.query_ascii_values(':freq:stop?')[0]
    
    def set_freq_stop(self, freq:float):
        """
        Sets the stop frequency.
        
        Parameters:
            freq : float
                Stop frequency in Hz.
        """
        if freq < self.min_freq or freq > self.max_freq:
            raise ValueError(f'Input parameter <freq> must between {self.min_freq} and {self.max_freq}, given {freq}.')
        self.visa.write(f':freq:stop {freq}Hz')

    def get_res_bw(self):
        """
        Returns resolution bandwidth.
        """
        return self.visa.query_ascii_values(':band?')[0]
    
    def set_res_bw(self, freq:float):
        """
        Sets resolution bandwidth.
        """
        self.visa.write(f':band {freq}')

    def averaging(self, count=100):
        """
        Sets sampling mode to averaging.

        Parameters:
            count : int, optional
                Number of samples to average over.
        """
        self.visa.write(':trace:type aver')
        self.visa.write(f':aver:coun {count}')

    def get_trace(self):
        """
        Returns trace.

        Returns:
            ndarray : Frequencies
            ndarray : Trace
        """
        self.visa.write(':form:data real,32')

        # Set byte order to little endian
        byte_order = self.visa.query_ascii_values(':form:bord?', converter='s')[0].rstrip()
        if byte_order == 'NORM':
            self.visa.write(':form:bord swap')

        # Acquire trace
        trace = self.visa.query_binary_values(':trace:data? trace1', datatype='f', is_big_endian=False)
        trace_arr = np.asarray(trace)

        # Calculate frequencies
        f1 = self.get_freq_start()
        f2 = self.get_freq_stop()
        freq = np.linspace(f1, f2, len(trace_arr))

        return freq, trace_arr


class N9010A(KeysightSA):
    def __init__(self, visa):
        super().__init__(visa)
        if self.idn[1] != 'N9010A':
            print(f'{self.idn[0]} device not recognized as N9010A.')
        self.visa = visa

        self.min_freq = 10
        self.max_freq = 44e9