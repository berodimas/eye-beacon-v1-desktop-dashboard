from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget
from eyebeacon_gui3 import *
import sys

from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

from datetime import datetime, date
from camera_stream import *

i = 1

status = {
    'cv': 0,
    'ble': 0,
    'anomaly': 0
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.WebClientWorker = self.WebClientWorker()
        self.WebClientWorker.start()

        self.WebClientHandler = self.WebClientHandler()
        self.WebClientHandler.setter.connect(self.new_report)

        self.ui.button_page_feed.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.page_1))
        self.ui.button_page_feed.clicked.connect(
            self.state_function)
        self.ui.button_page_log.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.page_2))
        self.ui.button_page_log.clicked.connect(
            self.state_function)

        self.screen_width = QApplication.desktop().screenGeometry().width()
        self.screen_height = QApplication.desktop().screenGeometry().height()

        self.container_camera = self.ui.label_camera_stream
        self.camera_address_enter("rtsp://127.0.0.1:8554/cam")

    def camera_address_enter(self, camera_stream_address):
        self.camera_stream_address = camera_stream_address
        self.camera_stream = CameraStream(self.container_camera, self.screen_width //
                                              3, self.screen_height//3, camera_stream_address)
    def state_function(self):
        if self.ui.stacked_widget.currentIndex() == 0:
            self.ui.button_page_feed.setStyleSheet("background-color: rgb(238, 238, 238);\n"
                                                "border-top-left-radius: 5px;\n"
                                                "border-bottom-left-radius: 5px;\n"
                                                "font: 10pt;\n"
                                                "font-weight: bold;\n"
                                                "")
            self.ui.button_page_log.setStyleSheet("background-color: rgb(188, 188, 188);\n"
                                               "border-top-right-radius: 5px;\n"
                                               "border-bottom-right-radius: 5px;\n"
                                               "font: 10pt;\n"
                                               "font-weight: regular;")
        else:
            self.ui.button_page_feed.setStyleSheet("background-color: rgb(188, 188, 188);\n"
                                                "border-top-left-radius: 5px;\n"
                                                "border-bottom-left-radius: 5px;\n"
                                                "font: 10pt;\n"
                                                "font-weight: regular;\n"
                                                "")
            self.ui.button_page_log.setStyleSheet("background-color: rgb(238, 238, 238);\n"
                                               "border-top-right-radius: 5px;\n"
                                               "border-bottom-right-radius: 5px;\n"
                                               "font: 10pt;\n"
                                               "font-weight: bold;")
                   
    def new_report(self):
        global i
        now = datetime.now()
        today = date.today()

        current_time = now.strftime("%H:%M:%S")
        current_date = today.strftime("%B %d, %Y")

        widget_report = QWidget()
        widget_report.setStyleSheet("background-color: rgb(255, 255, 255);\nborder-radius: 5px;")
        layout_report = QGridLayout(widget_report)

        label_date = QLabel(current_date)
        label_time = QLabel(current_time)
        label_time.setAlignment(QtCore.Qt.AlignRight)
        label_detected = QLabel("BLE Detected: {}\nCV Detected: {}".format(status['ble'], status['cv']))
        if status['anomaly'] == 0:
            label_description = QLabel ("No Anomaly")
        else:
            label_description = QLabel("There's an anomaly with {} difference(s)".format(status['anomaly']))

        layout_report.addWidget(label_date, 0, 0, 1, 1)
        layout_report.addWidget(label_time, 0, 1, 1, 1)
        layout_report.addWidget(label_description, 2, 0, 1, 2)
        layout_report.addWidget(label_detected, 1, 0, 1, 2)

        self.layout = self.ui.report_container_layout_2
        self.layout.insertWidget(self.layout.count()-i, widget_report)

        i+=1

    class WebClientHandler(QObject):
        setter = pyqtSignal()

    class WebClient:
        @app.route("/eyebeacon", methods=['POST'])
        def post():
            mainWindow.WebClientHandler.setter.emit()
            if len(status) == 0:
                abort(404)
            if not request.json:
                abort(400)
            if 'cv' in request.json and type(request.json['cv']) is not int:
                abort(400)
            if 'ble' in request.json and type(request.json['ble']) is not int:
                abort(400)
            if 'anomaly' in request.json and type(request.json['anomaly']) is not int:
                abort(400)
            status['cv'] = request.json.get(
                'cv', status['cv'])
            status['ble'] = request.json.get(
                'ble', status['ble'])
            status['anomaly'] = request.json.get(
                'anomaly', status['anomaly'])
            return jsonify({'status': status})

    class WebClientWorker(QThread):
        def run(self):
            app.run(debug=True, use_reloader=False, port=5000)

if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(application.exec_())
