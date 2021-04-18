"""
Streaming Data from a Microphone 
Live Audio Spectrum on Time & Frequency Domain 
References : 
    👉[Fourier Transforms (scipy.fft)]SciPy v1.6.1 Reference Guide : https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html

Read wav file to playback and analyze sound
"""

import os, sys, time
import struct
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import wave
import pyaudio

#########################################################################################################
def live_audio_from_mic():
    """
    Streaming Data from a Microphone
    Live Audio Spectrum on Time & Frequency Domain
    """

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

    fig, (ax_time, ax_fft) = plt.subplots(2, figsize=(8, 5))

    # time domain
    x_time = np.arange(0, int(CHUNK / 2))  # time domain samples
    ax_time.set_ylim(-150, 150)
    (line_time,) = ax_time.plot(x_time, np.random.rand(int(CHUNK / 2)), "-", lw=1)

    # frequency domain
    x_fft = np.linspace(0, RATE, CHUNK, endpoint=False)  # frequency domain frequencies
    (line_fft,) = ax_fft.semilogx(x_fft, np.random.rand(CHUNK), "-", lw=1)

    plt.show(block=False)

    # finish playback by enter ctrl-c
    print("Enter ctrl-c to finish playback")
    try:
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
    except KeyboardInterrupt:
        # stop stream (4)
        stream.stop_stream()
        stream.close()
        # close PyAudio (5)
        p.terminate()
        sys.exit("finished")


#########################################################################################################
def wav_audio_from_file():
    """
    Read wav file to playback and analyze sound
    """

    CHUNK = 1024
    wav_file = select_wavfile()
    wf = wave.open(wav_file, "rb")

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )

    # read data
    data = wf.readframes(CHUNK)

    # finish playback by enter ctrl-c
    print("Enter ctrl-c to finish playback")

    try:
        # play stream (3)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)
    except KeyboardInterrupt:
        sys.exit("finished")

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()


#########################################################################################################
def select_wavfile():
    wav_file_path = r"C:\Users\mohyu\Desktop\Workspace\codes-snippets"
    files = os.listdir(wav_file_path)
    for f in files:
        print(f"{files.index(f)+1:3d} -> {f}")
    get_wav_file_number = int(input("Enter a number for wav file!\n")) - 1
    return wav_file_path + "\\" + files[get_wav_file_number]


#########################################################################################################
# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)
# wf = wave.open(sys.argv[1], 'rb')

mic_or_wav = input("Which input? [Microphone | Wav File]\nEnter 'm' or 'w'\t")
if mic_or_wav == "m":
    live_audio_from_mic()
elif mic_or_wav == "w":
    wav_audio_from_file()
else:
    pass
