# diff_press_logger_o

This is a personal project of 'emguse'.
It measures the differential pressure and records an event when there is a sudden change.
This project is a twin project and comes in two flavors, using sensors from different manufacturers.

I have a sibling project where I ported it to a microcontroller and ran it on a Raspberry Pi pico and CircuitPython.
[emguse/circuit_pico_logger_o](/circuit_pico_logger_o)

# What you need

- Raspberry Pi 4 4GB model
- OMRON D6F-PH0505 Differential pressure sensor 
- Other excitation piezoelectric buzzer
- Thermal printer DP-EH600 (optional)
- TrueType font file

# Features

- Event recording (CSV file)
- Event recording (WAV file)
- Event recording (print to thermal printer)
- Pre- and post-event recording is possible. (Number of seconds can be set.)
- Moving average recording
- Trigger detection using differences from past measurements

# Usage

1. Add any '.ttf' font files to the directory.
1. $ mkdir log
1. $ python diff_press_logger_o.py

# Requirement

smbus2
RPi.GPIO
thermalprinter
Pllow
numpy

# Author

- Author: emguse
- Personal Projects
- e-mail: noreply

# License

"diff_press_logger_o" is under [MIT license]

Copyright 2021 emguse

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.