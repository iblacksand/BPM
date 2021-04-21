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
