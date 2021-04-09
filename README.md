# BPM

Code of the Baby Pulse Monitor CLI

## Options

From `python BPM.py --help`:

```
Usage: BPM.py [OPTIONS]

Options:
  -t, --time INTEGER              Total time to record data in seconds.
                                  [default: 60]

  -c, --cycle INTEGER             How long each cycle takes before calculing
                                  BPM  [default: 5]

  -b, --brightness FLOAT          Percent brightness for the LED  [default:
                                  0.85]

  -f, --frequency INTEGER         Data acquisition frequency.  [default: 20]
  -s, --save                      save the data after processing
  -showa, --show-autocorrelation  Show the results of autocorrelation
  --help                          Show this message and exit.
```

## Requirements

Pip Packages:

- click
- matplotlib
- numpy
- pyfirmata
- tkinter
- scipy
