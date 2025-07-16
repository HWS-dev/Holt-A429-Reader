import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QTextEdit
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor


class ARINC429GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARINC 429 Live Monitor")
        self.resize(800, 600)

        self.init_ui()
        self.setup_mock_data_feed()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Channel Selector, Data Format Selector, and Start/Stop Button
        top_bar = QHBoxLayout()

        self.channel_combo = QComboBox()
        self.channel_combo.addItems(["Channel 1", "Channel 2"])

        self.format_combo = QComboBox()
        self.format_combo.addItems(["Hex", "Binary", "BCD", "BNR"])

        self.toggle_button = QPushButton("Stop")
        self.toggle_button.clicked.connect(self.toggle_data_feed)

        top_bar.addWidget(QLabel("Select Channel:"))
        top_bar.addWidget(self.channel_combo)
        top_bar.addWidget(QLabel("Data Format:"))
        top_bar.addWidget(self.format_combo)
        top_bar.addStretch()
        top_bar.addWidget(self.toggle_button)
        main_layout.addLayout(top_bar)

        # ARINC 429 Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Label", "Data", "SSM"])
        main_layout.addWidget(QLabel("Live ARINC Words"))
        main_layout.addWidget(self.table)

        # Parsed Word Display
        main_layout.addWidget(QLabel("Word Details / Parser"))
        self.details_box = QTextEdit()
        self.details_box.setReadOnly(True)
        self.details_box.setTextColor(QColor("cyan"))
        main_layout.addWidget(self.details_box)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def setup_mock_data_feed(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_mock_data)
        self.timer.start(500)  # every 500 ms

    def toggle_data_feed(self):
        if self.timer.isActive():
            self.timer.stop()
            self.toggle_button.setText("Start")
        else:
            self.timer.start(500)
            self.toggle_button.setText("Stop")

    def add_mock_data(self):
        # Simulate an ARINC word
        label = random.randint(0, 255)
        data = random.randint(0, 0xFFFFF)
        ssm = random.randint(0, 3)
        time_str = "12:00:%02d" % random.randint(0, 59)

        # Format data based on selected format
        format_type = self.format_combo.currentText()
        if format_type == "Hex":
            data_str = f"{data:05X}"
        elif format_type == "Binary":
            data_str = f"{data:021b}"
        elif format_type == "BCD":
            data_str = self.to_bcd(data)
        elif format_type == "BNR":
            data_str = self.to_bnr(data)
        else:
            data_str = str(data)

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(time_str))
        self.table.setItem(row, 1, QTableWidgetItem(f"{label:02X}"))
        self.table.setItem(row, 2, QTableWidgetItem(data_str))
        self.table.setItem(row, 3, QTableWidgetItem(str(ssm)))

        self.details_box.setPlainText(
            f"Label: {label:02X}\nData: {data_str}\nSSM: {ssm}\nTimestamp: {time_str}"
        )

    def to_bcd(self, data):
        # Convert to BCD-like string for display (mock implementation)
        return " ".join(str((data >> i) & 0xF) for i in range(16, -1, -4))

    def to_bnr(self, data):
        # Mock BNR conversion (interpret as signed 2's complement of 21-bit number)
        if data & (1 << 20):  # Negative number
            data = data - (1 << 21)
        return f"{data}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ARINC429GUI()
    window.show()
    sys.exit(app.exec())
