# noisegen/audio/generator.py
import numpy as np
import logging

def noise_psd(N, psd=lambda f: 1):
    # Add comments here
    x_white = np.fft.rfft(np.random.randn(N))
    s = psd(np.fft.rfftfreq(N))
    logging.debug(f"PSD values: {s}")
    # Normalize S
    s = s / np.sqrt(np.mean(s ** 2))
    x_shaped = x_white * s
    return np.fft.irfft(x_shaped)


def PSDGenerator(f):
    return lambda N: noise_psd(N, f)


@PSDGenerator
def white_noise(f):
    return 1


@PSDGenerator
def blue_noise(f):
    return np.sqrt(f)


@PSDGenerator
def violet_noise(f):
    return f


@PSDGenerator
def brown_noise(f):
    return 1 / np.where(f == 0, 1, f)


@PSDGenerator
def pink_noise(f):
    return 1 / np.where(f == 0, 1, np.sqrt(f))


def generate_noise(noise_type, duration=30, sample_rate=44100):
    N = duration * sample_rate
    noise = noise_type(N)
    logging.debug(f"Generated noise (before normalization): {noise[:10]}")
    return normalize(noise)


def normalize(noise):
    noise = np.nan_to_num(noise)
    max_val = np.max(np.abs(noise))
    logging.debug(f"Max value in noise: {max_val}")
    if max_val > 0:
        noise = noise / max_val
    noise = np.int16(noise * 32767)
    logging.debug(f"Normalized noise (first 10 values): {noise[:10]}")
    return noise
