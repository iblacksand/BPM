import click
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
@click.option('--cycle', '-c', 'cycle', default=5, show_default=True, help='How long each cycle takes before calculing BPM')
@click.option('--brightness', '-b', 'b', default=0.85, show_default=True, help='Percent brightness for the LED')
@click.option('--frequency', '-f', 'f', default=20, show_default=True, help='Data acquisition frequency.')
@click.option('--save', '-s', 's', is_flag=True, help='save the data after processing')
@click.option('--show-autocorrelation', '-showa', 'showa', is_flag=True, help='Show the results of autocorrelation')
def start(t1, cycle, b, f, s, showa):
    click.clear()
    style.use('fivethirtyeight')
    click.echo('The time you selected was: %s' % t1)
    mass_data = []
    bpms = []
    with click.progressbar(range(0, np.ceil(t1/cycle))) as bar:
        for x in bar:
            data = gather(cycle, f)
            mass_data.append(data)
            bpm = calculate(data, f, showa)
            bpms.append(bpm)
            avbpm = np.average(bpms)
            click.echo("\nCurrent BPM: " + str(bpm) + "\n" + "Average BPM: "+ str(avbpm))
            click.clear()
    t = np.linspace(0, t1, 10*t1)
    s = 1 + np.sin(2 * np.pi * t)
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    ax.grid()
    plt.show()
    if s:
        save(mass_data)
    

def gather(cycle, f):
    tick = 1/f
    data = []
    for i in range(0, ceil(cycle/tick)):
        data[i] = board.get_pin('a:0:i')
        time.sleep(tick)
    return data

def calculate(data, f, showa):
    x = autocorr(data)
    peaks = find_peaks(x, prominence=1)
    bpms = []
    for i in range(0, len(peaks)-1):
        bpms[i] = 1/(peaks[i+1] - peaks[i])*f*60
    bpm = np.average(bpms)
    return bpm
def save(data):
    files = [ ('Comma-separated values', '*.csv')]
    file = asksaveasfile(filetypes = files, defaultextension = files)
    a = np.asarray(data)
    a.tofile(file.name,sep=',',format='%10.5f')

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size/2:]
if __name__ == '__main__':
    start()