# dsp-crossover

A Python DSP tool for designing and analysing crossover filters, used for a DIY PA system (1 sub, 2 tops), built to understand DSP crossover theory before implementing on hardware.

## What it does
- Designs Butterworth and Linkwitz-Riley crossover filters at variable orders
- Plots filter frequency response on a flat curve
- Analyses the frequency spectrum of an audio file (Welch's method or single FFT)
- Shows filter responses on frequency spectrum
- Saves frequency response graph
- Applies filters to audio and save as .wav files

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
Follow terminal prompts

## Project context
Part of a DIY PA build  
- 15" Eminence Kappalite 3015LF sub 
- 2x 8" mid-woofer tops.
- 2x tweeter TBD
- Target crossover  80-100Hz
Python DSP crossover used before the amps to split into frequency bands

## Limitations
- Only 2 way crossover, no mid band support
- Audio saving is only allowed with .wav files
- No input validation on terminal prompts

## Planned
- 3 way crossover for sub/mid/tweeter
- Real time animated spectrum display
- Microcontroller implementation using CMSIS-DSP on ARM Cortex-M 
- CamillaDSP export for Raspberry Pi deployment