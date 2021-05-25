# BPM

Code of the Baby Pulse Monitor CLI

## Options

From `python BPM.py --help`:

```
Usage: BPM.py [OPTIONS]

  Runs the data collection and calculations

Options:
  -t, --time INTEGER       Total time to record data in seconds.  [default:
                           60]

  -c, --cycle INTEGER      How long each cycle takes before calculating BPM
                           [default: 5]

  -b, --brightness FLOAT   Percent brightness for the LED  [default: 0.85]
  -f, --frequency INTEGER  Data acquisition frequency.  [default: 20]
  -s, --save               save the data after processing
  -showp, --show-plot      Show the results of autocorrelation or FFT
  -p, --port TEXT          The port of the Arduino.  [default:
                           /dev/cu.usbmodem1101]

  --help                   Show this message and exit.
```

## Requirements

Pip Packages:

- click
- matplotlib
- numpy
- pyfirmata
- tkinter
- scipy

## Arduino Set-up

1. Install Firmata onto Arduino
  - Instructions can be found [here.](https://ecraft2learn.github.io/uui/about/firmata-installation-instructions.pdf)
2. Note the port used by the Arduino(ex: `COM4`)

## Example command

If the port is COM4, you can run the following command

```
python BPM.py -p COM4 -f 20 -t 30
```

This will collect data for 30 seconds with a frequency of 20 Hz using port `COM4`.

If you ever need to quit, you can use <kbd>CTRL+C</kbd>.