# noisegen/audio/player.py

import pyaudio
import numpy as np
from threading import Thread, Event

class AudioPlayer:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_playing = False
        self._stop_event = Event()

    def _play_audio(self, samples):
        # Play audio in separate thread
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.sample_rate,
                                  output=True)
        # Convert to 16-bit PCM
        samples = (samples * 32767).astype(np.int16).tobytes()
        self.is_playing = True

        while not self._stop_event.is_set():
            self.stream.write(samples)

        self.stream.stop_stream()
        self.stream.close()

    def play(self, samples):
        if self.is_playing:
            self._stop_event.set()
        self._stop_event.clear()
        self.play_thread = Thread(target=self._play_audio, args=(samples,))
        self.play_thread.start()

    def pause(self):
        if self.is_playing:
            self._stop_event.set()
            self.is_playing = False

    def stop(self):
        self._stop_event.set()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.is_playing = False

    def __del__(self):
        self.p.terminate()

