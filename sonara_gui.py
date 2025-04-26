import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from spotify_api import getCurrentSong

class SonaraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sonara 🎶")
        self.setGeometry(1100, 300, 800, 600)

        # Outer layout - controls overall spacing
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setAlignment(Qt.AlignTop)

        # Inner layout - holds your widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        # Welcome label
        self.welcomeLabel = QLabel("Welcome to Sonara 🎵")
        self.welcomeLabel.setFont(QFont("Montserrat", 25))
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcomeLabel)

        # Current song label
        self.song_label = QLabel("🎵 No song yet")
        self.song_label.setFont(QFont("Montserrat", 20))
        self.song_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.song_label)

        # Get song button
        self.button = QPushButton("Get Current Song")
        self.button.setFont(QFont("Montserrat", 18))
        self.button.clicked.connect(self.display_song)
        self.layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # Container widget holds inner layout
        container = QWidget()
        container.setLayout(self.layout)

        # Add container to outer layout
        outer_layout.addWidget(container, alignment=Qt.AlignTop)
        self.setLayout(outer_layout)

    def display_song(self):
        song = getCurrentSong()
        self.song_label.setText(f"🎵 {song}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SonaraApp()
    window.show()
    sys.exit(app.exec_())
