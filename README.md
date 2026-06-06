# dsp-crossover

A Python DSP tool for a designing and analysing crossover filters, used for a DIY PA system (1 sub, 2 tops)

## What it does
- Designs Butterworth and Linkwitz-Riley crossover filters (user defined)
- Plots filter frequency response on a flat curve
- Analyses the frequency spectrum of an audio file (FFT or Welch method)
- Show filter responses on audio spectrum
- Apply filters to audio and export as .wav files

## Filter types
- Butterworth - Flat passband, -3dB at crossover
- Linkwitz-Riley - Flat combined response, -6dB at crossover, industry standard for PA systems

## Tech
- Python 3.13
- numpy — array operations and FFT
- scipy — filter design (butter, sosfilt, sosfreqz, welch)
- matplotlib — frequency response and spectrum plotting
- soundfile — audio file I/O

## Usage
```bash
python crossover.py
```
Follow Terminal Prompts

## Project context
Part of a DIY PA build  
- 15" Eminence Kappalite 3015LF sub 
- 2x 8" mid-woofer tops.
- 2x tweeter TBD
- Target crossover  80-100Hz
Python DSP crossover used before the amps to split frequencies or boost/dip

## Planned
- 3 way crossover for sub/mid/tweeter
- Real time animated spectrum display
- Microcontroller implimentation