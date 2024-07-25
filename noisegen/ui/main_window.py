# noisegen/noisegen/ui/main_window.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from noisegen.audio.generator import generate_noise, white_noise, pink_noise, blue_noise, brown_noise, violet_noise
from noisegen.audio.player import AudioPlayer

class SpectrogramWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.ax.set_title("Spectrogram")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude (dB)")

    def plot(self, samples, sample_rate=44100):
        freqs, psd = np.fft.fftfreq(len(samples), 1/sample_rate), np.abs(np.fft.fft(samples))**2
        self.ax.clear()
        self.ax.plot(freqs[:len(freqs)//2], 10*np.log10(psd[:len(psd)//2]))
        self.ax.set_title("Spectrogram")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude (dB)")
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_player = AudioPlayer()
        self.setWindowTitle("NoiseGen")
        self.current_samples = None
        self.visualizer = None
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        btn_layout = QVBoxLayout()
        visualizer_control_layout = QVBoxLayout()

        # Buttons in left column
        white_noise_btn = QPushButton("White")
        violet_noise_btn = QPushButton("Violet")
        brown_noise_btn = QPushButton("Brown")
        pink_noise_btn = QPushButton("Pink")
        blue_noise_btn = QPushButton("Blue")

        white_noise_btn.clicked.connect(self.play_white_noise)
        violet_noise_btn.clicked.connect(self.play_violet_noise)
        brown_noise_btn.clicked.connect(self.play_brown_noise)
        blue_noise_btn.clicked.connect(self.play_brown_noise)
        pink_noise_btn.clicked.connect(self.play_brown_noise)

        btn_layout.addWidget(white_noise_btn)
        btn_layout.addWidget(violet_noise_btn)
        btn_layout.addWidget(brown_noise_btn)
        btn_layout.addWidget(pink_noise_btn)
        btn_layout.addWidget(blue_noise_btn)
        btn_layout.addStretch()

        # Visualizer in main part of window
        self.visualizer = SpectrogramWidget(self)
        self.visualizer.setFixedSize(600, 400)
        self.visualizer.setStyleSheet("background-color: #2E2E2E;")

        play_stop_btn = QPushButton("Play/Stop")
        play_stop_btn.clicked.connect(self.play_stop_audio)

        visualizer_control_layout.addWidget(self.visualizer)
        visualizer_control_layout.addWidget(play_stop_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addLayout(visualizer_control_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.applyStyles()

    def play_white_noise(self):
        samples = generate_noise(white_noise, duration=30)
        self.current_samples = samples
        self.audio_player.play(samples)
        self.visualizer.plot(samples)

    def play_pink_noise(self):
        samples = generate_noise(pink_noise, duration=30)
        self.current_samples = samples
        self.audio_player.play(samples)
        self.visualizer.plot(samples)

    def play_violet_noise(self):
        samples = generate_noise(violet_noise, duration=30)
        self.current_samples = samples
        self.audio_player.play(samples)
        self.visualizer.plot(samples)

    def play_brown_noise(self):
        samples = generate_noise(brown_noise, duration=30)
        self.current_samples = samples
        self.audio_player.play(samples)
        self.visualizer.plot(samples)

    def play_blue_noise(self):
        samples = generate_noise(blue_noise, duration=30)
        self.current_samples = samples
        self.audio_player.play(samples)
        self.visualizer.plot(samples)

    def play_stop_audio(self):
        if self.audio_player.is_playing:
            self.audio_player.stop()
        else:
            if self.current_samples is not None:
                self.audio_player.play(self.current_samples)
                self.visualizer.plot(self.current_samples)

    def applyStyles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color:  #E0E0E0;
            }
            QPushButton {
                background-color: #333333;
                color: #E0E0E0;
                border:  1px solid #555555;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
