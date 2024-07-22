# noisegen/noisegen/ui/main_window.py

from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from noisegen.audio.generator import gen_white_noise, gen_green_noise, gen_brown_noise, gen_blue_noise, gen_pink_noise
from noisegen.audio.player import AudioPlayer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_player = AudioPlayer()
        self.setWindowTitle("NoiseGen")
        self.current_samples = None
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        btn_layout = QVBoxLayout()

        # Buttons in left column
        white_noise_btn = QPushButton("White")
        green_noise_btn = QPushButton("Green")
        brown_noise_btn = QPushButton("Brown")
        pink_noise_btn = QPushButton("Pink")
        blue_noise_btn = QPushButton("Blue")

        white_noise_btn.clicked.connect(self.play_white_noise)
        green_noise_btn.clicked.connect(self.play_green_noise)
        brown_noise_btn.clicked.connect(self.play_brown_noise)
        blue_noise_btn.clicked.connect(self.play_brown_noise)
        pink_noise_btn.clicked.connect(self.play_brown_noise)

        btn_layout.addWidget(white_noise_btn)
        btn_layout.addWidget(green_noise_btn)
        btn_layout.addWidget(brown_noise_btn)
        btn_layout.addWidget(pink_noise_btn)
        btn_layout.addWidget(blue_noise_btn)
        btn_layout.addStretch()

        # Visualizer in main part of window
        visualizer = QWidget()
        visualizer.setFixedSize(600, 400)
        visualizer.setStyleSheet("background-color: #2E2E2E;")

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(visualizer)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.applyStyles()

    def play_white_noise(self):
        samples = gen_white_noise(duration=30)  # 10 seconds
        self.current_samples = samples
        self.audio_player.play(samples)

    def play_pink_noise(self):
        samples = gen_pink_noise(duration=30)  # 10 seconds
        self.current_samples = samples
        self.audio_player.play(samples)

    def play_green_noise(self):
        samples = gen_green_noise(duration=30)  # 10 seconds
        self.current_samples = samples
        self.audio_player.play(samples)

    def play_brown_noise(self):
        samples = gen_brown_noise(duration=30)  # 10 seconds
        self.current_samples = samples
        self.audio_player.play(samples)

    def play_blue_noise(self):
        samples = gen_blue_noise(duration=30)  # 10 seconds
        self.current_samples = samples
        self.audio_player.play(samples)



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
