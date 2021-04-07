import click
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyfirmata
import time

matplotlib.rcParams['font.sans-serif'] = ['Palatino', 'sans-serif']

@click.command()
@click.option('--time', '-t', 't1', default=60, help='How long to record data in seconds.')
def start(t1):
    click.echo('The time you selected was: %s' % t1)
    with click.progressbar(range(0, 1000*t1)) as bar:
        for x in bar:
            pass
            # time.sleep(1/1000)
    t = np.linspace(0, t1, 10*t1)
    s = 1 + np.sin(2 * np.pi * t)
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    ax.grid()
    fig.savefig("foo.pdf", bbox_inches='tight')
    plt.show()

def gather(time, h):
    
    reading = board.get_pin('a:0:i')

if __name__ == '__main__':
    start()