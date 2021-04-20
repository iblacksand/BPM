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
    bpm = 10
    f = 100
    noiselevel = 1
    randgen = np.random
    x = np.arange(0,5,1/(f))  #interval=0.1, 300 samples
    noise = noiselevel*randgen.randn(len(x))
    y = np.abs(np.sin(bpm/60*np.pi*x) + noise)
    # f = calculate(y, f, True);
    g = calcspec(y, f, True);

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
    peaks,_ = find_peaks(x, prominence=1)
    # bpms = []
    # for i in range(0, len(peaks[0])-1):
    #     bpms.append(1/(peaks[0][i+1] - peaks[0][i])*f*60)
    # bpm = np.average(bpms)
    bpm = 1/(peaks[len(peaks) - 1] - peaks[len(peaks) - 2])*f*60
    if showa:
        fig, (ax, bx) = plt.subplots(1, 2)
        ax.plot(peaks, x[peaks], "ob"); ax.plot(x); ax.legend(['prominence'])
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

def calcspec(data, f, showf):
    """calculates bpm using FFT

    Args:
        data (double array): data to calculate BPM from
        f (double): frequency of signal
        showf (boolean): controls whether graph of fft is shown
    """    
    data = data - np.average(data)
    Y = np.fft.fft(data)
    Y = np.abs(Y)
    freq = np.fft.fftfreq(len(data), 1/f)
    peaks,_ = find_peaks(Y, prominence=1)
    peakY = np.max(Y) # Find max peak
    locY = np.argmax(Y) # Find its location
    maxf = freq[locY]
    print("max frequency: " + str(maxf))
    print("Converted to bpm: " + str(maxf*60))
    if showf:
        fig, (ax, bx) = plt.subplots(1, 2)
        ax.plot(Y); ax.plot(peaks, Y[peaks], "ob");  ax.legend(['prominence'])
        bx.plot(data)
        plt.show()
    return maxf*60
if __name__ == '__main__':
    start()