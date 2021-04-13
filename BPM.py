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

matplotlib.rcParams['font.sans-serif'] = ['Palatino', 'sans-serif']

@click.command()
@click.option('--time', '-t', 't1', default=60, show_default=True, help='Total time to record data in seconds.')
@click.option('--cycle', '-c', 'cycle', default=5, show_default=True, help='How long each cycle takes before calculating BPM')
@click.option('--brightness', '-b', 'b', default=0.85, show_default=True, help='Percent brightness for the LED')
@click.option('--frequency', '-f', 'f', default=20, show_default=True, help='Data acquisition frequency.')
@click.option('--save', '-s', 's', is_flag=True, help='save the data after processing')
@click.option('--show-autocorrelation', '-showa', 'showa', is_flag=True, help='Show the results of autocorrelation')
@click.option('--port', '-p', 'port', default='/dev/cu.usbmodem11301', show_default=True, prompt='Arduino Port', help='The port of the Arduino.')
# test of this shit
def start(t1, cycle, b, f, s, showa, port): 
    '''Runs the data collection and calculations
    ''' 
    board = pyfirmata.Arduino(port)
    it = pyfirmata.util.Iterator(board)
    it.start()
    click.clear()
    analog_input = board.get_pin('a:0:i')
    led = board.get_pin('d:3:p')
    led.write(b)
    style.use('fivethirtyeight')
    click.echo('The time you selected was: %s' % t1)
    mass_data = []
    bpms = []
    for x in range(0, math.ceil(t1/cycle)):
        data = gather(analog_input, cycle, f)
        mass_data.extend(data)
        bpm = calculate(data, f, showa)
        bpms.append(bpm)
        avbpm = np.average(bpms)
        click.echo("\nCurrent BPM: " + str(bpm) + "\n" + "Average BPM: "+ str(avbpm))
    t = np.linspace(0, t1, f*t1)
    fig, ax = plt.subplots()
    ax.plot(mass_data)
    ax.set(xlabel='time (s)', ylabel='voltage (V)',
        title='Total Voltages')
    ax.grid()
    print('BPM using all data: ' + str(calculate(mass_data, f, showa)))
    plt.show()
    if s:
        save(mass_data)

def gather(analog_input, cycle, f):
    """gathers voltage readings for the specified amount of time

    Args:
        cycle (int): length of time to run the cycle
        f (int): frequency of collection

    Returns:
        double array: array of the voltages collected at the frequency rate
    """    
    tick = 1/f
    data = []
    print()
    for i in range(0, math.ceil(cycle/tick)):
        reading = analog_input.read()
        if reading != None:
            data.append(5*reading)
            print('Measured Voltage: ' + str(data[len(data)-1]), end = "\r")
        time.sleep(tick)
    return data

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

def save(data):
    """saves the given data into a csv file

    Args:
        data (double array): array to save into a csv file
    """    
    files = [ ('Comma-separated values', '*.csv')]
    file = asksaveasfile(filetypes = files, defaultextension = files)
    a = np.asarray(data)
    a.tofile(file.name,sep=',',format='%10.5f')

def autocorr(x):
    """runs autocorrelation on the provided array

    Args:
        x (double array): array to run autocorrelation on

    Returns:
        double array: results of the autocorrelation
    """
    result = np.correlate(x, x, mode='full')
    return result[math.floor(result.size/2):]

def normalize(x):
    norm = np.linalg.norm(x)
    return x/norm

if __name__ == '__main__':
    start()