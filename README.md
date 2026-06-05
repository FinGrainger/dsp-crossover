# dsp-crossover

A Python implementation of a digital crossover filter for a DIY PA system (1 sub, 2 tops)

## What it does
Splitting audio signal into 3 frequency bands (sub, mids, highs)
- Subwoofer channel - low-pass filter, below 90Hz
- Midwoofer channel - high-pass filter, above 90Hz
- Tweeter channel - TBC

Using a 4th order Butterworth filter designed with scipy.

## Tech
- Python 3.13
- numpy
- scipy
- matplotlib

## Usage
```bash
python crossover.py
```

## Project context
Part of a DIY PA build  
- 15" Eminence Kappalite 3015LF sub 
- 2x 8" mid-woofer tops.
- 2x tweeter TBD