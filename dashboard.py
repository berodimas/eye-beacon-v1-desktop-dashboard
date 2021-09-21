
from ui_file.eyebeacon_gui import *

from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget
from flask import Flask, jsonify, abort, request
from flask_restful import Api, abort
import redis, struct, cv2, os
import numpy as np

os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

app = Flask(__name__)
api = Api(app)

from datetime import datetime, date
import sys

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
        self.r = redis.Redis(host='localhost', port=6379, db=0)

        timer = QTimer(self)
        timer.setInterval(int(1000/30))
        timer.timeout.connect(self.fromRedis)
        timer.start()

    def fromRedis(self):
        """Retrieve Numpy array from Redis key 'n'"""
        encoded = self.r.get('image')
        h, w = struct.unpack('>II',encoded[:8])
        a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
        a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
        self.img = QImage(a, a.shape[1], a.shape[0],
                      QImage.Format_RGB888)
        self.pix = QPixmap.fromImage(self.img)
        self.pix = self.pix.scaledToHeight(self.container_camera.height())
        self.container_camera.setPixmap(self.pix)


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
        @app.route("/eyebeacon/dashboard/logs", methods=['POST'])
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
