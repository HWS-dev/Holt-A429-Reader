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
        self.format_combo.addItems(["BNR", "Binary", "BCD", "Hex"])
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
        self.data_window = LabelMenu(channel=channel,format_type=format_type, speed=speed)
        self.data_window.show()
        self.close()
      


class LabelMenu(QMainWindow):
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

        top_bar = QHBoxLayout()

        self.channel_label = QLabel(f"Channel: {self.channel} | Format: {self.format_type} | Speed: {self.speed}")
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        top_bar.addWidget(self.channel_label)
        self.start_stop_button = QPushButton("Stop")
        self.start_stop_button.clicked.connect(self.start_stop_data)
        top_bar.addWidget(self.start_stop_button)
        top_bar.addStretch()
        top_bar.addWidget(self.logo)
        main_layout.addLayout(top_bar)

        # ARINC 429 Table
        self.liveTable = QTableWidget()
        self.liveTable.setColumnCount(6)
        self.liveTable.setHorizontalHeaderLabels(["Time", "Label", "SDI", "Data", "SSM", "Parity"])
        main_layout.addWidget(QLabel("Live ARINC Words"))
        main_layout.addWidget(self.liveTable)

        # Parsed Word Display
        main_layout.addWidget(QLabel("Labels Detected"))
        self.labelTable = QTableWidget()
        # self.labelTable.setColumnCount(7)
        # self.labelTable.setHorizontalHeaderLabels(["Label", "SDI", "Data", "SSM", "Parity", "Parameter", "Units"])
        self.labelTable.setColumnCount(4)
        self.labelTable.setHorizontalHeaderLabels(["Label", "Data", "Parameter", "Units"])
        main_layout.addWidget(self.labelTable)

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
        label = random.randint(202, 206)
        sdi = format(random.randint(0,3),'02b')
        data = random.randint(0, 0xFFFF)
        ssm = random.randint(0, 3)
        parity = random.randint(0, 1)
        time_str = "12:00:%02d" % random.randint(0, 59)

        label = str(oct(label)[2:])

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

        data_proc = int(self.to_bnr(data))
        
        data_conv, units, param = self.data_decode(label, data_proc)
        data_conv = str(data_conv)
        # row = self.table.rowCount()
        # self.table.insertRow(row)
        # self.table.setItem(row, 0, QTableWidgetItem(time_str))
        # self.table.setItem(row, 1, QTableWidgetItem(f"{label:02X}"))
        # self.table.setItem(row, 2, QTableWidgetItem(data_str))
        # self.table.setItem(row, 3, QTableWidgetItem(str(ssm)))
        
        
        self.liveTable.insertRow(0)
        self.liveTable.setItem(0, 0, QTableWidgetItem(time_str))
        self.liveTable.setItem(0, 1, QTableWidgetItem(label))
        self.liveTable.setItem(0, 2, QTableWidgetItem(sdi))
        self.liveTable.setItem(0, 3, QTableWidgetItem(data_str))
        self.liveTable.setItem(0, 4, QTableWidgetItem(str(ssm)))
        self.liveTable.setItem(0, 5, QTableWidgetItem(str(parity)))
        self.liveTable.setVerticalHeaderItem(0, QTableWidgetItem(str(self.labCount)))
        self.labCount += 1

    # Check if label already exists in labelTable
        existing_row = -1
        if self.labCount == 2:
            self.labelTable.insertRow(0)
            self.labelTable.setItem(0, 0, QTableWidgetItem(label))
            # self.labelTable.setItem(0, 1, QTableWidgetItem(sdi))
            self.labelTable.setItem(0, 1, QTableWidgetItem(data_conv))
            # self.labelTable.setItem(0, 3, QTableWidgetItem(str(ssm)))
            # self.labelTable.setItem(0, 4, QTableWidgetItem(str(parity)))
            self.labelTable.setItem(0, 2, QTableWidgetItem(str(param)))
            self.labelTable.setItem(0, 3, QTableWidgetItem(str(units)))
        else:
            for row in range(self.labelTable.rowCount()):
                if self.labelTable.item(row, 0).text().strip() == label.strip():
                    existing_row = row
                    break

            if existing_row == -1:
                self.labelTable.insertRow(0)
                self.labelTable.setItem(0, 0, QTableWidgetItem(label))
                # self.labelTable.setItem(0, 1, QTableWidgetItem(sdi))
                self.labelTable.setItem(0, 1, QTableWidgetItem(data_conv))
                # self.labelTable.setItem(0, 3, QTableWidgetItem(str(ssm)))
                # self.labelTable.setItem(0, 4, QTableWidgetItem(str(parity)))
                self.labelTable.setItem(0, 2, QTableWidgetItem(str(param)))
                self.labelTable.setItem(0, 3, QTableWidgetItem(str(units)))
            else:
                # self.labelTable.setItem(existing_row, 1, QTableWidgetItem(sdi))
                self.labelTable.setItem(existing_row, 1, QTableWidgetItem(data_conv))
                # self.labelTable.setItem(existing_row, 3, QTableWidgetItem(str(ssm)))
                # self.labelTable.setItem(existing_row, 4, QTableWidgetItem(str(parity)))
                self.labelTable.setItem(existing_row, 2, QTableWidgetItem(str(param)))
                self.labelTable.setItem(existing_row, 3, QTableWidgetItem(str(units)))

        # self.labelTable.insertRow(0)
        # self.labelTable.setItem(0, 0, QTableWidgetItem(label))
        # self.labelTable.setItem(0, 1, QTableWidgetItem(sdi))
        # self.labelTable.setItem(0, 2, QTableWidgetItem(data_str))
        # self.labelTable.setItem(0, 3, QTableWidgetItem(str(ssm)))
        # self.labelTable.setItem(0, 4, QTableWidgetItem(str(parity)))
        # self.labelTable.setVerticalHeaderItem(0, QTableWidgetItem(str(self.labCount)))


        # self.details_box.setPlainText(
        #     f"Label: {label:02X}\nData: {data_str}\nSSM: {ssm}\nTimestamp: {time_str}"
        # )

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

    #decoding known lables. 
    def data_decode(self, label, data):
        if label == '312':
            data = round(data*0.125,3)
            param = "Ground Speed"
            units = 'knots'
        elif label == '313':
            data = round(data*0.0055,3)
            param = "Ground Track (True)"
            units = 'degrees'
        elif label == '314':
            data = round(data*0.0055,3)
            param = "Heading (True)"
            units = 'degrees'
        elif label == '315':
            data = round(data*0.125,3)
            param = "Wind Speed"
            units = 'Knots'
        elif label == '316':
            data = round(data*0.0055,3)
            param = "Wind Direction"
            units = 'degrees'
        else:
            param = 'unk'
            units = 'unk'
        return data, units, param

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenuWindow()
    main_menu.show()
    sys.exit(app.exec())
