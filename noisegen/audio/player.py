# noisegen/audio/player.py

import sounddevice as sd
from threading import Thread, Event
import logging

logging.basicConfig(level=logging.DEBUG)
class AudioPlayer:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.stream = None
        self.is_playing = False
        self._stop_event = Event()
        self.play_thread = None

    def _play_audio(self, samples):
        # Play audio in separate thread
        self.is_playing = True
        samples = samples.copy()

        def callback(outdata, frames, time, status):
            nonlocal samples
            if status:
                print(status)
                logging.debug(f"Status: {status}")
            if self._stop_event.is_set():
                raise sd.CallbackAbort
            if len(samples) >= frames:
                outdata[:] = samples[:frames].reshape(-1, 1)
                samples = samples[frames:]
                logging.debug(f"Frames written: {frames}, Remaining samples: {len(samples)}")
            else:
                outdata[:len(samples)] = samples.reshape(-1, 1)
                outdata[len(samples):] = 0
                self._stop_event.set()
                logging.debug(f"Last frames written: {len(samples)}, Buffer underflow prevented")

        self.stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=callback,
            blocksize=2048,
            latency='high'
        )
        self.stream.start()
        logging.debug(f"Stream started with sample rate: {self.sample_rate}")

    def play(self, samples):
        if self.is_playing:
            self.stop()
        self._stop_event.clear()
        self.play_thread = Thread(target=self._play_audio, args=(samples,))
        self.play_thread.start()
        logging.debug("Playback started")

    def pause(self):
        if self.is_playing:
            self._stop_event.set()
            self.is_playing = False
            logging.debug("Playback paused")

    def stop(self):
        self._stop_event.set()
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
        self.is_playing = False
        logging.debug("Playback stopped")

    def __del__(self):
        if self.stream is not None:
            self.stream.close()
        logging.debug("Stream closed")