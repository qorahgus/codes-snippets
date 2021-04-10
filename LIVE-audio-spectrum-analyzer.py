"""
Streaming Data from a Microphone 
Live Audio Spectrum on Time & Frequency Domain 
References : 
    👉[Fourier Transforms (scipy.fft)]SciPy v1.6.1 Reference Guide : https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html
"""

import os
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from scipy.fftpack import fft

# constants
CHUNK = 1024  # samples per frame
FORMAT = pyaudio.paInt16  # audio format (bytes per sample?)
CHANNELS = 1  # single channel for microphone
RATE = 44100  # samples per second

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK,
)

# audio_raw = stream.read(CHUNK)
# audio_int = struct.unpack(str(2 * CHUNK) + "B", audio_raw)
# audio_array = np.array(audio_int, dtype="b")

# fig, (ax_time) = plt.subplots()
# ax_time.plot(audio_array)
# plt.show()


fig, (ax_time, ax_fft) = plt.subplots(2, figsize=(8, 5))

# time domain
x_time = np.arange(0, int(CHUNK / 2))  # time domain samples
ax_time.set_ylim(-150, 150)
(line_time,) = ax_time.plot(x_time, np.random.rand(int(CHUNK / 2)), "-", lw=1)

# frequency domain
x_fft = np.linspace(0, RATE, CHUNK, endpoint=False)  # frequency domain frequencies
(line_fft,) = ax_fft.semilogx(x_fft, np.random.rand(CHUNK), "-", lw=1)

plt.show(block=False)

while True:
    # binary microphone raw data
    audio_raw = stream.read(CHUNK)
    # convert data to integers
    audio_int = struct.unpack(str(2 * CHUNK) + "B", audio_raw)

    # time domain make numpy array with reduced data by every 8th values for displaying vivid signal
    audio_array = np.array(audio_int, dtype="b")[::4]
    line_time.set_ydata(audio_array)

    # compute FFT and update line
    fft_array = fft(audio_int)
    line_fft.set_ydata(np.abs(fft_array[0:CHUNK]) / (128 * CHUNK))
    # print(np.abs(fft_array[0:CHUNK]).max(), np.abs(fft_array[0:CHUNK]).min())

    fig.canvas.draw()
    fig.canvas.flush_events()
