import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QTextEdit
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QPixmap

#creates main window after starup
class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Holt A429 Analyzer - Main Menu")
        self.resize(400, 300)

        
        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Left horizontal layout
        left_layout = QVBoxLayout()
        # left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)

        #setup channel select
        self.channel_combo = QComboBox()
        self.channel_combo.addItems(["Channel 1", "Channel 2"])
        channel_label = QLabel("Select Channel:")
        left_layout.addWidget(channel_label)
        channel_label.setStyleSheet("font-size: 16px;")
        left_layout.addWidget(self.channel_combo)
        left_layout.addSpacing(10)

        #setup speed select - ***NEED TO INCORPORATE LOGIC***
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["Low", "High"])
        speed_label = QLabel("Select A429 Speed:")
        left_layout.addWidget(speed_label)
        speed_label.setStyleSheet("font-size: 16px;")
        left_layout.addWidget(self.speed_combo)
        left_layout.addSpacing(10)

        #setup data format (remove)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Hex", "Binary", "BCD", "BNR"])
        format_label = QLabel("Select Data Format:")
        left_layout.addWidget(format_label)
        format_label.setStyleSheet("font-size: 16px;")
        left_layout.addWidget(self.format_combo)
        left_layout.addSpacing(20)

        #setup start/stop button. 
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.launch_data_window)
        left_layout.addWidget(self.start_stop_button)
        # layout.addStretch()

        #right side layout for logo
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo.png").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)


        #assemble main layout
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.logo)


        #setup window in container
        container = QWidget()                                   #creates the container 
        container.setLayout(main_layout)                        #assigns layout to container
        # container.setStyleSheet("background-color: #4B1E1E;")   #soft red
        self.setCentralWidget(container)                        #sets container as main content

    def launch_data_window(self):
        channel = self.channel_combo.currentText()
        format_type = self.format_combo.currentText()
        speed = self.speed_combo.currentText()
        self.data_window = ARINC429GUI(channel=channel,format_type=format_type, speed=speed)
        self.data_window.show()
        self.close()
      


class ARINC429GUI(QMainWindow):
    def __init__(self, channel="Channel 1", format_type="Hex", speed="High"):
        super().__init__()
        self.setWindowTitle("Live A429 Monitoring")
        self.resize(800, 600)

        self.channel = channel
        self.format_type = format_type
        self.speed = speed
        self.labCount = 1

        self.init_ui()
        self.setup_mock_data_feed()
        


    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.channel_label = QLabel(f"Channel: {self.channel} | Format: {self.format_type} | Speed: {self.speed}")
        main_layout.addWidget(self.channel_label)

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
        main_layout.addWidget(self.details_box)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.clicked.connect(self.back_to_main)
        main_layout.addWidget(self.back_button)

    def start_stop_data(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_stop_button.setText("Start")
        else:
            self.timer.start(500)
            self.start_stop_button.setText("Stop")

    def setup_mock_data_feed(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_mock_data)
        self.timer.start(500)  # every 500 ms

    #temperary method to simluate A429 data. 
    def add_mock_data(self):

        # Simulate an ARINC word
        label = random.randint(0, 255)
        data = random.randint(0, 0xFFFFF)
        ssm = random.randint(0, 3)
        time_str = "12:00:%02d" % random.randint(0, 59)

        # Format data based on selected format
        format_type = self.format_type
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

        # row = self.table.rowCount()
        # self.table.insertRow(row)
        # self.table.setItem(row, 0, QTableWidgetItem(time_str))
        # self.table.setItem(row, 1, QTableWidgetItem(f"{label:02X}"))
        # self.table.setItem(row, 2, QTableWidgetItem(data_str))
        # self.table.setItem(row, 3, QTableWidgetItem(str(ssm)))
        
        
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem(time_str))
        self.table.setItem(0, 1, QTableWidgetItem(f"{label:02X}"))
        self.table.setItem(0, 2, QTableWidgetItem(data_str))
        self.table.setItem(0, 3, QTableWidgetItem(str(ssm)))
        self.table.setVerticalHeaderItem(0, QTableWidgetItem(str(self.labCount)))
        self.labCount += 1

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

    def back_to_main(self):
        self.timer.stop()
        self.main_menu = MainMenuWindow()
        self.main_menu.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenuWindow()
    main_menu.show()
    sys.exit(app.exec())
