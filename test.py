from os import abort
import click
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import pyfirmata
import time
from tkinter.filedialog import asksaveasfile
from scipy.signal import find_peaks
# Testing printing out the data
def start():
    x = np.arange(0,30,0.1)  #interval=0.1, 300 samples
    y = np.sin(x)
    calculate(y, 20, True)

def calculate(data, f, showa):
    """calculates the beats per minute of a provided signal

    Args:
        data (double array): array of voltages to calculate bpm from
        f (frequency): frequency used to collect the data
        showa (boolean): whether or not to show the graph of the autocorrelation

    Returns:
        double: the beats per minute of the signal
    """    
    x = autocorr(data)
    peaks = find_peaks(x, prominence=1)
    bpms = []
    for i in range(0, len(peaks)-1):
        bpms.append(1/(peaks[0][i+1] - peaks[0][i])*f*60)
    bpm = np.average(bpms)
    if showa:
        fig, (ax, bx) = plt.subplots(1, 2)
        ax.plot(peaks[0], x[peaks[0]], "ob"); ax.plot(x); ax.legend(['prominence'])
        bx.plot(data)
        plt.show()
    return bpm

def autocorr(x):
    """runs autocorrelation on the provided array

    Args:
        x (double array): array to run autocorrelation on

    Returns:
        double array: results of the autocorrelation
    """
    result = np.correlate(x, x, mode='full')
    
    return result[math.floor(result.size/2):]
if __name__ == '__main__':
    start()